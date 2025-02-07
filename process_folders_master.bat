@echo off
setlocal enabledelayedexpansion

:: Define paths
SET SCRIPT_DIR=%~dp0
SET PYTHON_SCRIPT_GENERATE_FOLDERS="%SCRIPT_DIR%generate_valid_folders.py"
SET PYTHON_SCRIPT_GENERATE_METADATA="%SCRIPT_DIR%Generate_Metadata.py"
SET PROCESS_BATCH="%SCRIPT_DIR%process_valid_folders.bat"

:: Parse command-line arguments
IF "%1"=="-d" (
    SET INPUT_DIR=%2
    SET PROCESS_MODE=%4
) ELSE (
    ECHO Usage: %~nx0 -d [input_directory] -t [all|keep]
    EXIT /B 1
)

IF NOT DEFINED PROCESS_MODE (
    SET PROCESS_MODE=all
)

:: Validate the input directory
IF NOT EXIST "%INPUT_DIR%" (
    ECHO Error: The specified directory "%INPUT_DIR%" does not exist.
    PAUSE
    EXIT /B 1
)

:: Step 1: Generate valid folders list
ECHO Running Python script to generate the list of valid folders...
python %PYTHON_SCRIPT_GENERATE_FOLDERS% "%INPUT_DIR%" -t "%PROCESS_MODE%"
IF %ERRORLEVEL% NEQ 0 (
    ECHO Error: Failed to generate the list of valid folders.
    PAUSE
    EXIT /B 1
)

:: Step 2: Generate metadata from folder paths
ECHO Generating metadata for valid folders...
python %PYTHON_SCRIPT_GENERATE_METADATA% "%INPUT_DIR%"
IF %ERRORLEVEL% NEQ 0 (
    ECHO Error: Failed to generate metadata.
    PAUSE
    EXIT /B 1
)

:: Step 3: Process folders with Helicon Focus
ECHO Processing valid folders with Helicon Focus...
CALL %PROCESS_BATCH% "%INPUT_DIR%" -t "%PROCESS_MODE%"
IF %ERRORLEVEL% NEQ 0 (
    ECHO Error: Processing of folders failed.
    PAUSE
    EXIT /B 1
)

ECHO All tasks completed successfully.
PAUSE
