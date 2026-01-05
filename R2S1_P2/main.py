"""
Projekt 2 - Analiza Liniowego Układu Automatyki
Autor: Łukasz Błaszczyk
Data: 2 stycznia 2026
"""

import os
from modules.calculations import get_system_functions
from modules.assets import generate_assets
from modules.pdf_report import ProjectReport
from fpdf.enums import XPos, YPos

# Konfiguracja projektu
k1, k2, k3 = 0.2, 0.7, 1.8
student_name = "Łukasz Błaszczyk"
student_number = "339513"
code_link = "https://github.com/LukeMech/STUDIA_TMiPA_Projects/tree/main/R2S1_P2"
font_name = "Roboto"
font_base = f"res/fonts/{font_name}"

def main():
    """
    Główna funkcja programu - wykonuje analizę systemu i generuje raport.
    """
    print("Rozpoczynam analizę systemu...")

    # Obliczenia podstawowych transmitancji
    sys = get_system_functions(k1, k2, k3)
    print("Obliczenia transmitancji zakończone.")

    # Generowanie zasobów graficznych
    generate_assets(sys)

    # Tworzenie raportu PDF
    print("Tworzenie raportu PDF...")
    pdf = ProjectReport(font_name, student_name)
    pdf.add_font(font_name, "", f"{font_base}.ttf")
    pdf.add_font(font_name, "B", f"{font_base}_Bold.ttf")
    pdf.add_font(font_name, "I", f"{font_base}_Italic.ttf")
    pdf.add_font(font_name, "BI", f"{font_base}_Bold_Italic.ttf")

    def add_img_to_ch(img_name, w=45, ydel = 4):
        pdf.image(img_name, w=w)
        pdf.set_y(pdf.get_y() - ydel)

    # Strona tytułowa
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font("Roboto", "B", 26)
    pdf.cell(0, 10, "Projekt 2 TMiPA 2025/2026", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Roboto", "BI", 20)
    pdf.cell(0, 20, "Analiza liniowego układu automatyki", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Roboto", "B", 14)
    pdf.cell(0, 10, f"{student_name}, {student_number}", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Roboto", "I", 14)
    pdf.cell(0, 10, f"Zrobione w Pythonie, dostępne na github:", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT, link=code_link)
    pdf.set_text_color("#FB4AC5")  # Set text color to pink
    pdf.cell(0, 10, code_link, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT, link=code_link)
    pdf.set_text_color(0, 0, 0)  # Reset text color to black
    pdf.set_font("Roboto", "", 14)  # Reset font style


    # Rozdziały
    pdf.add_page()
    pdf.chapter_title("Założenia")
    pdf.image("main_diag.png", x=15, w=180)

    pdf.set_y(pdf.get_y() - 8)
    for img in ["G_eq.png", "Gr_eq.png", "k1_eq.png", "k2_eq.png", "k3_eq.png"]:
        add_img_to_ch(img)
    pdf.set_y(pdf.get_y() + 8)

    pdf.chapter_title("a) Transmitancja zastępcza (redukcja układu do 1 bloku)")
    pdf.image("reduced_diag.png", x=67.5, w=100)
    pdf.set_y(pdf.get_y() - 6)

    for img in ["step1.png", "step2.png"]:
        add_img_to_ch(img, w=90, ydel=6)
    pdf.set_y(pdf.get_y() + 2)
    add_img_to_ch("final_tf.png", w=110, ydel=-8)

    pdf.chapter_title("b) Analiza wymuszenia skokowego u0(t) = 2*1(t)")
    pdf.image("step.png", x=10, w=180)
    
    pdf.add_page()
    pdf.chapter_title("c) Wykres Nyquista")
    pdf.set_y(pdf.get_y() - 6)
    add_img_to_ch("Re_eq.png", w=60)
    add_img_to_ch("Im_eq.png", w=80)
    add_img_to_ch("L_jw_eq.png", w=100, ydel=0)
    pdf.image("nyquist.png", x=10, w=180)
    
    pdf.add_page()
    pdf.chapter_title("d) Redukcja transmitancji operatorowej sprzężenia")
    add_img_to_ch("step2.png", w=90, ydel=6)

    # Zapisywanie PDF
    nazwa_raportu = f"Raport_TMiPA_{student_name.replace(' ', '_')}.pdf"
    pdf.output(nazwa_raportu)
    print(f"Raport zapisany jako: {nazwa_raportu}")

    # Czyszczenie plików tymczasowych
    deleted_files = []
    for plik in os.listdir("."):
        if plik.endswith(".png"):
            try:
                if os.path.isfile(plik):
                    os.remove(plik)
                    deleted_files.append(plik)
            except OSError as e:
                print(f"Nie można usunąć pliku {plik}: {e}")
    
    if deleted_files:
        print(f"Pliki tymczasowe usunięte ({len(deleted_files)}): {', '.join(deleted_files)}")
    else:
        print("Brak plików tymczasowych do usunięcia.")

    print("Analiza zakończona pomyślnie!")

if __name__ == "__main__":
    main()