@echo off
setlocal enabledelayedexpansion

:: Define Helicon Focus executable WITH quotes
SET HF_EXE="C:\Program Files\Helicon Software\Helicon Focus 8\HeliconFocus.exe"

:: Locate folders_to_process.txt in the input directory
SET FOLDERS_FILE=%~1\folders_to_process.txt

:: Ensure the folders_to_process.txt exists
IF NOT EXIST "%FOLDERS_FILE%" (
    ECHO Error: %FOLDERS_FILE% not found.
    EXIT /B 1
)

:: Loop through each folder in the list
FOR /F "usebackq delims=" %%G IN ("%FOLDERS_FILE%") DO (
    ECHO Processing folder: %%G

    :: Define the parent directory
    FOR %%P IN ("%%G\..") DO SET PARENT_DIR=%%~fP

    :: Define the output file name in the parent directory
    SET OUTPUT_FILE=!PARENT_DIR!\%%~nG.dng

    :: Run Helicon Focus directly on the folder
    %HF_EXE% -silent "%%G" -save:"!OUTPUT_FILE!" -mp:2 -sp:4 -sort:auto

    :: Check if the process was successful
    IF %ERRORLEVEL% EQU 0 (
        ECHO Successfully processed %%G. Output saved to !OUTPUT_FILE!.
    ) ELSE (
        ECHO Error processing %%G. Check logs or parameters.
    )
)

ECHO All folders processed successfully.
PAUSE
