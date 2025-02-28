"""
Crop Scanned Photos package.
A tool to detect and crop multiple photos from scanned images.
"""

__version__ = "0.1.0"

from .main import remove_white_borders, process_images, parse_args, main

__all__ = ['remove_white_borders', 'process_images', 'parse_args', 'main']
