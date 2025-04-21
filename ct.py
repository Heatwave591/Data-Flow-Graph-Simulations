import numpy as np
from numpy.polynomial.polynomial import Polynomial

# Step 1: Define Lagrange basis polynomial
def lagrange_basis(xs, i):
    xi = xs[i]
    basis = Polynomial([1.0])
    for j, xj in enumerate(xs):
        if j != i:
            basis *= Polynomial([-xj, 1.0]) / (xi - xj)
    return basis

# Step 2: Input signal and kernel
input_vals = [1, ]       # Input polynomial: t(x) = 1 + 2x + 3x^2
kernel_vals = [4, 5, 6]      # Kernel polynomial: g(x) = 4 + 5x + 6x^2

# Step 3: Choose interpolation points
x_points = [-1, 0, 1, 2]     # Choose enough points to cover degree(input)+degree(kernel)

# Step 4: Evaluate both polynomials at the points
def evaluate_poly(coeffs, xs):
    return [np.polyval(list(reversed(coeffs)), x) for x in xs]

t_evals = evaluate_poly(input_vals, x_points)
g_evals = evaluate_poly(kernel_vals, x_points)

# Step 5: Pointwise multiplication of evaluations
h_evals = [a * b for a, b in zip(t_evals, g_evals)]

# Step 6: Interpolate to get the resulting polynomial h(x)
h_poly = sum(h * lagrange_basis(x_points, i) for i, h in enumerate(h_evals))
h_coeffs = h_poly.coef[:len(input_vals) + len(kernel_vals) - 1]  # Crop to valid length

# Step 7: Print the output coefficients
print("Cook-Toom (Lagrange) Convolution Result:")
for i, coeff in enumerate(h_coeffs):
    print(f"x^{i} coefficient: {coeff:.3f}")