import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

lw = 2
pm_fs = 24
d_fs = 14
arrow_props = dict(arrowstyle='->', lw=lw, color='black', connectionstyle="angle,angleA=90,angleB=0")
arrow_props_B = dict(arrowstyle='->', lw=lw, color='black', connectionstyle="angle,angleA=0,angleB=90")

# Pomocnicza funkcja do rysowania bloków
def draw_block(ax, x, y, w, h, tekst):
    rect = patches.Rectangle((x-w/2, y-h/2), w, h, linewidth=2, edgecolor='black', facecolor='white')
    ax.add_patch(rect)
    ax.text(x, y, tekst, ha='center', va='center', fontsize=14, fontweight='bold')
    return x, y

# Pomocnicza funkcja do rysowania sumatorów
def draw_sum(ax, x, y, r=0.3):
    circle = patches.Circle((x, y), r, linewidth=2, edgecolor='black', facecolor='white')
    ax.add_patch(circle)
    return x, y

def draw_main_diagram(temp_dir, filename):
    filepath = os.path.join(temp_dir, filename)

    _, ax = plt.subplots(figsize=(14, 10))

    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')

    # --- RYSOWANIE ELEMENTÓW ---

    # 1. Tor główny
    draw_sum(ax, 2, 6) # Sumator 1
    draw_block(ax, 6, 6, 2.5, 1.5, "G(s)") # Blok G(s)

    # 2. Tor sprzężenia zwrotnego (pionowo w dół)
    draw_block(ax, 9, 4, 1.5, 1, "k₁") # Blok k1
    draw_block(ax, 6, 3, 2.5, 1.5, "Gᵣ(s)") # Blok Gr(s)
    draw_block(ax, 6, 1, 1.5, 1, "k₂") # Blok k2
    draw_sum(ax, 3.5, 3) # Sumator 2
    draw_block(ax, 2, 4, 1.5, 1, "k₃") # Blok k3
    # --- STRZAŁKI I POŁĄCZENIA ---
    # Wejście u(t) -> Sumator 1
    ax.annotate('', xy=(1.75, 6), xytext=(0.5, 6), arrowprops=arrow_props)
    ax.text(0.4, 6.2, "u(t)", fontsize=d_fs)
    ax.text(1.4, 6.2, "+", fontsize=pm_fs)

    # Sumator 1 -> G(s)
    ax.annotate('', xy=(4.8, 6), xytext=(2.3, 6), arrowprops=arrow_props)

    # G(s) -> Wyjście y(t)
    ax.annotate('', xy=(11, 6), xytext=(7.25, 6), arrowprops=arrow_props)
    ax.text(10.5, 6.2, "y(t)", fontsize=d_fs)

    # Rozgałęzienie do k1
    ax.annotate('', xy=(9, 4.45), xytext=(9, 6), arrowprops=arrow_props)

    # k1 -> Gr(s)
    ax.annotate('', xy=(7.2, 3), xytext=(9, 3.5), arrowprops=arrow_props) # Do Gr(s)
    
    # k1 -> k2
    ax.annotate('', xy=(6.7, 1), xytext=(8, 3), arrowprops=arrow_props) # Do k2

    # Gr(s) -> Sumator 2
    ax.annotate('', xy=(3.75, 3), xytext=(4.75, 3), arrowprops=arrow_props)
    ax.text(3.7, 3.2, "+", fontsize=pm_fs)

    # k2 -> Sumator 2
    ax.annotate('', xy=(3.5, 2.75), xytext=(5.25, 1), arrowprops=arrow_props_B) 
    ax.text(3, 2.5, "+", fontsize=pm_fs)

    # Sumator 2 -> k3
    ax.annotate('', xy=(2, 3.55), xytext=(3.2, 3), arrowprops=arrow_props_B)

    # k3 -> Sumator 1 (Powrót)
    ax.annotate('', xy=(2, 5.75), xytext=(2, 4.5), arrowprops=arrow_props)
    ax.text(1.6, 5.4, "-", fontsize=pm_fs)
    ax.text(2.2, 5.5, "x(t)", fontsize=d_fs)

    # Zapis pliku
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    plt.close()

def draw_reduced_diagram(temp_dir, filename):
    filepath = os.path.join(temp_dir, filename)

    _, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 4)
    ax.set_aspect('equal')
    ax.axis('off')

    # Rysowanie uproszczonego schematu
    # Wejście
    ax.annotate('', xy=(2, 2), xytext=(0, 2), arrowprops=arrow_props)
    ax.text(0, 2.2, "u(t)", fontsize=d_fs)

    # Blok G_cl(s)
    draw_block(ax, 3, 2, 2, 1, "G_cl(s)")

    # Wyjście
    ax.annotate('', xy=(6, 2), xytext=(4, 2), arrowprops=arrow_props)
    ax.text(5.5, 2.3, "y(t)", fontsize=d_fs)

    # Zapis
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    plt.close()

