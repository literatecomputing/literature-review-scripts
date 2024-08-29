@echo off
setlocal enabledelayedexpansion

:: Check if the DOI file is passed as a parameter
if "%~1"=="" (
    echo Usage: %~nx0 ^<doiFile^>
    exit /b 1
)

:: Set the DOI file from the command-line parameter
set "doiFile=%~1"

:: Check if the DOI file exists
if not exist "%doiFile%" (
    echo The file %doiFile% does not exist.
    exit /b 1
)

:: Loop through each line in the DOI file
for /f "usebackq delims=" %%a in ("%doiFile%") do (
    set "doi=%%a"
    
    :: Replace '/' with '-' to create the output filename
    set "outputFile=!doi:/=-!.pdf"

    :: Check if the output file already exists
    if exist "!outputFile!" (
        echo Skipping !doi!, file already exists: !outputFile!
    ) else (
        :: Run the curl command
        curl https://www.tandfonline.com/doi/pdf/!doi!?download=true --output "!outputFile!"
        
        :: Echo the command for verification (optional)
        echo Downloaded !doi! to !outputFile!
    )
)

echo Done!
exit /b 0
