.PHONY: all prebuild build

all: prebuild build

prebuild:
	@echo "Running prebuild process..."
	poetry run prebuild

build: prebuild
	@echo "Running build process..."
	poetry build

publish: build
	@echo "Publishing to PyPI..."
	poetry publish