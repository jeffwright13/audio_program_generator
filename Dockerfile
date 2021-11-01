###########################################
FROM jrottenberg/ffmpeg:4.1-ubuntu AS base
###########################################
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_NO_INTERACTION=1

RUN apt-get update && \
    apt-get install -y python3.8 pip git && \
    apt-get install --no-install-recommends -y curl build-essential && \
    apt-get clean

##################
FROM base AS apg
##################
WORKDIR /
RUN mkdir /apg && \
    git clone https://github.com/jeffwright13/audio_program_generator.git

###################
FROM apg AS poetry
###################
ARG APG_SRC_DIR=/audio_program_generator
WORKDIR $APG_SRC_DIR
RUN pip install --no-cache-dir poetry

###################
FROM poetry AS run
###################
ARG APG_SRC_DIR=/audio_program_generator
WORKDIR $APG_SRC_DIR
COPY ./entry-run.sh entry-run.sh
RUN cd $APG_SRC_DIR && \
    poetry install --no-interaction --no-dev

ENTRYPOINT ["/bin/bash"]
CMD ["/audio_program_generator/entry-run.sh"]

####################
FROM poetry AS test
####################
ARG APG_SRC_DIR=/audio_program_generator
COPY ./entry-test.sh ./entry-test.sh
RUN cd $APG_SRC_DIR && \
    poetry install --no-interaction
RUN ln -s $(poetry env info --path) /var/my-venv
RUN echo 'source /var/my-venv/bin/activate' >> ~/.bashrc

ENTRYPOINT ["/bin/bash"]
CMD ["/audio_program_generator/entry-test.sh"]
