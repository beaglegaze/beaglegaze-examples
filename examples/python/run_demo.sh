#!/bin/bash

# Exit on error
set -e

# 1. Build the Hardhat Testnet Docker Image
echo "--- Building Hardhat Testnet Docker Image ---"
docker build -t hardhat-testnet ../../deploy/hardhat-testnet

# 2. Run the Docker Container
echo "--- Running Hardhat Testnet Docker Container ---"
if [ "$(docker ps -q -f name=hardhat-testnet)" ]; then
    echo "Hardhat container is already running."
else
    docker run -d --rm --name hardhat-testnet -p 8545:8545 hardhat-testnet
fi

# Give the container a moment to start
sleep 5

# 3. Install Dependencies
echo "--- Installing Python Dependencies ---"
pip install -r ../requirements.txt
pip install -e ../

# 4. Run the Demo Script
echo "--- Running Demo Script ---"
python demo.py

# 5. Stop the Docker Container
echo "--- Stopping Hardhat Testnet Docker Container ---"
docker stop hardhat-testnet
