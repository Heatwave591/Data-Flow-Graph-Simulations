#!/usr/bin/env python3
import argparse
import sympy as sp

def main():
    # Symbol for polynomial variable
    p = sp.symbols('p')

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="General Cook–Toom setup for lengths L, N and points β"
    )
    parser.add_argument('--L',  type=int, required=True,
                        help="length of x(p) (degree ≤ L-1)")
    parser.add_argument('--N',  type=int, required=True,
                        help="length of h(p) (degree ≤ N-1)")
    parser.add_argument('--beta', type=float, nargs='+', required=True,
                        help="evaluation points β₀ … β_{L+N-2}")
    args = parser.parse_args()

    L, N = args.L, args.N
    print(f"[DEBUG] L = {L}, N = {N}")
    beta = [sp.Rational(b) for b in args.beta]
    print(f"[DEBUG] beta = {beta}")
    d = L + N - 2            # degree of s(p)
    m = len(beta)
    if m != d+1:
        raise ValueError(f"Expected {d+1} β's, got {m}")
    print(f"[DEBUG] m = {m}, expected = {d+1}")

    # Create symbolic coeffs
    x_syms = sp.symbols(f'x0:{L}')
    h_syms = sp.symbols(f'h0:{N}')

    # 1) Define polynomials
    x = sum(x_syms[j]*p**j for j in range(L))
    print(f"[DEBUG] x(p) = {x}")
    h = sum(h_syms[j]*p**j for j in range(N))
    print(f"[DEBUG] h(p) = {h}")
    s = sp.expand(x*h)
    print(f"[DEBUG] s(p) = {s}")

    # print("\n1) Definitions:")
    # print(f"   x(p) = {x}")
    # print(f"   h(p) = {h}")
    # print(f"   s(p) = x(p)*h(p) = {s}")

    # 2) Evaluate at beta_i
    print("\n2) Evaluations:")
    print("   i    β_i     h(β_i)           x(β_i)           s(β_i)")
    for i, b in enumerate(beta):
        hv = sp.simplify(h.subs(p,b))
        xv = sp.simplify(x.subs(p,b))
        sv = sp.simplify(s.subs(p,b))
        print(f"   {i:>1}    {b!s:<3}   {hv!s:<15} {xv!s:<15} {sv!s}")

    # 3) Lagrange basis & terms
    print("\n3) Lagrange interpolation:")
    terms = []
    ell = []
    for i, bi in enumerate(beta):
        num, den = 1, 1
        for bj in beta:
            if bj==bi: continue
            num *= (p - bj)
            den *= (bi - bj)
        Li = sp.simplify(num/den)
        Si = sp.simplify(s.subs(p, bi))
        terms.append(Si*Li)
        ell.append(Li)
        # print(f"   s{i} = ({sp.factor(num)})/({den}) = {Li}")
        print(f"   term_{i} = (s_{i}*{sp.factor(num)})/({den}) = s_{i}*{Li}")
        # print(f"   term {i}: S({bi})·ℓ_{i}(p) = {Si}·{Li}")

    Sinterp = sp.simplify(sum(terms))
    print(f"[DEBUG] Interpolated s(p) = {Sinterp}")
    # print(f"\n   ⇒  s(p) = {sp.expand(Sinterp)}")

    # 4) Extract coefficients s0..sd
    coeffs = [sp.simplify(Sinterp.coeff(p,k)) for k in range(d+1)]
    print(f"[DEBUG] Coefficients of s(p): {[str(c) for c in coeffs]}")
    # print("\n4) Coefficients:")
    print("   s(p) = " + " + ".join(f"s_{k}·p^{k}" for k in range(d+1)))
    # for k, ck in enumerate(coeffs):
    #     print(f"   s_{k} = {ck}")

    # 5) Build B, G, G_int and fractional D
    # Pre-process matrix B (m×L)
    B = sp.Matrix([[beta[i]**j for j in range(L)] for i in range(m)])
    print("[DEBUG] Pre-processing matrix B created")

    # Lagrange interpolation matrix G (size (d+1)×m)
    G = sp.zeros(d+1, m)
    for i in range(m):
        poly = sp.Poly(ell[i], p)
        for monom, c in poly.terms():
            k = monom[0]
            G[k, i] = sp.simplify(c)

    # Find scale to clear fractions in G
    dens = [sp.denom(G[i, j]) for i in range(d+1) for j in range(m)]
    scale = sp.ilcm(*dens)

    print("[DEBUG] Computing G_int = scale * G")
    print("[DEBUG] G before scaling:")
    sp.pprint(G)

    G_int = (G * scale).applyfunc(sp.simplify)

    print("[DEBUG] G after scaling and simplification:")
    sp.pprint(G_int)
    
    G_int = (G*scale).applyfunc(sp.simplify)
    print(f"[DEBUG] Integer interpolation matrix G_int created with scale = {scale}")

    # Diagonal eval‑matrix with fractions in h
    h_eval = []
    for i in range(m):
        val = sum(h_syms[j] * beta[i]**j for j in range(N))
        print(f"[DEBUG] h(β_{i}) = {val}")
        h_eval.append(val)
    D_frac = sp.diag(*[sp.simplify(val/scale) for val in h_eval])
    print("[DEBUG] Diagonal matrix D_frac created")

    print("\n5) Matrices for convolution:")
    print("   [s_0…s_d]^T = G_int · D_frac · B · [x_0…x_{L-1}]^T\n")
    print("   Pre‑processing B:")
    sp.pprint(B)
    print("\n   Diagonal eval‑matrix D_frac:")
    sp.pprint(D_frac)
    print(f"\n   Integer post‑process G_int (scale={scale}):")
    sp.pprint(G_int)
    print()

if __name__ == '__main__':
    main()
