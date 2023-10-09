#!/bin/bash

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



# Activate poetry environment and run skybrushd
source "$(poetry env info --path)/bin/activate" && poetry lock --no-update && poetry install && skybrushd -c ../skybridge-ext-rl-gaming/$CONFIG_FILE  2>&1 | tee rl.log
