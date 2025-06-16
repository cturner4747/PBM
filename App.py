import streamlit as st
import os
import pandas as pd
from file_parser import parse_uploaded_file
from bin_router import load_bin_map, get_pbm_info

st.set_page_config(page_title="PBM Appeal Submission Assistant", layout="wide")
st.title("📤 PBM Appeal Submission Assistant")

st.markdown("Upload your underpaid claims file in `.txt`, `.xls`, `.xlsx`, or `.pdf` format:")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "xls", "xlsx", "pdf"])

if uploaded_file:
    file_ext = uploaded_file.name.split('.')[-1]
    temp_path = os.path.join("temp_upload." + file_ext)

    # Save uploaded file locally
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    # Attempt to parse the uploaded file
    try:
        parsed_data = parse_uploaded_file(temp_path)
        st.success("✅ File successfully parsed.")
    except Exception as e:
        st.error(f"❌ Parsing failed: {e}")
        st.stop()

    # Display preview
    st.markdown("### 🧾 Parsed Data Preview")
    if isinstance(parsed_data, pd.DataFrame):
        st.dataframe(parsed_data.head(20))
    else:
        st.code("\n".join(parsed_data[:20]), language="text")

    # Load BIN-to-PBM mapping
    try:
        bin_map = load_bin_map("bin_map.json")
    except Exception as e:
        st.error(f"❌ Failed to load BIN mapping: {e}")
        st.stop()

    # BIN Routing Preview
    st.markdown("### 🧠 BIN Routing Preview")
    bin_column_name = next((col for col in parsed_data.columns if "bin" in str(col).lower()), None)

    if bin_column_name:
        preview = parsed_data.dropna(subset=[bin_column_name]).head(5)
        for i, row in preview.iterrows():
            bin_val = row[bin_column_name]
            pbm_info = get_pbm_info(bin_val, bin_map)
            st.markdown(f"- BIN `{bin_val}` ➜ **{pbm_info['pbm']}** — {pbm_info['line_of_business']}")
    else:
        st.info("No BIN column detected or file type does not support preview.")

