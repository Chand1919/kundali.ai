from src.pdf_generator import PDFGenerator
import os

def test_generate_pdf(tmp_path):
    pdf = PDFGenerator(output_dir=tmp_path)
    file_path = pdf.generate({"name": "Project X"}, "test.pdf")
    assert os.path.exists(file_path)


