import sympy as sp
from modules.plots import save_latex_img, generate_analysis_plots
from modules.diagrams import draw_main_diagram, draw_reduced_diagram
import os

def generate_assets(temp_dir, sys, k1, k2, k3, coefficients, color, console):
    """
    Generuje wszystkie zasoby graficzne automatycznie na podstawie parametrów.
    """
    s = sp.symbols('s')
    w = sp.symbols('omega', real=True)

    os.makedirs(temp_dir, exist_ok=True)

    # Obiekt G(s) jest stały w tym zadaniu
    save_latex_img(temp_dir, r"G(s) = \frac{1}{4s+1}", "obj.png")
    # G_cl_sym jest już przeliczone w sys
    save_latex_img(temp_dir, rf"G_{{cl}}(s) = \frac{{G(s)}}{{1 + G(s) H(s)}} = {sp.latex(sys['G_cl_sym'])}", "final_tf.png")

    save_latex_img(temp_dir, r"G(s) = \frac{1}{4s+1}", "G_eq.png")
    save_latex_img(temp_dir, r"G_r(s) = \frac{1}{s}", "Gr_eq.png")
    save_latex_img(temp_dir, rf"k_1 = {k1}", "k1_eq.png")
    save_latex_img(temp_dir, rf"k_2 = {k2}", "k2_eq.png")
    save_latex_img(temp_dir, rf"k_3 = {k3}", "k3_eq.png")

    # Dynamiczne wyliczenie H_wew i H(s) dla LaTeX
    h_wew_expr = k1 * (1/s + k2)
    h_total_expr = k3 * h_wew_expr

    save_latex_img(temp_dir, rf"H_{{wew}}(s) = k_1 (G_r(s) + k_2) = {sp.latex(h_wew_expr)}", "step1.png")
    save_latex_img(temp_dir, rf"H(s) = k_3 H_{{wew}}(s) = {sp.latex(sp.simplify(h_total_expr))}", "step2.png")

    # Obliczenie L(jw) poprzez podstawienie s = jw
    l_sym = sys['L_sym']
    l_jw = l_sym.subs(s, sp.I * w)
    
    # Wyznaczenie części rzeczywistej i urojonej
    # simplify pomaga uzyskać czytelną postać ułamkową
    re_l = sp.simplify(sp.re(l_jw))
    im_l = sp.simplify(sp.im(l_jw))

    save_latex_img(temp_dir, rf"s = j\omega \to L(j\omega) = {sp.latex(sp.simplify(l_jw))}", "L_jw_eq.png")
    save_latex_img(temp_dir, rf"Re[L(j\omega)] = {sp.latex(re_l)}", "Re_eq.png")
    save_latex_img(temp_dir, rf"Im[L(j\omega)] = {sp.latex(im_l)}", "Im_eq.png")

    generate_analysis_plots(temp_dir, sys['G_cl_num'], sys['L_num'], "step.png", "nyquist.png", color)

    draw_main_diagram(temp_dir, "main_diag.png", color)
    draw_reduced_diagram(temp_dir, "reduced_diag.png", color)
    generate_hurwitz_assets(temp_dir, coefficients, console)


def generate_hurwitz_assets(temp_dir, coefficients, console):
    n_order = len(coefficients) - 1
    H = sp.zeros(n_order, n_order)

    # 1. Budowanie macierzy
    for i in range(n_order):
        for j in range(n_order):
            idx = 2 * j + 1 - i
            if 0 <= idx < len(coefficients):
                H[i, j] = coefficients[idx]
            else:
                H[i, j] = 0

    try:
        latex_rows = []
        for i in range(n_order):
            row_vals = [str(round(float(val), 3)) for val in H[i, :]]
            latex_rows.append(" & ".join(row_vals))

        matrix_latex = (
            r"H = \left[ \begin{array}{" + "c" * n_order + r"} "
            + r" \\ ".join(latex_rows)
            + r" \end{array} \right]"
        )

        save_latex_img(temp_dir, matrix_latex, "hurwitz_matrix.png", enhanced_latex=True)

    except Exception:
        console.print("[yellow][W] LaTeX rendering failed, falling back to simple format.")

        rows = []
        for i in range(n_order):
            row_vals = [str(round(float(val), 3)) for val in H[i, :]]
            rows.append(f"[{', '.join(row_vals)}]")
        
        matrix_simple = "H = " + " | ".join(rows)
        save_latex_img(temp_dir, matrix_simple, "hurwitz_matrix.png")

    # 3. Wyznaczniki (determinanty)
    determinants = []
    for i in range(1, n_order + 1):
        det_val = H[:i, :i].det()
        val_numeric = round(float(det_val.evalf()), 4)
        
        # Tutaj też bez dolarów
        det_text = rf"D_{{{i}}} = {val_numeric}"
        save_latex_img(temp_dir, det_text, f"hurwitz_det_{i}.png")
        determinants.append(val_numeric)
