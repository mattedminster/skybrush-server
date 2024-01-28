#!/bin/bash

rm ./skybrush-server/rl.log

# Function to handle script termination
cleanup() {
    echo "Terminating skybrushd..."
    pkill -f "skybrushd"
    exit
}

# Register cleanup function to execute on script termination
trap cleanup EXIT

# Determine configuration file based on OS
if [[ "$OSTYPE" == "darwin"* ]]; then
  # Mac OS
  echo "Running on Mac OS"
  CONFIG_FILE=rl-skybrush-mac.jsonc
else
  # Linux
  echo "Running on Linux"
  CONFIG_FILE=rl-skybrush-ubuntu-se.jsonc
fi



# Activate poetry environment and run skybrushd
poetry install && poetry run skybrushd -c ../skybridge-ext-rl-gaming/$CONFIG_FILE  2>&1 | tee rl.log
