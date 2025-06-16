
import pandas as pd
from openpyxl import load_workbook

def generate_optumrx_excel(template_path, claims_df, output_path, ncpdp_override=None):
    """
    Populates the official OptumRx MAC Appeal Excel template with claims data.
    """
    wb = load_workbook(template_path)
    ws = wb.active

    start_row = 12  # Row where data entry begins

    for idx, (_, row) in enumerate(claims_df.iterrows()):
        r = start_row + idx
        ws[f"A{r}"] = str(row.get("BIN", "")).zfill(6)
        ws[f"B{r}"] = row.get("PCN", "")
        ws[f"C{r}"] = ""  # Carrier ID – leave blank
        ws[f"D{r}"] = str(ncpdp_override).zfill(7) if ncpdp_override else ""  # NCPDP ID
        ws[f"E{r}"] = str(row.get("Rx", ""))
        ws[f"F{r}"] = pd.to_datetime(row.get("Fill Date", "")).strftime("%m/%d/%Y") if pd.notna(row.get("Fill Date")) else ""
        ws[f"G{r}"] = str(row.get("Dispensed NDC", "")).replace("-", "").zfill(11)[:11]
        ws[f"H{r}"] = "N"  # Compound: default to N
        ws[f"I{r}"] = "MAC Unit is below cost"  # Reason
        ws[f"J{r}"] = ""  # Notes
        ws[f"K{r}"] = row.get("Invoice Cost", "")
        ws[f"M{r}"] = row.get("TP Remit", "")
        ws[f"O{r}"] = row.get("Drug Name", "")
        ws[f"Q{r}"] = ""  # Attestation

    wb.save(output_path)
    return output_path
