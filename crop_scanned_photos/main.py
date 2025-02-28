import os
import cv2
import argparse
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple, List


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Process scanned images to detect and crop multiple photos.')

    parser.add_argument('--input-folder',
                        default=os.getenv("INPUT_FOLDER", "raw"),
                        help='Input folder containing scanned images (default: raw)')

    parser.add_argument('--output-folder',
                        default=os.getenv("OUTPUT_FOLDER", "output_images"),
                        help='Output folder for cropped images (default: output_images)')

    parser.add_argument('--threads',
                        type=int,
                        default=int(os.getenv("THREADS", "1")),
                        help='Number of processing threads (default: 1)')

    parser.add_argument('--threshold-value',
                        type=int,
                        default=int(os.getenv("THRESHOLD_VALUE", "240")),
                        help='Threshold value for image processing (default: 240)')

    parser.add_argument('--threshold-max',
                        type=int,
                        default=int(os.getenv("THRESHOLD_MAX", "255")),
                        help='Maximum threshold value (default: 255)')

    parser.add_argument('--min-contour-width',
                        type=int,
                        default=int(os.getenv("MIN_CONTOUR_WIDTH", "50")),
                        help='Minimum contour width to process (default: 50)')

    parser.add_argument('--min-contour-height',
                        type=int,
                        default=int(os.getenv("MIN_CONTOUR_HEIGHT", "50")),
                        help='Minimum contour height to process (default: 50)')

    parser.add_argument('--allowed-extensions',
                        default=os.getenv("ALLOWED_EXTENSIONS", ".png,.jpg,.jpeg"),
                        help='Comma-separated list of allowed file extensions (default: .png,.jpg,.jpeg)')

    args = parser.parse_args()
    args.allowed_extensions = tuple(args.allowed_extensions.split(','))
    return args


def remove_white_borders(image_path: str, output_folder: str, threshold_value: int, threshold_max: int, min_contour_width: int, min_contour_height: int):
    """Detects multiple photos in a scanned image and saves them as separate files."""
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    if image is None:
        print(f"Error: Unable to read {image_path}")
        return

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to highlight non-white areas
    _, thresh = cv2.threshold(gray, threshold_value, threshold_max, cv2.THRESH_BINARY)

    # Invert colors to highlight objects
    thresh_inv = cv2.bitwise_not(thresh)

    # Find contours of the separate images
    contours, _ = cv2.findContours(thresh_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print(f"Warning: No contours found in {image_path}")
        return

    # Sort contours by position (top to bottom, then left to right)
    contours = sorted(contours, key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0]))

    # Process each detected image region separately
    base_filename = os.path.splitext(os.path.basename(image_path))[0]
    count = 0

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Ensure the detected region is significant enough to be considered a photo
        if w < min_contour_width or h < min_contour_height:  # Ignore very small regions
            continue

        cropped_image = image[y: y + h, x: x + w]

        # Save each detected photo
        output_path = os.path.join(output_folder, f"{base_filename}_{count}.jpg")
        cv2.imwrite(output_path, cropped_image)
        print(f"Saved: {output_path}")
        count += 1


def process_images(output_folder: str, input_folder: str, allowed_extensions: Tuple[str], threads: int = 1) -> List[str]:
    """Processes images using multiple threads."""
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    return [os.path.join(input_folder, f) for f in os.listdir(input_folder)
            if f.lower().endswith(allowed_extensions)]


def main():
    args = parse_args()
    image_files = process_images(
        output_folder=args.output_folder,
        input_folder=args.input_folder,
        allowed_extensions=args.allowed_extensions,
        threads=args.threads
    )
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        executor.map(lambda x: remove_white_borders(x, args.output_folder, args.threshold_value, args.threshold_max, args.min_contour_width, args.min_contour_height), image_files)


if __name__ == "__main__":
    main()
