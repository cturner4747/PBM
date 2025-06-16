
import pandas as pd
import os

def format_for_submission(df):
    """
    Organizes claims into PBM-specific CSVs based on BIN and prepares file content.
    Returns a dictionary: {filename: DataFrame}
    """
    if "BIN" not in df.columns:
        raise ValueError("BIN column missing from data.")

    output_files = {}

    for bin_value, group in df.groupby("BIN"):
        pbm_name = get_pbm_name_from_bin(str(bin_value))
        filename = f"{pbm_name.replace(' ', '_')}_{bin_value}.csv"
        output_files[filename] = group.reset_index(drop=True)

    return output_files

def get_pbm_name_from_bin(bin_number):
    """
    Simple mapping for demo; should be replaced by lookup from bin_map.json.
    """
    bin_lookup = {
        "610279": "OptumRx",
        "610127": "OptumRx",
        "004336": "Caremark",
        "610494": "OptumRx",
        "003858": "Ambetter",
        "610502": "Aetna",
        "610014": "ExpressScripts"
    }
    return bin_lookup.get(bin_number.zfill(6), "Unknown_PBM")
