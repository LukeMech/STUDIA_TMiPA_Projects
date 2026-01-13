from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.panel import Panel
import tomllib, os, shutil, time

# Load students data from students.toml
students_file = "students.toml"
if not os.path.exists(students_file):
    shutil.copy("students.sample.toml", students_file)

with open(students_file, "rb") as f:  # Use binary mode for tomllib
    students_data = tomllib.load(f)

students = [
    (
        student_info["name"],
        student_index,
        student_info["color"],
        student_info["k1"],
        student_info["k2"],
        student_info["k3"],
        student_info["code_link"],
        student_info.get("replace_ai_1", ""),
        student_info.get("replace_ai_2", ""),
        student_info.get("replace_ai_3", ""),
        student_info.get("replace_ai_4", "")
    )
    for student_index, student_info in students_data.items()
]

# Konfiguracja konsoli rich
console = Console()
font_name = "Roboto"
font_base = f"res/fonts/{font_name}"

def main(student_info):
    student_name, student_number, color, k1, k2, k3, code_link, replace_ai_1, replace_ai_2, replace_ai_3, replace_ai_4 = student_info
    # 1. Wyświetlenie tabeli z danymi wejściowymi
    input_table = Table(show_header=False, box=None)
    input_table.add_column("Parametr", style="dim")
    input_table.add_column("Wartość", style="bold yellow")
    input_table.add_row("Student", student_name)
    input_table.add_row("Indeks", student_number)
    input_table.add_row("Kolor", color)
    input_table.add_row("Parametry k", f"k1={k1}, k2={k2}, k3={k3}")
    input_table.add_row("GitHub", code_link)
    
    console.print(Panel(input_table, title="[bold blue]PARAMETRY WEJŚCIOWE PROJEKTU[/bold blue]", border_style="bold blue"))

    # 2. Proces generowania z paskiem postępu
    with Progress(
        SpinnerColumn(speed=2), # Kręcące się kółeczko
        TextColumn("[progress.description]{task.description}"),
        BarColumn(), # Pasek postępu
        TaskProgressColumn(text_format="[yellow]{task.percentage:>3.0f}%"), # Procenty
        console=console
    ) as progress:
        
        # Tworzymy główne zadanie
        overall_task = progress.add_task("[bright_blue]Importowanie bibliotek Python...", total=8)
        
        from modules.calculations import get_system_functions, hurwitz_criterion, is_point_outside_nyquist, get_characteristic_polynomial
        from modules.assets import generate_assets
        from modules.pdf_report import ProjectReport
        from fpdf.enums import XPos, YPos
        from g4f.client import Client

        def get_ai_response(prompt, ws=False):
            client = Client()
            response = client.chat.completions.create(
                model="deepseek",
                messages=[{"role": "user", "content": prompt + " Nie używaj formatowania tekstu (pogrubień przy pomocy * itp.). Odpowiedz w formie czystego tekstu. Nie przekrocz limitu 150 słów."}],
                web_search=ws
            )
            return response.choices[0].message.content
        
        # KROK 1: Obliczenia
        progress.advance(overall_task)

        progress.update(overall_task, description="[green]Obliczanie transmitancji...")
        sys = get_system_functions(k1, k2, k3)
        coefficients = get_characteristic_polynomial(sys['G_cl_sym'])
        progress.advance(overall_task)

        # KROK 2: Zasoby graficzne
        progress.update(overall_task, description="[red]Generowanie wykresów i wzorów...")
        # Warto wyciszyć printy w assets.py, żeby nie "psuły" paska postępu
        temp_dir = f"temp/{student_number}"
        os.makedirs(temp_dir, exist_ok=True)
        generate_assets(temp_dir, sys, k1, k2, k3, coefficients, color)
        progress.advance(overall_task)

        # KROK 3: AI
        progress.update(overall_task, description="[magenta]Generowanie opisów przez AI (może zająć długi czas)...")

        # Zastąp funkcję get_ai_response gotowym stringiem, aby ustawić opis na sztywno, a nie generować go za każdym razem
        if len(replace_ai_1) > 0:
            ai_forcejump_summary = replace_ai_1
        else:
            ai_forcejump_summary = get_ai_response("Podsumuj jak działa wykres odpowiedzi skokowej dla wymuszenia u0(t)=2*1(t). Opisz co się dzieje w układzie i jak to widać na wykresie.")
        progress.advance(overall_task)

        if len(replace_ai_2) > 0:
            ai_nyq_summary = replace_ai_2
        else:
            ai_nyq_summary = get_ai_response("Podsumuj jak działa wykres Nyquista. W tym przypadku do jego narysowania uzylem cz. Re, Im, parametru L_jw. Nie wspominaj co robią - podsumuj jedynie działanie tego wykresu.")
        progress.advance(overall_task)

        # Kryterium Hurwitza
        hurwitz_stable = hurwitz_criterion(coefficients)
        if len(replace_ai_3) > 0:
            ai_hurwitz_summary = replace_ai_3
        else:
            ai_hurwitz_summary = get_ai_response(f"Podsumuj analizę Hurwitza. Układ jest {'stabilny' if hurwitz_stable else 'niestabilny'} - napisz na bazie czego zostało to określone.")
        progress.advance(overall_task)

        nyquist_stable = is_point_outside_nyquist(sys['L_num'])
        if len(replace_ai_4) > 0:
            ai_nyquist_summary = replace_ai_4
        else:
            ai_nyquist_summary = get_ai_response(f"Podsumuj analizę Nyquista. Punkt (-1, 0) {'jest poza' if nyquist_stable else 'nie jest poza'} wykresem - określ co to znaczy.")
        progress.advance(overall_task)

        # KROK 4: PDF
        progress.update(overall_task, description="[cyan]Składanie pliku PDF...")
        pdf = ProjectReport(font_name, student_name)
        pdf.add_font(font_name, "", f"{font_base}.ttf")
        pdf.add_font(font_name, "B", f"{font_base}_Bold.ttf")
        pdf.add_font(font_name, "I", f"{font_base}_Italic.ttf")
        pdf.add_font(font_name, "BI", f"{font_base}_Bold_Italic.ttf")

        def add_img_to_ch(img_name, w=45, ydel=4):
            img_path = f"{temp_dir}/{img_name}"
            pdf.image(img_path, w=w)
            pdf.set_y(pdf.get_y() - ydel)

        # Strona tytułowa
        pdf.add_page()
        pdf.ln(50)
        pdf.set_font(font_name, "B", 26)
        pdf.cell(0, 10, "Projekt 2 TMiPA 2025/2026", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font(font_name, "BI", 20)
        pdf.cell(0, 20, "Analiza liniowego układu automatyki", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font(font_name, "B", 14)
        pdf.cell(0, 10, f"{student_name}, {student_number}", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font(font_name, "I", 14)
        pdf.cell(0, 10, f"Zrobione w Pythonie, kod na Github:", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT, link=code_link)
        try:
            pdf.set_text_color(color)  # Set text color
        except:
            from matplotlib import colors
            pdf.set_text_color(colors.to_hex(color))  # Set text color

        pdf.cell(0, 10, code_link, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT, link=code_link)
        pdf.set_text_color(0, 0, 0)  # Reset text color to black

        # Rozdziały
        pdf.add_page()
        pdf.chapter_title("Założenia")
        pdf.image(f"{temp_dir}/main_diag.png", x=15, w=180)

        pdf.set_y(pdf.get_y() - 8)
        for img in ["G_eq.png", "Gr_eq.png", "k1_eq.png", "k2_eq.png", "k3_eq.png"]:
            add_img_to_ch(img)
        pdf.set_y(pdf.get_y() + 8)

        pdf.chapter_title("a) Transmitancja zastępcza (redukcja układu do 1 bloku)")
        pdf.image(f"{temp_dir}/reduced_diag.png", x=67.5, w=100)
        pdf.set_y(pdf.get_y() - 6)

        for img in ["step1.png", "step2.png"]:
            add_img_to_ch(img, w=90, ydel=6)
        pdf.set_y(pdf.get_y() + 2)
        add_img_to_ch("final_tf.png", w=110, ydel=-8)

        pdf.chapter_title("b) Analiza wymuszenia skokowego u0(t) = 2*1(t)")
        pdf.set_font(font_name, "", 14)  # Reset font style
        pdf.write(text=ai_forcejump_summary+"\n")
        pdf.image(f"{temp_dir}/step.png", x=10, w=180)
        
        pdf.chapter_title("c) Wykres Nyquista")
        pdf.set_font(font_name, "", 14)  # Reset font style
        pdf.write(text=ai_nyq_summary+"\n")
        add_img_to_ch("Re_eq.png", w=60)
        add_img_to_ch("Im_eq.png", w=80)
        add_img_to_ch("L_jw_eq.png", w=100, ydel=0)
        pdf.image(f"{temp_dir}/nyquist.png", x=10, w=180)

        pdf.chapter_title("d) Redukcja transmitancji operatorowej sprzężenia")
        add_img_to_ch("step2.png", w=90, ydel=-10)

        # Dodanie analizy Hurwitza do PDF
        pdf.chapter_title("e) Analiza stabilności (Hurwitz i Nyquist)")

        # Kryterium Hurwitza
        pdf.set_font(font_name, "B", 14)
        pdf.write(text=f"Hurwitz: Układ jest {'stabilny' if hurwitz_stable else 'niestabilny'}" + "\n", )
        pdf.set_font(font_name, "", 14)
        pdf.write(text=ai_hurwitz_summary + "\n\n")

        pdf.write(text="Wyznaczniki Hurwitza:\n")
        pdf.set_y(pdf.get_y() - 10)
        for idx in range(1, len(coefficients)):
            add_img_to_ch(f"hurwitz_det_{idx}.png", w=70, ydel=10)
        pdf.set_y(pdf.get_y() + 10)

        pdf.write(text="Macierz Hurwitza:\n")
        pdf.set_y(pdf.get_y() - 10)
        add_img_to_ch("hurwitz_matrix.png", w=100, ydel=-4)

        # Kryterium Nyquista
        pdf.set_font(font_name, "B", 14)
        pdf.write(text=f"Nyquist: Punkt (-1, 0) {'jest poza' if nyquist_stable else 'nie jest poza'} wykresem. Układ jest {'stabilny' if nyquist_stable else 'niestabilny'}" + "\n", )
        pdf.set_font(font_name, "", 14)
        pdf.write(text=ai_nyquist_summary)

        # Zapisywanie PDF
        nazwa_raportu = f"Raport_TMiPA_{student_name.replace(' ', '_')}.pdf"
        pdf.output(nazwa_raportu)
        progress.advance(overall_task)
                
        # 4. Tabelka końcowa (Wynikowa)
        result_table = Table(show_header=False, box=None)
        result_table.add_row("[bold cyan]PLIK WYJŚCIOWY:[/bold cyan]", f"[underline yellow]{nazwa_raportu}[/underline yellow]")
        
        console.print(Panel(result_table, title="[bold green]FINAŁ[/bold green]", border_style="green"))

        progress.update(overall_task, description="[grey]Sukces!")



if __name__ == "__main__":
    start_time = time.time()

    with Progress(
        SpinnerColumn(speed=2), # Kręcące się kółeczko
        TextColumn("[progress.description]{task.description}"),
        BarColumn(), # Pasek postępu
        TaskProgressColumn(text_format="[yellow]{task.percentage:>3.0f}%"), # Procenty
        console=console
    ) as main_progress:
        
        main_task = main_progress.add_task("[bright_blue]System generowania działa...", total=students.__len__())

        for s in students:
            main(s)
            main_progress.advance(main_task)
        
        # Sprzątanie
        temp_dir = "temp"
        main_progress.update(main_task, description="[red]Usuwanie plików tymczasowych...")
        shutil.rmtree(temp_dir)

        end_time = time.time()
        elapsed_time = end_time - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)

        main_progress.advance(main_task)
        main_progress.update(main_task, description=f"[bold green]Wszystko gotowe po {minutes} minutach i {seconds} sekundach.[/bold green]")
