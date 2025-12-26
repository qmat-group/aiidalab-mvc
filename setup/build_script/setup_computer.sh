#!/bin/bash

# Configuration directory
CONFIG_DIR="../config/computer"

# Check if config directory exists
if [ ! -d "$CONFIG_DIR" ]; then
    echo "Error: Configuration directory $CONFIG_DIR not found."
    echo "Please ensure you are running this script from the setup/build directory."
    exit 1
fi

# List of specific files to run (space-separated filenames).
# Leave empty to run all .yaml files in the config directory.
TARGET_FILES=("pias_computer.yaml")

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
echo "Starting computer setup..."
for config_file in "${FILES_TO_PROCESS[@]}"; do
    echo "Processing $config_file..."
    
    # Define temporary files
    SETUP_Yaml="temp_setup.yaml"
    CONFIG_Yaml="temp_configure.yaml"
    
    # Use python to split the config file into setup and configure parts
    python3 -c "
import yaml
import sys

try:
    with open('$config_file', 'r') as f:
        data = yaml.safe_load(f)
        
    # Keys supported by 'verdi computer setup'
    setup_keys = ['label', 'hostname', 'description', 'transport', 'scheduler', 'work_dir', 'mpiprocs_per_machine', 'prepend_text', 'append_text']
    setup_data = {k: v for k, v in data.items() if k in setup_keys}
    
    # Keys supported by 'verdi computer configure' (add more if needed)
    # Common ssh keys: username, port, look_for_keys, key_filename, timeout, allow_agent, proxy_command, compress, gss_auth, gss_kex, gss_deleg_creds, gss_host, load_system_host_keys, key_policy, safe_interval, use_login_shell
    config_keys = ['username', 'port', 'look_for_keys', 'key_filename', 'timeout', 'allow_agent', 'proxy_command', 'compress', 'gss_auth', 'gss_kex', 'gss_deleg_creds', 'gss_host', 'load_system_host_keys', 'key_policy', 'safe_interval', 'use_login_shell', 'user']
    configure_data = {k: v for k, v in data.items() if k in config_keys}
    
    with open('$SETUP_Yaml', 'w') as f:
        yaml.dump(setup_data, f)
        
    with open('$CONFIG_Yaml', 'w') as f:
        yaml.dump(configure_data, f)
        
except Exception as e:
    print(f'Error processing yaml: {e}')
    sys.exit(1)
"
    if [ $? -ne 0 ]; then
        echo "Failed to process YAML file $config_file"
        continue
    fi

    # Setup the computer using verdi with the filtered setup yaml
    verdi computer setup --config "$SETUP_Yaml" --non-interactive
    
    if [ $? -eq 0 ]; then
        echo "Successfully setup computer from $config_file"
        
        # Extract label and transport to configure
        LABEL=$(grep "^label:" "$SETUP_Yaml" | awk '{print $2}' | tr -d '"' | tr -d "'")
        TRANSPORT=$(grep "^transport:" "$SETUP_Yaml" | awk '{print $2}' | tr -d '"' | tr -d "'")
        
        if [ -n "$LABEL" ] && [ -n "$TRANSPORT" ]; then
            echo "Configuring computer $LABEL with transport $TRANSPORT..."
            
            # Configure the computer using the filtered configure yaml
            verdi computer configure "$TRANSPORT" "$LABEL" --config "$CONFIG_Yaml" --non-interactive
            
            if [ $? -eq 0 ]; then
                 echo "Successfully configured computer $LABEL"
            else
                 echo "Failed to configure computer $LABEL"
            fi
        else
             echo "Could not extract label or transport, skipping configuration."
        fi
    else
        echo "Failed to setup computer from $config_file"
    fi
    
    # Cleanup temp files
    rm -f "$SETUP_Yaml" "$CONFIG_Yaml"
done

echo "Computer setup process finished."
