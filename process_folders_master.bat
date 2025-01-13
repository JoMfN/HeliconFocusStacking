@echo off
setlocal enabledelayedexpansion

:: Define paths
SET SCRIPT_DIR=%~dp0
SET PYTHON_SCRIPT="%SCRIPT_DIR%generate_valid_folders.py"
SET PROCESS_BATCH="%SCRIPT_DIR%process_valid_folders.bat"

:: Parse the command-line argument for the input directory
IF "%1"=="-d" (
    SET INPUT_DIR=%2
) ELSE (
    ECHO Usage: %~nx0 -d [input_directory]
    EXIT /B 1
)

:: Validate the input directory
IF NOT EXIST "%INPUT_DIR%" (
    ECHO Error: The specified directory "%INPUT_DIR%" does not exist.
    PAUSE
    EXIT /B 1
)

:: Step 1: Run the Python script to generate folders_to_process.txt
ECHO Running Python script to generate the list of valid folders...
python %PYTHON_SCRIPT% "%INPUT_DIR%"
IF %ERRORLEVEL% NEQ 0 (
    ECHO Error: Failed to generate the list of valid folders.
    PAUSE
    EXIT /B 1
)

:: Step 2: Call the batch script to process the folders
ECHO Processing valid folders with Helicon Focus...
CALL %PROCESS_BATCH% "%INPUT_DIR%"
IF %ERRORLEVEL% NEQ 0 (
    ECHO Error: Processing of folders failed.
    PAUSE
    EXIT /B 1
)

ECHO All tasks completed successfully.
PAUSE
