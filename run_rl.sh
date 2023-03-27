#! /bin/bash
poetry lock --no-update && poetry install && skybrushd -c ../../skybrush/skybrush-ext-rl-gaming/rl-skybrush.jsonc 
