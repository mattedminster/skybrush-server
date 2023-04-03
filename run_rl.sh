#! /bin/bash
poetry shell && poetry lock --no-update && poetry install && skybrushd -c ../skybridge-ext-rl-gaming/rl-skybrush.jsonc 
