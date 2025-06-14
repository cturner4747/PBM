import streamlit as st
import pandas as pd
import re
from io import StringIO, BytesIO
import zipfile
from pathlib import Path

st.set_page_config(page_title="PBM Report Formatter", layout="wide")

# PBM mapping by BIN
PBM_MAP = {
    "004336": "Caremark",
    "610502": "Caremark",
    "610014": "PSAO Other",
    "015581": "Express Scripts",
    "017010": "MedImpact",
    "610097": "Mavatis",
}

@st.cache_data
def clean_and_extract(text: str):
    lines = text.splitlines()
    header = None
    clean_lines = []
    for line in lines:
        # Detect header row
        if re.match(r"^Rx[\t,]Patient", line):
            header = line.strip()
            continue
        # Skip metadata and repeated headers
        if not header or line.startswith("West Gate Pharmacy") or line.startswith("Rx Gross Profit Detail"):
            continue
        if line.startswith("Transaction Status") or line.startswith("Page ") or line.startswith("Total"):
            continue
        if line.strip() == header:
            continue
        clean_lines.append(line)
    return header, clean_lines

@st.cache_data
def parse_dataframe(header: str, lines: list[str]):
    delimiter = "\t" if "\t" in header else ","
    csv_data = header + "\n" + "\n".join(lines)
    df = pd.read_csv(StringIO(csv_data), sep=delimiter, dtype=str)
    df = df[df["Rx"].str.strip().str.isnumeric()]
    return df

@st.cache_data
def format_reports(df: pd.DataFrame, base_name: str) -> dict[str, bytes]:
    outputs = {}
    for bin_val, group in df.groupby("BIN"):
        pbm_name = PBM_MAP.get(bin_val.strip(), "PSAO Other")
        out_df = group.reset_index(drop=True)
        buf = BytesIO()
        out_df.to_excel(buf, index=False)
        buf.seek(0)
        filename = f"{Path(base_name).stem}_{pbm_name}.xlsx"
        outputs[filename] = buf.read()
    return outputs

st.title("📦 PBM Report Formatter")
st.markdown("Upload a PioneerRx report (.txt) and get formatted Excel files per PBM bundled in a ZIP.")

uploaded = st.file_uploader("Choose report files", type="txt", accept_multiple_files=True)

if uploaded:
    all_outputs = {}
    for report in uploaded:
        raw = report.read().decode("utf-8", errors="ignore")
        header, lines = clean_and_extract(raw)
        if not header or not lines:
            st.warning(f"No valid data found in {report.name}")
            continue
        df = parse_dataframe(header, lines)
        if df.empty:
            st.warning(f"No Rx rows found in {report.name}")
            continue
        out_files = format_reports(df, report.name)
        all_outputs.update(out_files)
    if all_outputs:
        zip_buf = BytesIO()
        with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zipf:
            for fname, data in all_outputs.items():
                zipf.writestr(fname, data)
        zip_buf.seek(0)
        st.download_button(
            label="📥 Download Formatted Reports as ZIP",
            data=zip_buf,
            file_name="formatted_reports.zip",
            mime="application/zip"
        )
    else:
        st.info("No formatted files generated.")
else:
    st.info("Awaiting report upload…")

