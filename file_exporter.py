
import zipfile
import io
import pandas as pd
import os

def package_files_as_zip(file_dict):
    """
    Handles a mix of DataFrames and already-exported file paths (e.g., .xlsx).
    Returns zip as BytesIO.
    """
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
        for filename, file_obj in file_dict.items():
            if isinstance(file_obj, pd.DataFrame):
                z.writestr(filename, file_obj.to_csv(index=False))
            elif isinstance(file_obj, str) and os.path.isfile(file_obj):
                with open(file_obj, "rb") as f:
                    z.writestr(filename, f.read())
            else:
                raise ValueError(f"Unsupported file type or missing file: {filename}")
    buffer.seek(0)
    return buffer
