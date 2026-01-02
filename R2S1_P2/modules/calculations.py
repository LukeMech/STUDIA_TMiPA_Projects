import sympy as sp
import control as ctrl

def get_system_functions(k1, k2, k3):
    # Symbolika (SymPy)
    s = sp.symbols('s')
    G_s = 1 / (4*s + 1)
    Gr_s = 1 / s
    H_wew = k1 * (Gr_s + k2)
    H_total = sp.simplify(k3 * H_wew)
    G_cl_sym = sp.simplify(G_s / (1 + G_s * H_total))

    # Numerycznie (Control)
    sn = ctrl.TransferFunction.s
    Gn = 1 / (4*sn + 1)
    Grn = 1 / sn
    Hn = k3 * k1 * (Grn + k2)
    G_cl_num = ctrl.feedback(Gn, Hn)
    L_num = Gn * Hn

    return {
        "G_s": G_s, "Gr_s": Gr_s, "G_cl_sym": G_cl_sym,
        "G_cl_num": G_cl_num, "L_num": L_num
    }