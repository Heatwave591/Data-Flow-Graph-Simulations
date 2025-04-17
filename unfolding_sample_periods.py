import math
from fractions import Fraction

def parse_fraction(value: str) -> float:
    try:
        return float(Fraction(value))
    except ZeroDivisionError:
        print("Error: Division by zero in input.")
        exit(1)
    except Exception as e:
        print(f"Error: Invalid input '{value}'. {e}")
        exit(1)

def find_j_for_sample_period(Tc, Tclk, max_j=100):
    min_diff = float('inf')
    closest_j = -1
    closest_spj = None

    for j in range(1, max_j + 1):
        Tcj = j * Tc
        Tclkj = max(math.ceil(Tcj), Tclk)
        spj = Tclkj / j

        print(f"j = {j}\tTcj = {Tcj:.6f}\tTclkj = {Tclkj:.6f}\tspj = {spj:.6f}")

        if abs(spj - Tc) < 1e-6:
            print(f"\nSP =  equals Tc at j = {j}")
            return j

        if abs(spj - Tc) < min_diff:
            min_diff = abs(spj - Tc)
            closest_j = j
            closest_spj = spj

    print("\nNo j where SP = Tc")
    print(f"Closest j is {closest_j} with spj ≈ {closest_spj:.6f}")
    return -1

if __name__ == "__main__":
    Tc_input = input("Iteration Bound:  ")
    Tclk_input = input("Clock Period: ")

    Tc = parse_fraction(Tc_input)
    Tclk = parse_fraction(Tclk_input)

    find_j_for_sample_period(Tc, Tclk)