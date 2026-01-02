from fpdf import FPDF
from fpdf.enums import XPos, YPos

class ProjectReport(FPDF):
    def __init__(self, font_name, student_name):
        super().__init__()
        self.font_name = font_name
        self.student_name = student_name

    def header(self):
        if self.page_no() > 1:
            self.set_font(self.font_name, 'I', 8)
            self.cell(0, 10, 'Analiza Liniowego Układu Automatyki', align='R', 
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.font_name, 'I', 8)
        self.cell(0, 10, f'Strona {self.page_no()}', align='C')

    def chapter_title(self, label):
        self.set_font(self.font_name, 'B', 14)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, label, fill=True, align='L', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)