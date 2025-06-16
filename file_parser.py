import pandas as pd
import os
import re
from PyPDF2 import PdfReader

def parse_xls(file_path):
    """Parse Excel .xls or .xlsx file and return as DataFrame."""
    try:
        xls = pd.ExcelFile(file_path)
        df = xls.parse(xls.sheet_names[0])
        return df
    except Exception as e:
        raise ValueError(f"Failed to parse XLS/XLSX file: {e}")

def parse_pdf(file_path):
    """Parse PDF file and return list of claim-relevant lines."""
    try:
        reader = PdfReader(file_path)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        rows = [line.strip() for line in text.split("\n") if line.strip()]
        # Very basic claim detection: capture lines with NDC-like formatting
        data = []
        for line in rows:
            if re.search(r"\d{5}-\d{4}-\d{2}", line):  # crude NDC format match
                data.append(line)
        return data
    except Exception as e:
        raise ValueError(f"Failed to parse PDF file: {e}")

def parse_txt(file_path):
    """Parse .txt file and return cleaned line list."""
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
        return [line.strip() for line in lines if line.strip()]
    except Exception as e:
        raise ValueError(f"Failed to parse TXT file: {e}")

def parse_uploaded_file(file_path):
    """
    Determine file type by extension and route to the appropriate parser.
    Supports: .xls, .xlsx, .pdf, .txt
    """
    ext = os.path.splitext(file_path)[-1].lower()
    if ext in [".xls", ".xlsx"]:
        return parse_xls(file_path)
    elif ext == ".pdf":
        return parse_pdf(file_path)
    elif ext == ".txt":
        return parse_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
