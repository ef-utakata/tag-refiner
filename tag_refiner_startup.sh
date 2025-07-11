#!/bin/bash
# Tag Refiner Startup Script

# Initialize conda
source /home/rnishimura/miniconda3/etc/profile.d/conda.sh

# Activate the document environment
conda activate document

# Change to script directory
cd /mnt/c/Users/endor/Documents/private/private_works/scripts/projects/tag_refiner

# Load environment variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Run tag_refiner.py in background
nohup python tag_refiner.py --provider openai --model o4-mini --input-dir "/mnt/c/Users/endor/Documents/private/Clippings" > "tag_processing_startup_$(date +%Y%m%d_%H%M%S).log" 2>&1 &

echo "Tag Refiner started in background with PID: $!"