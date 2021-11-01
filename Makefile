DIR:=$(strip $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST)))))

build-all:	build-run build-test

build-run:
	docker build --target run --tag apg-run .
run:
	docker run --rm -it -v $(DIR)/apgfiles:/audio_program_generator/apgfiles apg-run

build-test:
	docker build --target test --tag apg-test .
test:
	docker run --rm -it -v $(DIR)/apgfiles:/audio_program_generator/apgfiles apg-test
