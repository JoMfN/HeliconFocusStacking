### HeliconFocusCLI.md

# Helicon Focus Command Line Interface (CLI) Guide

Helicon Focus can be executed from the command line, allowing for automation and integration with other software workflows. This guide provides an overview of the available command-line parameters and examples for usage.

---

## **Command Line Parameters**

### **General Parameters**
| Parameter                              | Description                                                                 |
|----------------------------------------|-----------------------------------------------------------------------------|
| `-silent`                              | Starts Helicon Focus without the interface, with console output only.       |
| `--activationCode <code>`              | Registers the license automatically using the specified activation code.    |
| `--register-global`                    | Registers the license for all users on this computer (requires admin rights).|

---

### **Output Parameters**
| Parameter                              | Description                                                                 |
|----------------------------------------|-----------------------------------------------------------------------------|
| `-save:<full_name.ext>`                | Saves the result to `full_name.ext`. If omitted, the result is saved to the `Focused` subfolder. |
| `-j:<jpeg_quality>`                    | Sets JPEG quality (0-100).                                                  |
| `-dmap`                                | Saves the depth map image.                                                  |
| `-noresult`                            | Prevents saving the resulting image.                                        |
| `-3d`                                  | Saves a 3D model in Helicon 3D Viewer file format.                          |
| `--preferred-output-path <folder>`     | Sets the default folder to be opened when saving outputs.                   |
| `-tif:<x>`                             | Specifies TIFF compression: `'lzw'` for LZW compression or `'u'` for no compression. Example: `-tif:u`. |

---

### **Input Parameters**
| Parameter                              | Description                                                                 |
|----------------------------------------|-----------------------------------------------------------------------------|
| `-i <full_name.ext>`                   | Specifies a text file (`full_name.ext`) containing a list of input file names separated by a new line. |
| `-o <full_name.ext>`                   | Specifies a text file (`full_name.ext`) to store the list of saved output file names. |

---

### **Processing Parameters**
| Parameter                              | Description                                                                 |
|----------------------------------------|-----------------------------------------------------------------------------|
| `-mp:<x>`                              | Sets the method for focus stacking: `0`=Method A, `1`=Method B, `2`=Method C. |
| `-rp:<xxx>`                            | Sets the Radius.                                                           |
| `-sp:<xxx>`                            | Sets the Smoothing level.                                                  |
| `-sort:<order>`                        | Specifies the sorting order: `asc` for ascending, `desc` for descending, `auto` for automatic. |
| `-va:<xxx>`                            | Sets Vertical shift adjustment.                                            |
| `-ha:<xxx>`                            | Sets Horizontal shift adjustment.                                          |
| `-ra:<xxx>`                            | Sets Rotation adjustment.                                                  |
| `-ma:<xxx>`                            | Sets Magnification adjustment.                                             |
| `-ba:<xxx>`                            | Sets Brightness adjustment.                                                |
| `-im:<x>`                              | Sets the Interpolation method (`1`=Bilinear, etc.).                        |
| `-dmf:<xx>`                            | Sets Depth Map Feathering.                                                 |

---

## **Examples**

### **Basic Usage**
1. Process all images in a folder using default parameters:
   ```bash
   HeliconFocus.exe -silent "c:\my images\set20"
   ```

2. Process all images in the current folder and save the result to the `Focused` subfolder:
   ```bash
   "C:\Program Files\Helicon Focus\HeliconFocus.exe" -silent .
   ```

### **Custom Parameters**
1. Process images with specified radius, smoothing, and method:
   ```bash
   HeliconFocus.exe -silent "c:\my images\set20" -rp:6 -sp:7 -mp:1
   ```

2. Process images in a folder and save the result as a TIFF file:
   ```bash
   HeliconFocus.exe -silent "c:\my images\set20" -save:c:\result.tiff
   ```

3. Process images, save a depth map, and do not save the final result:
   ```bash
   HeliconFocus.exe -silent "c:\my images\set20" -dmap -noresult
   ```

---

## **Usage Notes**
- **Path Formatting**: Always use double quotes (`"`) around file and folder paths to handle spaces in names.
- **License Activation**: Ensure Helicon Focus is properly licensed before using command-line functionality.
- **Compatibility**: Verify that input files are supported by Helicon Focus (e.g., RAW formats like `.ARW`).

For detailed documentation, visit the [Helicon Focus User Guide](https://www.heliconsoft.com/focus/help/english/HeliconFocus.html#HF_Raw_PROCESS).
