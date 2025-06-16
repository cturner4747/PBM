
import zipfile
import io

def package_files_as_zip(file_dict):
    """
    Takes a dictionary of {filename: DataFrame}, returns zip bytes.
    """
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
        for filename, df in file_dict.items():
            z.writestr(filename, df.to_csv(index=False))
    buffer.seek(0)
    return buffer
