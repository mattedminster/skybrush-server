#!/bin/bash

if [[ "$OSTYPE" == "darwin"* ]]; then
  # Mac OS
  echo "Running on Mac OS"
  CONFIG_FILE=rl-skybrush-mac.jsonc
else
  # Linux
  echo "Running on Linux"
  CONFIG_FILE=rl-skybrush-ubuntu.jsonc
fi

source "$(~/.local/bin/poetry env info --path)/bin/activate" && poetry lock --no-update && poetry install && skybrushd -c ../skybridge-ext-rl-gaming/$CONFIG_FILE
