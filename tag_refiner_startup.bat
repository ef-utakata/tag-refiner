@echo off
REM Tag Refiner Startup Script for Obsidian
REM This script activates conda environment and runs tag_refiner.py

echo Starting Tag Refiner...

wsl -e bash -c "source /home/rnishimura/miniconda3/etc/profile.d/conda.sh && conda activate document && cd /mnt/c/Users/endor/Documents/private/private_works/scripts/projects/tag_refiner && if [ -f .env ]; then export $(grep -v '^#' .env | xargs); fi && nohup python tag_refiner.py --provider openai --model o4-mini --input-dir '/mnt/c/Users/endor/Documents/private/Clippings' > tag_processing_startup_$(date +%%Y%%m%%d_%%H%%M%%S).log 2>&1 &"

echo Tag Refiner started in background.