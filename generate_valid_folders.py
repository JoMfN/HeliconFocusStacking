import os
import sys
import re

# Constants for folder exclusions
EXCLUDED_FOLDERS = {"$Recycle.Bin", "System Volume Information", "CaptureOne"}

# Mapping of special characters to ASCII-compatible replacements
CHAR_REPLACEMENTS = {
    "ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss",
    "Ä": "Ae", "Ö": "Oe", "Ü": "Ue"
}

def sanitize_folder_name(folder_name):
    """Replace special characters in folder names with ASCII-compatible equivalents."""
    for char, replacement in CHAR_REPLACEMENTS.items():
        folder_name = folder_name.replace(char, replacement)
    return folder_name.replace(".", "_")  # Ensure dots are replaced with underscores

def rename_folder_if_needed(folder_path):
    """Rename a folder if it contains special characters."""
    parent_dir = os.path.dirname(folder_path)
    original_name = os.path.basename(folder_path)
    sanitized_name = sanitize_folder_name(original_name)

    if original_name != sanitized_name:
        new_path = os.path.join(parent_dir, sanitized_name)

        # Ensure a unique name (avoid overwriting)
        counter = 1
        while os.path.exists(new_path):
            new_path = os.path.join(parent_dir, f"{sanitized_name}_{counter}")
            counter += 1

        os.rename(folder_path, new_path)
        print(f"Renamed: {original_name} -> {sanitized_name}")
        return new_path
    return folder_path

def is_valid_folder(folder_path):
    """Check if a folder is valid for processing (contains >=2 ARW files, not excluded)."""
    if os.path.basename(folder_path) in EXCLUDED_FOLDERS:
        return False

    arw_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.arw')]
    return len(arw_files) >= 2 and not any("label" in f.lower() for f in arw_files)

def has_existing_dng(folder_path):
    """Check if a `.dng` file already exists in the parent directory."""
    parent_dir = os.path.dirname(folder_path)
    return any(f.lower().endswith('.dng') for f in os.listdir(parent_dir))

def generate_valid_folders(input_dir, process_mode="all"):
    """Generate a list of valid folders and save it to `folders_to_process.txt`."""
    valid_folders = []

    for root, dirs, _ in os.walk(input_dir, topdown=True):
        sanitized_root = rename_folder_if_needed(root)
        if is_valid_folder(sanitized_root):
            if process_mode == "keep" and has_existing_dng(sanitized_root):
                print(f"Skipping (DNG exists): {sanitized_root}")
                continue
            valid_folders.append(sanitized_root)

    output_file = os.path.join(input_dir, "folders_to_process.txt")

    # Handle existing backup files safely
    backup_file = output_file + ".backup"
    if os.path.exists(backup_file):
        counter = 1
        while os.path.exists(f"{backup_file}.{counter}"):
            counter += 1
        backup_file = f"{backup_file}.{counter}"

    if os.path.exists(output_file):
        os.rename(output_file, backup_file)
        print(f"Backup created: {backup_file}")

    # Write valid folders to the output file
    with open(output_file, 'w') as f:
        for folder in valid_folders:
            f.write(folder + '\n')

    print(f"Valid folders saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_valid_folders.py [input_directory] -t [all|keep]")
        sys.exit(1)

    input_dir = sys.argv[1]
    process_mode = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "-t" else "all"

    if not os.path.exists(input_dir):
        print(f"Error: The directory {input_dir} does not exist.")
        sys.exit(1)

    generate_valid_folders(input_dir, process_mode)
