import sympy as sp
from modules.plots import save_latex_img, generate_analysis_plots
from modules.diagrams import draw_main_diagram, draw_reduced_diagram

def generate_assets(sys, k1, k2, k3):
    """
    Generuje wszystkie zasoby graficzne automatycznie na podstawie parametrów.
    """
    s = sp.symbols('s')
    w = sp.symbols('omega', real=True)

    # Obiekt G(s) jest stały w tym zadaniu
    save_latex_img(r"G(s) = \frac{1}{4s+1}", "obj.png")
    # G_cl_sym jest już przeliczone w sys
    save_latex_img(rf"G_{{cl}}(s) = \frac{{G(s)}}{{1 + G(s) H(s)}} = {sp.latex(sys['G_cl_sym'])}", "final_tf.png")

    save_latex_img(r"G(s) = \frac{1}{4s+1}", "G_eq.png")
    save_latex_img(r"G_r(s) = \frac{1}{s}", "Gr_eq.png")
    save_latex_img(rf"k_1 = {k1}", "k1_eq.png")
    save_latex_img(rf"k_2 = {k2}", "k2_eq.png")
    save_latex_img(rf"k_3 = {k3}", "k3_eq.png")

    # Dynamiczne wyliczenie H_wew i H(s) dla LaTeX
    h_wew_expr = k1 * (1/s + k2)
    h_total_expr = k3 * h_wew_expr
    
    save_latex_img(rf"H_{{wew}}(s) = k_1 (G_r(s) + k_2) = {sp.latex(h_wew_expr)}", "step1.png")
    save_latex_img(rf"H(s) = k_3 H_{{wew}}(s) = {sp.latex(sp.simplify(h_total_expr))}", "step2.png")

    # Obliczenie L(jw) poprzez podstawienie s = jw
    l_sym = sys['L_sym']
    l_jw = l_sym.subs(s, sp.I * w)
    
    # Wyznaczenie części rzeczywistej i urojonej
    # simplify pomaga uzyskać czytelną postać ułamkową
    re_l = sp.simplify(sp.re(l_jw))
    im_l = sp.simplify(sp.im(l_jw))

    save_latex_img(rf"s = j\omega \to L(j\omega) = {sp.latex(sp.simplify(l_jw))}", "L_jw_eq.png")
    save_latex_img(rf"Re[L(j\omega)] = {sp.latex(re_l)}", "Re_eq.png")
    save_latex_img(rf"Im[L(j\omega)] = {sp.latex(im_l)}", "Im_eq.png")

    generate_analysis_plots(sys['G_cl_num'], sys['L_num'], "step.png", "nyquist.png")

    draw_main_diagram("main_diag.png")
    draw_reduced_diagram("reduced_diag.png")
