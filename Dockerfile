##########################################
FROM jrottenberg/ffmpeg:3.2-ubuntu AS base
##########################################
RUN apt-get update && apt-get install -y python3.8 pip git

#################
FROM base AS apg
#################
ARG APG_DIR=/audio_program_generator/
WORKDIR /
COPY ./entry.sh entry.sh

RUN mkdir /apg && \
    git clone https://github.com/jeffwright13/audio_program_generator.git && \
    pip install poetry && \
    cd $APG_DIR && \
    poetry install --no-dev

###################
FROM apg AS runtime
###################
ENTRYPOINT ["/bin/bash"]
CMD ["/entry.sh"]
