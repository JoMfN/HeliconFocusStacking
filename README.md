# Helicon Focus Batch Processing Workflow

This repository provides an automated workflow for batch processing focus stacking tasks using **Helicon Focus** software. It also includes scripts to parse metadata from folder structures and save it for downstream processing.

---

## Workflow Overview

1. **Folder Validation**:
   - Python script identifies valid folders containing `.ARW` files.
   - It excludes invalid folders (e.g., those with `CaptureOne` subdirectories).

2. **Batch Processing**:
   - A `.bat` script processes valid folders, generating `.dng` stacked images.
   - Each `.dng` file is saved at the parent folder level with a robust name.

3. **Metadata Extraction**:
   - A second Python script extracts metadata from processed folders and saves it to a CSV file.
   - Metadata includes:
     - Collection object or photographer.
     - Hash value (if available).
     - Species name.
     - View type (e.g., dorsal, lateral).
     - Extra details (e.g., magnification).

---

## Repository Structure

|-- generate_valid_folders.py # Validates folders and generates folders_to_process.txt |-- process_folders_master.bat # Master batch script orchestrating Python and .bat scripts |-- process_valid_folders.bat # Processes folders using Helicon Focus |-- postprocess_file_metadata.py # Parses metadata from processed folders |-- folders_to_process.txt # List of valid folders (generated) |-- parsed_metadata.csv # Final metadata in tabular format (output)


Based on your input and the detailed examination of folder structures, filenames, and requirements, here's an improved workflow and updated Python script for handling metadata extraction and saving DNG files with robust naming conventions. Additionally, I'll provide a README.md to explain the entire workflow.

Python Script for Metadata Parsing and Tabularization
This script:

Processes folder names from folders_to_process.txt.
Extracts metadata such as collection object, collector, species, and view type.
Saves parsed metadata into a structured CSV file.
Handles complex folder names (e.g., coll.mfn-berlin.de_u_09f74e__Polydesmus_python__dorsal_90mm_1zu3).
postprocess_file_metadata.py
python
Copy code
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
README.md for GitHub Repository
markdown
Copy code
# Helicon Focus Batch Processing Workflow

This repository provides an automated workflow for batch processing focus stacking tasks using **Helicon Focus** software. It also includes scripts to parse metadata from folder structures and save it for downstream processing.

---

## Workflow Overview

1. **Folder Validation**:
   - Python script identifies valid folders containing `.ARW` files.
   - It excludes invalid folders (e.g., those with `CaptureOne` subdirectories).

2. **Batch Processing**:
   - A `.bat` script processes valid folders, generating `.dng` stacked images.
   - Each `.dng` file is saved at the parent folder level with a robust name.

3. **Metadata Extraction**:
   - A second Python script extracts metadata from processed folders and saves it to a CSV file.
   - Metadata includes:
     - Collection object or photographer.
     - Hash value (if available).
     - Species name.
     - View type (e.g., dorsal, lateral).
     - Extra details (e.g., magnification).

---

## Repository Structure

|-- generate_valid_folders.py # Validates folders and generates folders_to_process.txt |-- process_folders_master.bat # Master batch script orchestrating Python and .bat scripts |-- process_valid_folders.bat # Processes folders using Helicon Focus |-- postprocess_file_metadata.py # Parses metadata from processed folders |-- folders_to_process.txt # List of valid folders (generated) |-- parsed_metadata.csv # Final metadata in tabular format (output)

---

## Usage

### Setup

Install "HeliconFocus" and the "Adobe DNG Converter" plugin from the [Helicon Soft website][https://www.heliconsoft.com/software-downloads/]

### Step 1 (only first time): 
Activate the licence with a valid licence key for the software.

```powershell
LICENSE_KEY=12345678                                                              :: Replace with your activation key
HF_EXE="C:\Program Files\Helicon Software\Helicon Focus 8\HeliconFocus.exe"       :: Define path to Helicon Focus executable and main directory containing subfolders
%HF_EXE% --activationCode %LICENSE_KEY% --register-global
```


Step 2: generate valid folders to batch process them for Focus stacking within the .ARW images in those folders.

Run the following command to generate a `folders_to_process.txt` file within the [INPUT_DIR] :

```powershell
process_folders_master.bat -d [INPUT_DIR]
```
[INPUT_DIR]: Root directory containing subfolders with .ARW files.

Helicon Focus processes the folders listed in folders_to_process.txt. Output .dng files are saved in the parent folder.

Step 3: Extract Metadata (Unfinished)
Run the postprocess_file_metadata.py script to parse folder metadata:

```bash
python postprocess_file_metadata.py
```


