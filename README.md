# Helicon Focus Batch Processing Workflow

This repository provides an automated workflow for batch processing focus stacking tasks using **Helicon Focus** software. It also includes scripts to parse metadata from folder structures and save it for downstream processing.


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
```
|-- *\[INPUT_DIR]\[Folder_With_ARW]\*.ARW
|-- generate_valid_folders.py # Validates folders and generates folders_to_process.txt 
|-- process_folders_master.bat # Master batch script orchestrating Python and .bat scripts 
|-- process_valid_folders.bat # Processes folders using Helicon Focus 
|-- postprocess_file_metadata.py # Parses metadata from processed folders (Unfinished)
|-- *\[INPUT_DIR]\folders_to_process.txt # List of valid folders (generated) 
|-- *\[INPUT_DIR]\parsed_metadata.csv # Final metadata in tabular format (output)

---
```

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

### Step 2: generate valid folders to batch process them for Focus stacking within the .ARW images in those folders.

#### Step 2.1: generate valid folders

Run the following command to generate a `folders_to_process.txt` file within the [INPUT_DIR] :

```powershell
process_folders_master.bat -d [INPUT_DIR] -t [all|keep]
```
[INPUT_DIR]: Root directory containing subfolders with .ARW files.
[all|keep]: a flagg to determine if all valid folders need to be stacked or just the ones without a `.dng` stacked image in their parent folder (default is `all`)

### **Example Directory Structure**

#### **Before Running the Script**

```
C:\path_to_images
├── Folder1
│   ├── file1.ARW
│   ├── file2_label.ARW
├── Folder2
│   ├── file3.ARW
│   ├── file4.ARW
│   └── SubFolder1
│       ├── file5.ARW
│       └── file6.ARW
├── CaptureOne
│   ├── file7.ARW
│   └── file8.ARW
```

#### **After Running the Script**
**Content of `folders_to_process.txt`:**
```
C:\path_to_images\Folder2
C:\path_to_images\Folder2\SubFolder1
```

#### Step 2.2: to batch process them for Focus stacking within the .ARW images in those folders.

Helicon Focus processes the folders listed in folders_to_process.txt. Output .dng files are saved in the parent folder.

### **Example Directory Structure**

**Before Processing**:
```
C:\path_to_images
├── Folder1
│   ├── Image1.ARW
│   ├── Image2.ARW
│   └── Image3.ARW
├── Folder2
│   ├── Image1.ARW
│   └── Image2.ARW
├── folders_to_process.txt
```

**After Processing**:
```
C:\path_to_images
├── Folder1
│   ├── Image1.ARW
│   ├── Image2.ARW
│   ├── Image3.ARW
│   └── Folder1.dng
├── Folder2
│   ├── Image1.ARW
│   ├── Image2.ARW
│   └── Folder2.dng
├── folders_to_process.txt
```

### Step 3: Extract Metadata (Unfinished)
Run the postprocess_file_metadata.py script to parse folder metadata:

```bash
python postprocess_file_metadata.py
```


