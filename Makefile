DIR:=$(strip $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST)))))
build:
	docker build --tag apg .
run:
	docker run --rm -it -v "$(DIR)"/apgfiles:/audio_program_generator/apgfiles apg
