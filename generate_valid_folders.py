import os
import sys

# Constants for folder exclusions
EXCLUDED_FOLDERS = {"$Recycle.Bin", "System Volume Information", "CaptureOne"}

def is_valid_folder(folder_path):
    """
    Check if a folder is valid for processing.
    A folder is valid if:
    - It contains at least 2 .ARW files.
    - It does not contain "label" in any .ARW file names.
    - It is not in the excluded folders list.
    """
    folder_name = os.path.basename(folder_path)

    # Skip excluded folders
    if folder_name in EXCLUDED_FOLDERS:
        print(f"Skipping folder: {folder_path} (Excluded folder)")
        return False

    # Get all .ARW files in the folder
    arw_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.arw')]

    # Skip folders with fewer than 2 .ARW files
    if len(arw_files) < 2:
        print(f"Skipping folder: {folder_path} (Only {len(arw_files)} .ARW file(s))")
        return False

    # Skip folders with .ARW files containing "label" in the name
    if any("label" in f.lower() for f in arw_files):
        print(f"Skipping folder: {folder_path} (Contains 'label' in file name)")
        return False

    return True


def generate_valid_folders(input_dir):
    """
    Generate a list of valid folders and save it to `folders_to_process.txt` in the input directory.
    """
    valid_folders = []

    # Walk through all folders in the input directory
    for root, dirs, files in os.walk(input_dir):
        if is_valid_folder(root):
            valid_folders.append(root)

    # Define output file path
    output_file = os.path.join(input_dir, "folders_to_process.txt")

    # Save valid folders to the output file
    with open(output_file, 'w') as f:
        for folder in valid_folders:
            f.write(folder + '\n')

    print(f"Valid folders saved to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_valid_folders.py [input_directory]")
        sys.exit(1)

    input_dir = sys.argv[1]

    # Check if the input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: The directory {input_dir} does not exist.")
        sys.exit(1)

    generate_valid_folders(input_dir)
