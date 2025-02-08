import os
import PyPDF2
import json
import traceback

from PyPDF2 import PdfReader

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PdfReader(file)
            text = "".join([page.extract_text() or "" for page in pdf_reader.pages])
            return text
        except Exception:
            raise Exception("Error reading the PDF file")

