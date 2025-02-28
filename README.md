# Image Cropper

[![Tests](https://github.com/yourusername/crop-scanned-photos/actions/workflows/test.yml/badge.svg)](https://github.com/yourusername/crop-scanned-photos/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/crop-scanned-photos.svg)](https://badge.fury.io/py/crop-scanned-photos)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python tool that processes scanned images to automatically detect and crop multiple photos. Specifically designed for scanned images with white borders (as commonly produced by scanners), where multiple photos were scanned together on a single page. The tool will identify each individual photo and save them as separate files.

## Features

- Detects multiple photos in scanned images with white borders
- Automatically crops and saves individual photos
- Supports multi-threading for faster processing
- Configurable via command-line arguments or environment variables
- Supports various image formats (PNG, JPG, JPEG)

## Installation

1. Make sure you have Poetry installed ([Poetry Installation Guide](https://python-poetry.org/docs/#installation))

2. Clone this repository:

```bash
git clone https://github.com/yourusername/image-cropper.git
cd image-cropper
```

3. Install dependencies:

```bash
poetry install
```

## Usage

### Command-Line Arguments

```bash
poetry run python crop.py --help
```

### Environment Variables

You can also configure the tool using environment variables:

Available arguments:
- `--input-folder`: Input folder containing scanned images (default: "raw")
- `--output-folder`: Output folder for cropped images (default: "output_images")
- `--threads`: Number of processing threads (default: 1)
- `--threshold-value`: Threshold value for image processing (default: 240)
- `--threshold-max`: Maximum threshold value (default: 255)
- `--min-contour-width`: Minimum contour width to process (default: 50)
- `--min-contour-height`: Minimum contour height to process (default: 50)
- `--allowed-extensions`: Comma-separated list of allowed file extensions (default: .png,.jpg,.jpeg)

```bash
export INPUT_FOLDER="scans"
export OUTPUT_FOLDER="cropped"
export THREADS="4"
export THRESHOLD_VALUE="230"
export THRESHOLD_MAX="255"
export MIN_CONTOUR_WIDTH="100"
export MIN_CONTOUR_HEIGHT="100"
export ALLOWED_EXTENSIONS=".png,.jpg,.jpeg"

poetry run python crop.py
```

Note: Command-line arguments take precedence over environment variables.

## Directory Structure

```
crop-scanned-photos/
├── raw/                    # Default input directory for scanned images
├── output_images/          # Default output directory for cropped images
├── examples/               # Default output directory for test images
├── crop.py                 # Main script
├── create_test_image.py    # Script to generate test images
├── pyproject.toml          # Poetry configuration
└── README.md               # This file
```

## Test Images Generation

The project includes a script to generate test images that simulate scanned photos with white borders. These test images are useful for development and testing of the cropping functionality.

### Generating Test Images

Use the `create_test_image.py` script to generate test images:

```bash
poetry run python create_test_image.py -n 4 -o test_4_photos.jpg -f examples
```

This will create a test image with 4 photos in the `examples` directory.

### Running the Cropping Script on Test Images

To run the cropping script on the test images, use the following command:

```bash
poetry run python crop.py --input-folder examples --output-folder examples/cropped
```

This will process the test images in the `examples` directory and save the cropped images in the `examples/cropped` directory.

### Options:
- `-n, --num_photos`: Number of photos to include (default: 4)
- `-o, --output`: Output filename (default: test_N_scan.jpg where N is number of photos)
- `-f, --folder`: Output folder path (default: examples)

### Test Image Structure

The generated test images have the following characteristics:
- A4 scan proportions (2000x2800 pixels)
- White background simulating scanner bed
- Colored rectangles representing photos (for easy visual testing)
- Automatic grid layout based on number of photos
- 100px white margins between photos

Example layout for 4 photos:
![Example Test Image](examples/test_4_scan.jpg)

After running the cropping script, the output directory will contain the following files:
- test_1_scan.jpg (blue region)
- test_2_scan.jpg (red region)
- test_3_scan.jpg (green region)
- test_4_scan.jpg (yellow region)

Example output:
![Example Cropped Image 1](examples/cropped/test_1_scan.jpg)
![Example Cropped Image 2](examples/cropped/test_2_scan.jpg)
![Example Cropped Image 3](examples/cropped/test_3_scan.jpg)
![Example Cropped Image 4](examples/cropped/test_4_scan.jpg)

### Expected Cropping Behavior

When processing these test images, the cropping script should:
1. Detect the boundaries between the white background and colored regions
2. Create separate image files for each detected region
3. Remove the white borders around each photo
4. Preserve the original aspect ratio of each photo
5. Name the output files based on the input filename with sequential numbering

For example, processing `test_4_scan.jpg` should produce:
- test_4_scan_1.jpg (blue region)
- test_4_scan_2.jpg (red region)
- test_4_scan_3.jpg (green region)
- test_4_scan_4.jpg (yellow region)

Each output image should contain only the colored rectangle without any white borders.

## Requirements

- Python 3.8 or higher
- OpenCV (installed automatically via Poetry)

## License

MIT License

Copyright (c) 2025 Pedro Soares
