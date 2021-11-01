#!/bin/bash
set +x
export VIRTUAL_ENV_DISABLE_PROMPT=1
cd /audio_program_generator || exit
echo --------------------------------------
echo Running tests...
echo --------------------------------------
source /var/my-venv/bin/activate
pytest -v --html=tests/results/report.html --self-contained-html
