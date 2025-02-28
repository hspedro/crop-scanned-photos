"""
Crop Scanned Photos package.
A tool to detect and crop multiple photos from scanned images
with white borders.
"""

__version__ = "0.1.0"

from .main import main, parse_args, process_images, remove_white_borders

__all__ = ["main", "parse_args", "process_images", "remove_white_borders"]
