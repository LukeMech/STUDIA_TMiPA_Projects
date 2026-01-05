import sympy as sp
from modules.plots import save_latex_img, generate_analysis_plots
from modules.diagrams import draw_main_diagram, draw_reduced_diagram

def generate_assets(sys):
    """
    Generuje wszystkie zasoby graficzne: diagramy, wykresy, wzory.
    """
    print("Generowanie obrazów podstawowych...")
    save_latex_img(r"G(s) = \frac{1}{4s+1}", "obj.png")
    save_latex_img(rf"G_{{cl}}(s) = \frac{{G(s)}}{{1 + G(s) H(s)}} = {sp.latex(sys['G_cl_sym'])}", "final_tf.png")

    print("Generowanie założeń...")
    save_latex_img(r"G(s) = \frac{1}{4s+1}", "G_eq.png")
    save_latex_img(r"G_r(s) = \frac{1}{s}", "Gr_eq.png")
    save_latex_img(r"k_1 = 0.2", "k1_eq.png")
    save_latex_img(r"k_2 = 0.7", "k2_eq.png")
    save_latex_img(r"k_3 = 1.8", "k3_eq.png")

    print("Generowanie kroków obliczeń transmitancji...")
    save_latex_img(r"H_{wew}(s) = k_1 (G_r(s) + k_2) = 0.2 \left( \frac{1}{s} + 0.7 \right)", "step1.png")
    save_latex_img(r"H(s) = k_3 H_{wew}(s) = 0.36 \left( \frac{1}{s} + 0.7 \right)", "step2.png")

    print("Generowanie wykresów analizy...")
    generate_analysis_plots(sys['G_cl_num'], sys['L_num'], "step.png", "nyquist.png")

    print("Generowanie diagramu blokowego...")
    draw_main_diagram("main_diag.png")

    print("Generowanie diagramu zastępczego...")
    draw_reduced_diagram("reduced_diag.png")

    print("Generowanie wzorów transmitancji widmowej...")
    save_latex_img(r"s = j\omega \to L(j\omega) = \frac{0.36 + j0.252\omega}{-4\omega^2 + j\omega}", "L_jw_eq.png")
    save_latex_img(r"Re[L(j\omega)] = \frac{-1.188}{16\omega^2 + 1}", "Re_eq.png")
    save_latex_img(r"Im[L(j\omega)] = \frac{-(0.36 + 1.008\omega^2)}{\omega(16\omega^2 + 1)}", "Im_eq.png")

    print("Generowanie zasobów zakończone.")