import pandas as pd
import os
import re
from PyPDF2 import PdfReader

def parse_xls(file_path):
    """Automatically detect header row and parse .xls or .xlsx files."""
    try:
        # Load file without headers to scan for header row
        raw_df = pd.read_excel(file_path, header=None)
        header_row = None
        target_headers = ["rx", "bin", "ndc", "patient", "drug name"]

        # Scan first 20 rows to find the header row
        for i in range(min(20, len(raw_df))):
            row = raw_df.iloc[i].astype(str).str.lower().str.strip()
            if any(header in row.tolist() for header in target_headers):
                header_row = i
                break

        if header_row is None:
            raise ValueError("No suitable header row found in XLS/XLSX.")

        # Reload using the detected header row
        df = pd.read_excel(file_path, header=header_row)
        df.columns = [str(col).strip() for col in df.columns]  # Clean headers
        df = df.dropna(axis=0, how='all')  # Drop fully empty rows

        return df

    except Exception as e:
        raise ValueError(f"Failed to parse XLS/XLSX file: {e}")

def parse_pdf(file_path):
    """Extract lines with NDC-like content from PDF."""
    try:
        reader = PdfReader(file_path)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        rows = [line.strip() for line in text.split("\n") if line.strip()]
        data = []
        for line in rows:
            if re.search(r"\d{5}-\d{4}-\d{2}", line):
                data.append(line)
        return data
    except Exception as e:
        raise ValueError(f"Failed to parse PDF file: {e}")

def parse_txt(file_path):
    """Read and return clean lines from TXT file."""
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
        return [line.strip() for line in lines if line.strip()]
    except Exception as e:
        raise ValueError(f"Failed to parse TXT file: {e}")

def parse_uploaded_file(file_path):
    """
    Determines file type and routes to appropriate parser.
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

