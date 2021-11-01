#!/bin/bash
export VIRTUAL_ENV_DISABLE_PROMPT=1
cd /audio_program_generator || exit
echo --------------------------------------
echo Type 'apg' to create an audio program.
echo Type 'exit' to quit.
echo --------------------------------------
source ~/.bashrc
poetry shell
