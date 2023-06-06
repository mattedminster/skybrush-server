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
  CONFIG_FILE=rl-skybrush-mac-sim.jsonc
else
  # Linux
  echo "Running on Linux"
  CONFIG_FILE=rl-skybrush-ubuntu-sim.jsonc
fi

#increment version number
python3 ../increment_pytoml.py ../skybridge-ext-rl-gaming/pyproject.toml

# Activate poetry environment and run skybrushd
source "$(~/.local/bin/poetry env info --path)/bin/activate" && ~/.local/bin/poetry lock --no-update && ~/.local/bin/poetry install && skybrushd -c ../skybridge-ext-rl-gaming/$CONFIG_FILE  2>&1 | tee rl.log
