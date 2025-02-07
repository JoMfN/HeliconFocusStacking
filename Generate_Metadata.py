import os
import re
import sys
import pandas as pd

# Define regex patterns for folder structures
patterns = [
    r".*?(?P<ObjectCollector>[a-zA-Z0-9_-]+).*?(?P<Hash>[a-z0-9]+)__(?P<SpeciesName>[a-zA-Z_]+)__(?P<ViewType>[a-zA-Z_]+)(?:_.*)?",
    r".*?(?P<Hash>[a-z0-9]+)__(?P<SpeciesName>[a-zA-Z_]+)__(?P<ViewType>[a-zA-Z_]+)(?:_.*)?",
]

# Excluded folders that should not be processed
EXCLUDED_FOLDERS = {"CaptureOne", "Cache", "Proxies", "Settings140", "Thumbnails"}

def format_folder_path(input_dir, folder_path):
    """
    Format the folder path by removing the input directory prefix and replacing backslashes with '__'.
    """
    relative_path = os.path.relpath(folder_path, input_dir)
    formatted_path = relative_path.replace("\\", "__")
    return formatted_path

def parse_folder(folder_name, patterns):
    """
    Parse metadata from a folder name using defined regex patterns.
    """
    for pattern in patterns:
        match = re.search(pattern, folder_name)
        if match:
            metadata = match.groupdict()
            metadata.setdefault("ObjectCollector", "Unknown")
            metadata["FolderPath"] = folder_name
            return metadata
    return None

def generate_metadata(input_dir):
    """
    Generate metadata for all valid folders under the input directory.
    """
    parsed_data = []
    
    for root, dirs, _ in os.walk(input_dir):
        # Filter out excluded folders
        dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERS]
        
        for dir_name in dirs:
            full_path = os.path.join(root, dir_name)
            formatted_folder = format_folder_path(input_dir, full_path)
            metadata = parse_folder(formatted_folder, patterns)
            
            if metadata:
                metadata["FormattedFolderPath"] = formatted_folder
                parsed_data.append(metadata)
    
    # Convert to DataFrame
    folders_df = pd.DataFrame(parsed_data)
    
    if not folders_df.empty:
        # Save metadata to CSV
        output_csv = os.path.join(input_dir, "parsed_folders_metadata.csv")
        folders_df.to_csv(output_csv, index=False)
        print(f"Metadata saved to {output_csv}")
    else:
        print("No valid metadata found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_metadata.py [input_directory]")
        sys.exit(1)

    input_dir = sys.argv[1]

    if not os.path.exists(input_dir):
        print(f"Error: The directory {input_dir} does not exist.")
        sys.exit(1)

    generate_metadata(input_dir)
