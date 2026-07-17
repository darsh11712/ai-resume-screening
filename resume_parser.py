import fitz
from docx import Document

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(),filetype='pdf')
    return "\n".join([page.get_text() for page in doc])

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text() for para in doc.paragraphs])