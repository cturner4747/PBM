
import pandas as pd
import os
from optum_formatter import generate_optumrx_excel

OPTUM_BINS = {"610279", "610127", "610494", "610502", "610611", "610014"}  # Expandable list

def format_for_submission(df):
    """
    Organizes claims by PBM and formats OptumRx BINs into .xlsx template files.
    Returns: dict of {filename: DataFrame or file bytes}
    """
    if "BIN" not in df.columns:
        raise ValueError("BIN column missing from data.")

    output_files = {}

    for bin_value, group in df.groupby("BIN"):
        bin_str = str(bin_value).zfill(6)
        pbm_name = get_pbm_name_from_bin(bin_str)

        if bin_str in OPTUM_BINS:
            filename = f"{pbm_name}_{bin_str}.xlsx"
            temp_path = f"/tmp/{filename}"
            generate_optumrx_excel("OptumRx_MAC_Appeal_FINAL.xlsx", group, temp_path)
            output_files[filename] = temp_path  # File path to be opened into ZIP later
        else:
            filename = f"{pbm_name}_{bin_str}.csv"
            output_files[filename] = group.reset_index(drop=True)

    return output_files

def get_pbm_name_from_bin(bin_number):
    bin_lookup = {
        "610279": "OptumRx",
        "610127": "OptumRx",
        "610494": "OptumRx",
        "610502": "Aetna",
        "004336": "Caremark",
        "003858": "Ambetter",
        "610014": "ExpressScripts"
    }
    return bin_lookup.get(bin_number.zfill(6), "Unknown_PBM")
