import pandas as pd
import os
import re
import csv
from PyPDF2 import PdfReader

def parse_xls(file_path):
    # Placeholder for XLS parsing (handled elsewhere)
    raise NotImplementedError("XLS parser not shown here.")

def parse_pdf(file_path):
    """Parse PDF and extract NDC-like lines into a list."""
    try:
        reader = PdfReader(file_path)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        rows = [line.strip() for line in text.split("\n") if line.strip()]
        data = []
        for line in rows:
            if re.search(r"\d{5}-\d{4}-\d{2}", line):  # crude NDC match
                data.append(line)
        return data
    except Exception as e:
        raise ValueError(f"Failed to parse PDF file: {e}")

def parse_txt(file_path):
    """
    Auto-detect header row, parse .txt as CSV from that point forward,
    and return as a structured pandas DataFrame.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        header_row_index = None
        for i, line in enumerate(lines):
            if line.lower().startswith("rx,") or "rx,patient" in line.lower():
                header_row_index = i
                break

        if header_row_index is None:
            raise ValueError("Could not locate header row in .txt file.")

        csv_lines = lines[header_row_index:]
        reader = csv.reader(csv_lines)
        records = list(reader)

        df = pd.DataFrame(records[1:], columns=[col.strip() for col in records[0]])
        df = df.dropna(axis=0, how='all')

        # Normalize column name for routing
        df.rename(columns={col: "BIN" for col in df.columns if "bin" in col.lower()}, inplace=True)

        return df

    except Exception as e:
        raise ValueError(f"Failed to parse TXT file: {e}")

def parse_uploaded_file(file_path):
    """Route to the correct parser based on file extension."""
    ext = os.path.splitext(file_path)[-1].lower()
    if ext in [".xls", ".xlsx"]:
        return parse_xls(file_path)
    elif ext == ".pdf":
        return parse_pdf(file_path)
    elif ext == ".txt":
        return parse_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

