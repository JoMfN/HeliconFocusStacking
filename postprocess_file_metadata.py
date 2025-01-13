import os
import re
import pandas as pd

# Load folders to process
def load_folders(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

# Parse folder metadata
def parse_folder(folder_name):
    """
    Extract metadata from folder names using a robust regex pattern.
    """
    # Regex pattern to extract metadata
    pattern = r"(?:(.*?)_)?(u_\w+)?__(.*?)__(\w+)?__(.*?)$"
    match = re.search(pattern, folder_name)

    if match:
        collector_or_object = match.group(1) or "Unknown"
        hash_value = match.group(2) or "No Hash"
        species = match.group(3)
        view = match.group(4)
        extra_info = match.group(5)
        return {
            "CollectorOrObject": collector_or_object,
            "Hash": hash_value,
            "Species": species,
            "View": view,
            "ExtraInfo": extra_info,
        }
    else:
        return {
            "CollectorOrObject": "Invalid",
            "Hash": "Invalid",
            "Species": "Invalid",
            "View": "Invalid",
            "ExtraInfo": "Invalid",
        }

# Main function
def process_folders_to_csv(input_file, output_csv):
    folder_list = load_folders(input_file)
    parsed_metadata = []

    for folder in folder_list:
        folder_name = os.path.basename(folder)
        metadata = parse_folder(folder_name)
        metadata["FullPath"] = folder
        parsed_metadata.append(metadata)

    # Convert to DataFrame
    df = pd.DataFrame(parsed_metadata)
    df.to_csv(output_csv, index=False)
    print(f"Metadata saved to {output_csv}")

# Example usage
if __name__ == "__main__":
    input_file = r"G:\RawStackBilder\folders_to_process.txt"
    output_csv = r"G:\RawStackBilder\parsed_metadata.csv"
    process_folders_to_csv(input_file, output_csv)
