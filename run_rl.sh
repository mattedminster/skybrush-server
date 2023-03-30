#! /bin/bash
/Users/matt/.local/bin/poetry shell && /Users/matt/.local/bin/poetry lock --no-update && /Users/matt/.local/bin/poetry install && skybrushd -c ../skybridge-ext-rl-gaming/rl-skybrush.jsonc 
