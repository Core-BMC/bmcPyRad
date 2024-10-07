#!/bin/bash

# Set the folder paths and n value
FOLDER_PATHS=("./Control" "./TMJOA")
N=34
OUTPUT_FILES=("output_features_Control.csv" "output_features_TMJOA.csv")

# Loop through each folder path and corresponding output file
for i in "${!FOLDER_PATHS[@]}"; do
    FOLDER_PATH=${FOLDER_PATHS[$i]}
    OUTPUT_FILE=${OUTPUT_FILES[$i]}
    
    echo "Processing folder: $FOLDER_PATH"

    # Run the Python script with the specified parameters
    python -c "
import os
from PyRadiomicsPrep_bmc import RadiomicsPreparation

# Initialize the class with the folder path and n value
radiomics_prep = RadiomicsPreparation('$FOLDER_PATH', $N)

# Prepare the input file
radiomics_prep.prepare_input_file()

# Run Pyradiomics
radiomics_prep.run_pyradiomics('$OUTPUT_FILE')
"
done

# End of script
