"""Utility script to generate test images for development and testing."""

import argparse
import math
import os

from PIL import Image


def create_test_scan(num_photos, output_path=None, output_folder="examples"):
    """Create a test scan image with multiple photos.

    Args:
        num_photos: Number of photos to include in the test image
        output_path: Output filename (default: test_N_scan.jpg where N is number
            of photos)
        output_folder: Output folder path (default: examples)

    Returns:
        str: Full output path of the created test image
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Calculate grid dimensions based on number of photos
    grid_size = math.ceil(math.sqrt(num_photos))

    # Create a white background (A4 scan proportions)
    background = Image.new("RGB", (2000, 2800), "white")

    # Calculate photo dimensions
    photo_width = 800
    photo_height = 1200
    margin = 100

    # Colors for different photos
    colors = ["blue", "red", "green", "yellow", "purple", "orange", "pink", "cyan"]

    # Generate photo positions
    photos = []
    for i in range(min(num_photos, grid_size * grid_size)):
        row = i // grid_size
        col = i % grid_size

        x1 = margin + col * (photo_width + margin)
        y1 = margin + row * (photo_height + margin)
        x2 = x1 + photo_width
        y2 = y1 + photo_height

        photos.append(((x1, y1, x2, y2), colors[i % len(colors)]))

    # Draw the photos
    for bounds, color in photos:
        photo = Image.new("RGB", (bounds[2] - bounds[0], bounds[3] - bounds[1]), color)
        background.paste(photo, (bounds[0], bounds[1]))

    # Generate output filename if not provided
    if output_path is None:
        output_path = f"test_{num_photos}_scan.jpg"

    # Combine output folder with filename
    full_output_path = os.path.join(output_folder, output_path)

    # Save the image
    background.save(full_output_path, "JPEG", quality=95)
    print(f"Test image created at: {full_output_path}")
    return full_output_path


def parse_args() -> argparse.Namespace:
    """Parse command line arguments for test image generation.

    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Create a test scan image with multiple photos"
    )
    parser.add_argument(
        "-n",
        "--num_photos",
        type=int,
        default=4,
        help="Number of photos to include in the test image (default: 4)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output filename (default: test_N_scan.jpg where N is number of photos)",
    )
    parser.add_argument(
        "-f",
        "--folder",
        type=str,
        default="examples",
        help="Output folder path (default: examples)",
    )

    return parser.parse_args()


def main() -> None:
    """Generate test images based on command line arguments."""
    args = parse_args()
    create_test_scan(args.num_photos, args.output, args.folder)


if __name__ == "__main__":
    main()
