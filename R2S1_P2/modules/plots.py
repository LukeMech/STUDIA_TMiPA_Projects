import matplotlib.pyplot as plt
import control as ctrl
import os

def save_latex_img(temp_dir, latex_str, filename, size=22, enhanced_latex=False):
    os.makedirs(temp_dir, exist_ok=True)
    filepath = os.path.join(temp_dir, filename)
    def fun():
        plt.close()
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
        plt.rcParams['font.weight'] = 'regular'
        plt.figure(figsize=(4, 1))
        plt.text(0, 0, f"${latex_str}$", size=size, family='sans-serif', weight='regular')
        plt.axis('off')
        plt.savefig(filepath, dpi=200, transparent=True, bbox_inches='tight')
        plt.close()

    if enhanced_latex:
        plt.rcParams["text.usetex"] = True
        fun()
    else:
        plt.rcParams["text.usetex"] = False
        fun()

def generate_analysis_plots(temp_dir, G_cl, L, step_file, nyquist_file, color):
    os.makedirs(temp_dir, exist_ok=True)
    step_path = os.path.join(temp_dir, step_file)
    nyquist_path = os.path.join(temp_dir, nyquist_file)

    # Skokowa
    t, y = ctrl.step_response(2 * G_cl)
    plt.figure(figsize=(6, 4))
    plt.plot(t, y, linewidth=2, color=color)
    plt.xlabel('Czas [s]')
    plt.ylabel('Wyjście y(t)')
    plt.grid(True)
    plt.savefig(step_path, dpi=150)
    plt.close()

    # Nyquist
    plt.figure(figsize=(5, 5))
    ctrl.nyquist_plot(L, title='', color=color)
    plt.savefig(nyquist_path, dpi=150)
    plt.close()