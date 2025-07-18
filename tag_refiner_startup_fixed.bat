@echo off
REM Tag Refiner Startup Script for Obsidian (Fixed Version)
REM This script ensures proper logging and execution

echo Starting Tag Refiner (Fixed Version)...
echo Current time: %DATE% %TIME%

REM Generate log filename with current timestamp
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do (
    set datestr=%%c%%a%%b
)
for /f "tokens=1-2 delims=: " %%a in ('time /t') do (
    set timestr=%%a%%b
)
set logfile=tag_processing_startup_%datestr%_%timestr%.log

echo Log file: %logfile%

REM Run with improved logging
wsl -e bash -c "cd /mnt/c/Users/endor/Documents/private/private_works/scripts/projects/tag_refiner && source /home/rnishimura/miniconda3/etc/profile.d/conda.sh && conda activate document && if [ -f .env ]; then export $(grep -v '^#' .env | xargs); fi && python tag_refiner.py --provider openai --model o4-mini --input-dir '/mnt/c/Users/endor/Documents/private/Clippings' > %logfile% 2>&1"

if %ERRORLEVEL% EQU 0 (
    echo SUCCESS: Tag Refiner completed successfully
    echo Check log file: %logfile%
) else (
    echo ERROR: Tag Refiner failed with exit code %ERRORLEVEL%
)

echo Completed at: %DATE% %TIME%