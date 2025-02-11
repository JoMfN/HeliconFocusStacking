import os
import re
import sys
import pandas as pd

# Define excluded folders that should not be processed
EXCLUDED_FOLDERS = {"CaptureOne", "Cache", "Proxies", "Settings140", "Thumbnails"}

# Improved regex pattern to dynamically extract metadata from folder names
PATTERN = re.compile(r"([a-zA-Z0-9_-]+)")

def format_folder_path(input_dir, folder_path):
    """
    Formats the folder path by:
    - Removing the input directory prefix
    - Replacing backslashes with '__'
    - Removing known excluded folders
    """
    relative_path = os.path.relpath(folder_path, input_dir)
    formatted_path = relative_path.replace("\\", "__")

    # Exclude folders in the EXCLUDED_FOLDERS list
    for excluded in EXCLUDED_FOLDERS:
        if f"__{excluded}__" in formatted_path or formatted_path.endswith(f"__{excluded}"):
            return None  # Skip processing

    return formatted_path

def parse_folder(folder_name):
    """
    Extracts metadata dynamically from formatted folder paths.
    """
    metadata = {
        "ObjectCollector": "Unknown",
        "Hash": "No Hash",
        "SpeciesName": "Unknown",
        "ViewType": "Unknown",
        "ExtraInfo": ""
    }

    # Split folder name into meaningful segments
    parts = folder_name.split("__")
    extracted_values = []

    for part in parts:
        match = PATTERN.fullmatch(part)
        if match:
            extracted_values.append(match.group(1))

    # Assign metadata dynamically based on extracted values
    if len(extracted_values) >= 4:
        metadata["ObjectCollector"] = extracted_values[0]
        metadata["Hash"] = extracted_values[1]
        metadata["SpeciesName"] = extracted_values[2]
        metadata["ViewType"] = extracted_values[3]
        if len(extracted_values) > 4:
            metadata["ExtraInfo"] = "__".join(extracted_values[4:])
    elif len(extracted_values) == 3:
        metadata["ObjectCollector"] = "Unknown"
        metadata["Hash"] = extracted_values[0]
        metadata["SpeciesName"] = extracted_values[1]
        metadata["ViewType"] = extracted_values[2]
    elif len(extracted_values) == 2:
        metadata["ObjectCollector"] = "Unknown"
        metadata["Hash"] = "No Hash"
        metadata["SpeciesName"] = extracted_values[0]
        metadata["ViewType"] = extracted_values[1]

    return metadata

def generate_metadata(input_dir):
    """
    Generates metadata from all valid folders listed in `folders_to_process.txt`.
    """
    folders_file = os.path.join(input_dir, "folders_to_process.txt")

    if not os.path.exists(folders_file):
        print(f"Error: {folders_file} not found.")
        return

    with open(folders_file, 'r') as f:
        folder_paths = [line.strip() for line in f]

    parsed_data = []
    for folder in folder_paths:
        formatted_path = format_folder_path(input_dir, folder)
        if formatted_path:
            metadata = parse_folder(formatted_path)
            metadata["FormattedFolderPath"] = formatted_path
            parsed_data.append(metadata)

    # Convert to DataFrame
    folders_df = pd.DataFrame(parsed_data)

    # Save metadata to CSV
    output_csv = os.path.join(input_dir, "parsed_folders_metadata.csv")
    folders_df.to_csv(output_csv, index=False)
    print(f"Metadata saved to {output_csv}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_metadata.py [input_directory]")
        sys.exit(1)

    input_dir = sys.argv[1]

    if not os.path.exists(input_dir):
        print(f"Error: The directory {input_dir} does not exist.")
        sys.exit(1)

    generate_metadata(input_dir)
