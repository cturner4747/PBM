import pandas as pd
import os
import re
from PyPDF2 import PdfReader

def parse_xls(file_path):
    """Auto-detect header row from rows 3–7, and parse data starting from row 8."""
    try:
        raw_df = pd.read_excel(file_path, header=None)
        header_row = None
        target_keywords = ["rx", "bin", "ndc", "patient", "drug name"]

        # Scan rows 3 through 7 for the actual header row
        for i in range(3, 8):
            row = raw_df.iloc[i].astype(str).str.lower().str.strip()
            if any(keyword in row.tolist() for keyword in target_keywords):
                header_row = i
                break

        if header_row is None:
            raise ValueError("No header row found between rows 3–7.")

        # Re-read file using detected header row and skip to data row 8
        df = pd.read_excel(file_path, header=header_row, skiprows=range(header_row + 1, 8))
        df.columns = [str(col).strip() for col in df.columns]

        # Normalize BIN column name
        df.rename(columns={col: "BIN" for col in df.columns if "bin" in col.lower()}, inplace=True)

        # Drop empty rows
        df = df.dropna(axis=0, how='all')
        return df

    except Exception as e:
        raise ValueError(f"Failed to parse XLS/XLSX file: {e}")

def parse_pdf(file_path):
    """Parse PDF and return lines containing NDC-like values."""
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
    """Parse plain .txt file line-by-line."""
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
        return [line.strip() for line in lines if line.strip()]
    except Exception as e:
        raise ValueError(f"Failed to parse TXT file: {e}")

def parse_uploaded_file(file_path):
    """Auto-route to appropriate parser based on file extension."""
    ext = os.path.splitext(file_path)[-1].lower()
    if ext in [".xls", ".xlsx"]:
        return parse_xls(file_path)
    elif ext == ".pdf":
        return parse_pdf(file_path)
    elif ext == ".txt":
        return parse_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


