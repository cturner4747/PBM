import json
import os

def load_bin_map(path="bin_map.json"):
    """Load BIN-to-PBM mapping from a JSON file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"BIN map not found at {path}")
    with open(path, "r") as f:
        return json.load(f)

def get_pbm_info(bin_number, bin_map):
    """Return PBM info for a given BIN number (as a 6-digit string)."""
    bin_str = str(bin_number).replace(".0", "").zfill(6)
    return bin_map.get(bin_str, {
        "pbm": "Unknown",
        "pcns": [],
        "line_of_business": "Unknown",
        "notes": "BIN not recognized in master list"
    })

# Example test (optional)
if __name__ == "__main__":
    bin_map = load_bin_map("bin_map.json")
    test_bin = "610279"
    result = get_pbm_info(test_bin, bin_map)
    print(f"BIN {test_bin} routes to PBM: {result['pbm']}")
