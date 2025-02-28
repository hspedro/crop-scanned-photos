.PHONY: help install check test lint run generate-test clean coverage coverage-html format

help:  ## Show this help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies using Poetry
	@command -v poetry >/dev/null 2>&1 || { echo >&2 "Poetry is required but not installed. Install from https://python-poetry.org/docs/#installation"; exit 1; }
	poetry install

check: ## Check dependencies and environment
	@command -v poetry >/dev/null 2>&1 || { echo >&2 "Poetry is required but not installed."; exit 1; }
	@echo "Poetry is installed"
	@poetry check
	@echo "Project dependencies are properly configured"
	@poetry run python -c "import cv2" >/dev/null 2>&1 || { echo >&2 "OpenCV is not installed."; exit 1; }
	@echo "OpenCV is installed"
	@poetry run python -c "from PIL import Image" >/dev/null 2>&1 || { echo >&2 "Pillow is not installed."; exit 1; }
	@echo "Pillow is installed"

test: ## Run pytest
	poetry run pytest test/

coverage: ## Run tests with coverage report
	poetry run python -m pytest --cov=crop_scanned_photos --cov-report=term-missing test/

coverage-html: ## Generate HTML coverage report
	poetry run python -m pytest --cov=crop_scanned_photos --cov-report=html test/
	@echo "HTML coverage report generated in htmlcov/index.html"

lint: ## Run flake8 linting
	poetry run flake8 crop_scanned_photos/
	poetry run mypy crop_scanned_photos/

run: ## Run the crop script (can be customized with make run ARGS="--input-folder custom_input")
	poetry run python crop.py $(ARGS)

generate-test: ## Generate test images (can be customized with make generate-test ARGS="-n 6")
	poetry run python create_test_image.py $(ARGS)

format:
	poetry run black crop_scanned_photos/
	poetry run isort crop_scanned_photos/

clean: ## Clean up generated files and caches
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	rm -rf output_images/*
	rm -rf examples/*
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
