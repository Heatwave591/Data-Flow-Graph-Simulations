import numpy as np
from sympy import symbols, simplify, expand, Matrix, Rational
import sympy as sp

def modified_toom_cook(l, m, beta_values=None):
    """
    Implements the modified Toom-Cook algorithm for fast convolution with correctly
    structured matrices
    
    Parameters:
    l, m: dimensions of the polynomials (l-1 and m-1 are the degrees)
    beta_values: evaluation points (defaults to [0, -1, -2, ...] if not provided)
    
    Returns:
    Reorganized matrices for the algorithm
    """
    
    # Ensure we have enough evaluation points
    if len(beta_values) < l+m-2:
        raise ValueError(f"Need at least {l+m-2} beta values for {l}x{m} convolution")
    
    # Create symbolic variables for polynomials
    p = symbols('p')
    x_coeffs = symbols(f'x0:{l}')
    h_coeffs = symbols(f'h0:{m}')
    
    # Define the input polynomials
    x_poly = sum(x_coeffs[i] * p**i for i in range(l))
    h_poly = sum(h_coeffs[i] * p**i for i in range(m))
    
    # Product polynomial degree
    product_degree = l + m - 1
    
    # Evaluation points
    eval_points = beta_values[:l+m-2]
    
    # Create evaluations of polynomials at beta points
    x_evals = []
    h_evals = []
    for beta in eval_points:
        x_val = x_poly.subs(p, beta)
        h_val = h_poly.subs(p, beta)
        x_evals.append(x_val)
        h_evals.append(h_val)
    
    # Create the highest-degree term of the product
    highest_term = x_coeffs[l-1] * h_coeffs[m-1]
    
    # Step 1: Construct the X transform matrix
    # Maps x coefficients to evaluations at beta points + highest coefficient
    x_transform = np.zeros((len(eval_points) + 1, l), dtype=object)
    
    # Fill rows for evaluation points
    for i, beta in enumerate(eval_points):
        x_row = []
        for j in range(l):
            x_row.append(beta ** j)
        x_transform[i, :] = x_row
    
    # Last row for the highest coefficient
    x_transform[-1, -1] = 1
    
    # Step 2: Construct the H matrix (diagonal with h terms)
    h_matrix = np.zeros((len(eval_points) + 1, len(eval_points) + 1), dtype=object)
    
    # Fill the diagonal with h(beta_i) values
    for i in range(len(eval_points)):
        h_matrix[i, i] = h_evals[i]
    
    # Last diagonal element is h_{m-1}
    h_matrix[-1, -1] = h_coeffs[m-1]
    
    # Step 3: Construct the postprocessing matrix
    # We need to map from evaluations to coefficients
    
    # First, create the Vandermonde matrix for the evaluation points
    vander = np.zeros((len(eval_points) + 1, product_degree), dtype=object)
    
    # Fill rows for evaluation points
    for i, beta in enumerate(eval_points):
        for j in range(product_degree):
            if j < product_degree:
                vander[i, j] = beta ** j
    
    # Add a row for the highest term
    vander[-1, -1] = 1
    
    # Convert to sympy matrix for inversion and exact arithmetic
    vander_sp = Matrix(vander)
    
    # Calculate the postprocessing matrix (inverse of Vandermonde)
    # We'll try to find an integer representation
    try:
        # Compute the raw inverse
        raw_postproc = vander_sp.inv()
        
        # Convert to integers if possible by scaling
        lcm_list = []
        for i in range(raw_postproc.rows):
            for j in range(raw_postproc.cols):
                elem = raw_postproc[i, j]
                if elem.is_Rational:
                    lcm_list.append(elem.q)  # denominator
        
        if lcm_list:
            # Find the LCM of all denominators
            from sympy import lcm
            scaling_factor = 1
            for denom in lcm_list:
                scaling_factor = lcm(scaling_factor, denom)
            
            # Scale the postprocessing matrix to get integers
            postproc = raw_postproc * scaling_factor
            
            # Scale the h-matrix by the inverse to maintain correctness
            for i in range(h_matrix.shape[0]):
                for j in range(h_matrix.shape[1]):
                    if h_matrix[i, j] != 0:
                        h_matrix[i, j] = h_matrix[i, j] / scaling_factor
        else:
            postproc = raw_postproc
            scaling_factor = 1
    except:
        # Fall back to numerical approximation if exact inversion fails
        postproc = Matrix(np.linalg.pinv(vander.astype(float)))
        scaling_factor = 1
    
    return {
        'postprocessing': np.array(postproc),
        'h_matrix': h_matrix,
        'x_transform': x_transform,
        'x_input': np.array(x_coeffs[:l], dtype=object).reshape(l, 1),
        'eval_points': eval_points,
        'scaling_factor': scaling_factor
    }

