#!/bin/bash
docker run --rm -it -v "$(pwd)"/apgfiles:/audio_program_generator/apgfiles apg
