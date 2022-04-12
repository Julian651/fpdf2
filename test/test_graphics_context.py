from pathlib import Path

import pytest

from fpdf import FPDF, XPos, YPos
from test.conftest import assert_pdf_equal

HERE = Path(__file__).resolve().parent


def test_graphics_context(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(0x00, 0xFF, 0x00)
    pdf.set_fill_color(0xFF, 0x88, 0xFF)
    pdf.set_y(20)
    pdf.cell(txt="outer 01", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
    with pdf.local_context():
        pdf.set_font("courier", "BIU", 30)
        pdf.set_text_color(0xFF, 0x00, 0x00)
        pdf.set_fill_color(0xFF, 0xFF, 0x00)
        pdf.cell(txt="inner 01", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
        pdf.set_x(70)
        with pdf.rotation(30, pdf.get_x(), pdf.get_y()):
            pdf.set_fill_color(0x00, 0xFF, 0x00)
            pdf.cell(txt="inner 02", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
        pdf.set_stretching(150)
        pdf.cell(txt="inner 03", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
    pdf.cell(txt="outer 02", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
    assert_pdf_equal(pdf, HERE / "graphics_context.pdf", tmp_path)


def test_local_context_init(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "", 12)
    with pdf.local_context(
        font_family="Courier", font_style="B", font_size=24, fill_color=(255, 128, 0)
    ):
        pdf.cell(txt="Local context")
    pdf.ln()
    pdf.cell(txt="Back to base")
    assert_pdf_equal(pdf, HERE / "local_context_init.pdf", tmp_path)


def test_invalid_local_context_init():
    pdf = FPDF()
    pdf.add_page()
    with pytest.raises(ValueError):
        with pdf.local_context(font_size_pt=24):
            pass