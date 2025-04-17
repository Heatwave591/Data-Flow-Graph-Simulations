import math

def find_j_for_sample_period(Tc, Tclk, max_j=8):
    for j in range(1, max_j + 1):
        Tcj = j * Tc
        Tclkj = max(math.ceil(Tcj), Tclk)
        spj = Tclkj / j

        print(f"j={j}, Tcj={Tcj}, Tclkj={Tclkj}, spj={spj}")

        if abs(spj - Tc) < 1e-6:  # Tolerance for float equality
            print(f"\nSample period equals Tc at j = {j}")
            return j
    print("\nNo value of j found where sample period equals Tc.")
    return -1

# Example usage
Tc = float(input("Enter iteration bound (Tc): "))
Tclk = float(input("Enter clock period (Tclk): "))
find_j_for_sample_period(Tc, Tclk)