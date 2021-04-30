import io
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import fpdf
from test.conftest import assert_pdf_equal

HERE = Path(__file__).resolve().parent


def test_insert_jpg(tmp_path):
    pdf = fpdf.FPDF()
    pdf.compress = False
    pdf.add_page()
    file_path = HERE / "insert_images_insert_jpg.jpg"
    pdf.image(file_path, x=15, y=15, h=140)
    if sys.platform in ("cygwin", "win32"):
        # Pillow uses libjpeg-turbo on Windows and libjpeg elsewhere,
        # leading to a slightly different image being parsed and included in the PDF:
        assert_pdf_equal(pdf, HERE / "image_types_insert_jpg_windows.pdf", tmp_path)
    else:
        assert_pdf_equal(pdf, HERE / "image_types_insert_jpg.pdf", tmp_path)


def test_insert_png(tmp_path):
    pdf = fpdf.FPDF()
    pdf.compress = False
    pdf.add_page()
    file_path = HERE / "insert_images_insert_png.png"
    pdf.image(file_path, x=15, y=15, h=140)
    assert_pdf_equal(pdf, HERE / "image_types_insert_png.pdf", tmp_path)


def test_insert_bmp(tmp_path):
    pdf = fpdf.FPDF()
    pdf.compress = False
    pdf.add_page()
    file_path = HERE / "circle.bmp"
    pdf.image(file_path, x=15, y=15, h=140)
    assert_pdf_equal(pdf, HERE / "image_types_insert_bmp.pdf", tmp_path)


def test_insert_gif(tmp_path):
    pdf = fpdf.FPDF()
    pdf.compress = False
    pdf.add_page()
    file_path = HERE / "circle.gif"
    pdf.image(file_path, x=15, y=15)
    assert_pdf_equal(pdf, HERE / "image_types_insert_gif.pdf", tmp_path)


def test_insert_pillow(tmp_path):
    pdf = fpdf.FPDF()
    pdf.add_page()
    file_path = HERE / "insert_images_insert_png.png"
    img = Image.open(file_path)
    pdf.image(img, x=15, y=15, h=140)
    assert_pdf_equal(pdf, HERE / "image_types_insert_png.pdf", tmp_path)


def test_insert_pillow_issue_139(tmp_path):
    pdf = fpdf.FPDF()
    pdf.add_page()
    font = ImageFont.truetype("arial.ttf", 40)
    for y in range(5):
        for x in range(4):
            img = Image.new(mode="RGB", size=(100, 100), color=(60, 255, 10))
            ImageDraw.Draw(img).text((20, 20), f"{y}{x}", fill="black", font=font)
            pdf.image(img, x=x * 50 + 5, y=y * 50 + 5, w=45)
    assert_pdf_equal(pdf, HERE / "insert_pillow_issue_139.pdf", tmp_path)


def test_insert_bytesio(tmp_path):
    pdf = fpdf.FPDF()
    pdf.add_page()
    file_path = HERE / "insert_images_insert_png.png"
    img = Image.open(file_path)
    img_bytes = io.BytesIO()
    img.save(img_bytes, "PNG")
    pdf.image(img_bytes, x=15, y=15, h=140)
    assert_pdf_equal(pdf, HERE / "image_types_insert_png.pdf", tmp_path)