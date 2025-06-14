
import streamlit as st
import pandas as pd
import json
import io

# Load PBM template memory
with open("pbm_templates.json", "r") as f:
    pbm_templates = json.load(f)

st.title("🧾 PBM Submission Agent")

# PBM Selection
pbm_choice = st.selectbox("Select PBM", list(pbm_templates.keys()))
template = pbm_templates[pbm_choice]

st.markdown("### 📝 Required Fields")
st.write(template["required_fields"])
st.markdown("**Format Notes:** " + template["format_notes"])

# File Upload
uploaded_file = st.file_uploader("Upload your claim data (.csv or .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    # Read the uploaded file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.markdown("### 📋 Preview of Uploaded Data")
    st.dataframe(df.head())

    # Filter to only required fields (if present)
    required = template["required_fields"]
    filtered_df = df[[col for col in required if col in df.columns]]

    st.markdown("### 📄 Filtered Submission File")
    st.dataframe(filtered_df.head())

    # Download button for the filtered file
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        filtered_df.to_excel(writer, index=False, sheet_name="Submission")
        writer.save()
        st.download_button(
            label="📥 Download Submission File (.xlsx)",
            data=buffer.getvalue(),
            file_name=f"{pbm_choice}_submission.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
