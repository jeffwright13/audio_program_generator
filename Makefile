DIR:=$(strip $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST)))))
NAME:=$(shell grep -e "^name\s*=\s*" pyproject.toml | cut -d = -f 2 | xargs)
VERSION:=$(shell grep -e "^version\s*=\s*" pyproject.toml | cut -d = -f 2 | xargs)
IGNORE_DIRS := dist|htmlcov|venv|__pycache__|audio_program_generator.egg-info

apg-build:
	docker build --target apg-run --tag $(NAME):$(VERSION) .

apg:
	docker run --rm -it -v $(DIR)/apgfiles:/audio_program_generator/apgfiles $(NAME):$(VERSION) ${args}

apg-build-test:
	docker build --target apg-test --tag apg-test:$(VERSION) .

test:
	docker run --rm -it -v $(DIR)/apgfiles:/audio_program_generator/apgfiles apg-test:$(VERSION)

.PHONY : clean
clean:
	docker container rm -f $(NAME):$(VERSION)
	docker image rm -f $(NAME):$(VERSION)

tree:
	tree -I "$(IGNORE_DIRS)"