def format_matrix(matrix):
    """Format matrix elements for better display"""
    result = np.empty(matrix.shape, dtype=object)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix[i, j]
            
            # Check if it's a sympy object
            if hasattr(value, 'is_zero') and value.is_zero:
                result[i, j] = "0"
            elif hasattr(value, 'is_one') and value.is_one:
                result[i, j] = "1"
            elif hasattr(value, 'is_negative_one') and value.is_negative_one:
                result[i, j] = "-1"
            # Handle numeric values
            elif value == 0:
                result[i, j] = "0"
            elif value == 1:
                result[i, j] = "1"
            elif value == -1:
                result[i, j] = "-1"
            else:
                result[i, j] = str(value)
    return result

def count_additions(matrix):
    """Count the number of additions in a matrix"""
    count = 0
    for row in matrix:
        nonzeros = sum(1 for val in row if val != 0 and val != "0")
        if nonzeros > 1:
            count += nonzeros - 1
    return count

def print_matrices(result, l, m):
    """
    Print the matrices in the requested format
    """
    print(f"Modified Toom-Cook {l}x{m} Fast Convolution")
    print("=" * 50)
    print(f"Evaluation points: {result['eval_points']}")
    
    if 'scaling_factor' in result and result['scaling_factor'] != 1:
        print(f"Scaling factor: {result['scaling_factor']} (postprocessing matrix scaled up, H matrix scaled down)")
    
    print("\nPostprocessing Matrix:")
    print(format_matrix(result['postprocessing']))
    
    print("\nH Matrix (with h terms only):")
    print(format_matrix(result['h_matrix']))
    
    print("\nX Transform Matrix:")
    print(format_matrix(result['x_transform']))
    
    print("\nX Input Vector:")
    print(format_matrix(result['x_input']))
    
    # Calculate computational complexity
    postproc_adds = count_additions(result['postprocessing'])
    x_trans_adds = count_additions(result['x_transform'])
    
    print(f"\nTotal additions: postprocessing={postproc_adds}, x_transform={x_trans_adds}")
    print(f"Total multiplications: {len(result['eval_points']) + 1}")  # Number of point evaluations + highest term

# Example for 2x2 convolution with β₀ = 0, β₁ = -1
print("=========== 2x2 Convolution Example ============")
result_2x2 = modified_toom_cook(2, 2, [0, -1])
print_matrices(result_2x2, 2, 2)

# Example for 3x3 convolution 
print("\n\n=========== 3x3 Convolution Example ============")
result_3x3 = modified_toom_cook(3, 3, [0, 1, -1, 2])
print_matrices(result_3x3, 3, 3)

def run_custom():
    try:
        l = int(input("\nEnter value for l: "))
        m = int(input("Enter value for m: "))
        
        # Get beta values
        beta_input = input(f"Enter {l+m-2} beta values separated by commas (or press Enter for defaults): ")
        
        if beta_input.strip():
            beta_values = [int(x.strip()) for x in beta_input.split(',')]
        else:
            beta_values = None
        
        result = modified_toom_cook(l, m, beta_values)
        print_matrices(result, l, m)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("\nWould you like to try a custom configuration?")
    response = input("Enter 'y' for yes, any other key to exit: ")
    if response.lower() == 'y':
        run_custom()