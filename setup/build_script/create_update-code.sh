#!/bin/bash

# Configuration directory
CONFIG_DIR="../config/code"

# Check if config directory exists
if [ ! -d "$CONFIG_DIR" ]; then
    echo "Error: Configuration directory $CONFIG_DIR not found."
    echo "Please ensure you are running this script from the setup/build directory."
    exit 1
fi

# List of specific files to run (space-separated filenames).
# Leave empty to run all .yaml files in the config directory.
TARGET_FILES=()

# Check if config directory exists
if [ ! -d "$CONFIG_DIR" ]; then
    echo "Error: Configuration directory $CONFIG_DIR not found."
    echo "Please ensure you are running this script from the setup/build directory."
    exit 1
fi

# Determine files to process
FILES_TO_PROCESS=()
if [ ${#TARGET_FILES[@]} -gt 0 ]; then
    echo "Processing specified files: ${TARGET_FILES[*]}"
    for file in "${TARGET_FILES[@]}"; do
        FULL_PATH="$CONFIG_DIR/$file"
        if [ -f "$FULL_PATH" ]; then
            FILES_TO_PROCESS+=("$FULL_PATH")
        else
            echo "Warning: Specified file '$file' not found in $CONFIG_DIR. Skipping."
        fi
    done

    if [ ${#FILES_TO_PROCESS[@]} -eq 0 ]; then
        echo "Error: None of the specified files were found."
        exit 1
    fi
else
    # Check if there are any yaml files
    shopt -s nullglob
    YAML_FILES=("$CONFIG_DIR"/*.yaml)
    shopt -u nullglob

    if [ ${#YAML_FILES[@]} -eq 0 ]; then
         echo "No YAML configuration files found in $CONFIG_DIR"
         exit 0
    else
        FILES_TO_PROCESS=("${YAML_FILES[@]}")
    fi
fi

# Iterate over files
echo "Starting code setup..."
for config_file in "${FILES_TO_PROCESS[@]}"; do
    echo "Processing $config_file..."
    
    # Setup the code using verdi
    verdi code create core.code.installed --config "$config_file" --non-interactive
    
    if [ $? -eq 0 ]; then
        echo "Successfully setup code from $config_file"
    else
        echo "Failed to setup code from $config_file"
    fi
done
echo "Code setup process finished."
