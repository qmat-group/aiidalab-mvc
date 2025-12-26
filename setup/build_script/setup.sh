#!/bin/bash

# This script orchestrates the setup of both computers and codes.

echo "=========================================="
echo "Starting Full AiiDA Setup"
echo "=========================================="

# Run setup_computer.sh
echo ""
echo ">>> Step 1: Setting up Computers"
if [ -f "./setup_computer.sh" ]; then
    bash ./setup_computer.sh
else
    echo "Error: ./setup_computer.sh not found!"
fi

# Run create_update-code.sh
echo ""
echo ">>> Step 2: Setting up Codes"
if [ -f "./create_update-code.sh" ]; then
    bash ./create_update-code.sh
else
    echo "Error: ./create_update-code.sh not found!"
fi

echo ""
echo "=========================================="
echo "Full Setup Finished"
echo "=========================================="
