import pytest
import os
from PIL import Image
import shutil
import sys
from crop_scanned_photos import (
    parse_args,
    remove_white_borders,
    process_images,
    main
)


def create_test_image(path, size=(2000, 2800)):
    """Create a test image with colored rectangles on white background."""
    # Create a white background
    background = Image.new('RGB', size, 'white')

    # Create some "scanned photos" (colored rectangles) with white borders
    photos = [
        ((100, 100, 900, 1300), 'blue'),    # Top left photo
        ((1000, 100, 1800, 1300), 'red'),   # Top right photo
        ((100, 1500, 900, 2700), 'green'),  # Bottom left photo
        ((1000, 1500, 1800, 2700), 'yellow')  # Bottom right photo
    ]

    # Draw the photos on the background
    for bounds, color in photos:
        photo = Image.new('RGB', (bounds[2] - bounds[0], bounds[3] - bounds[1]), color)
        background.paste(photo, (bounds[0], bounds[1]))

    # Ensure directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Save the image
    background.save(path, 'JPEG', quality=95)
    return True


@pytest.fixture
def test_dirs(tmp_path):
    """Create test directories and cleanup after tests."""
    input_dir = tmp_path / "raw"
    output_dir = tmp_path / "output_images"
    input_dir.mkdir()
    output_dir.mkdir()

    yield input_dir, output_dir

    # Cleanup
    shutil.rmtree(input_dir, ignore_errors=True)
    shutil.rmtree(output_dir, ignore_errors=True)


def test_parse_args(monkeypatch):
    # Mock sys.argv for testing
    monkeypatch.setattr(sys, 'argv', ['crop.py'])

    # Test default values
    args = parse_args()
    assert args.input_folder == "raw"
    assert args.output_folder == "output_images"
    assert args.threads == 1

    # Test environment variables
    monkeypatch.setenv("INPUT_FOLDER", "custom_input")
    monkeypatch.setenv("THREADS", "4")
    monkeypatch.setattr(sys, 'argv', ['crop.py'])  # Reset argv
    args = parse_args()
    assert args.input_folder == "custom_input"
    assert args.threads == 4


def test_remove_white_borders(test_dirs):
    """Test the white border removal functionality."""
    input_dir, output_dir = test_dirs
    test_image_path = input_dir / "test_image.jpg"
    create_test_image(str(test_image_path))

    # Test with valid image
    remove_white_borders(
        str(test_image_path),
        str(output_dir),
        threshold_value=240,
        threshold_max=255,
        min_contour_width=50,
        min_contour_height=50
    )

    # Check if cropped images were created
    output_files = os.listdir(output_dir)
    assert len(output_files) >= 4

    # Test with invalid image path
    remove_white_borders(
        "nonexistent.jpg",
        str(output_dir),
        threshold_value=240,
        threshold_max=255,
        min_contour_width=50,
        min_contour_height=50
    )

    # Test with image having no contours
    blank_image_path = input_dir / "blank.jpg"
    Image.new('RGB', (100, 100), 'white').save(blank_image_path)
    remove_white_borders(
        str(blank_image_path),
        str(output_dir),
        threshold_value=240,
        threshold_max=255,
        min_contour_width=50,
        min_contour_height=50
    )


def test_process_images(test_dirs):
    """Test the image processing functionality."""
    input_dir, output_dir = test_dirs
    
    # Create test images
    create_test_image(str(input_dir / "test1.jpg"))
    create_test_image(str(input_dir / "test2.jpg"))
    (input_dir / "not_an_image.txt").touch()
    
    # Test with valid configuration
    image_files = process_images(
        output_folder=str(output_dir),
        input_folder=str(input_dir),
        allowed_extensions=('.jpg', '.jpeg', '.png'),
        threads=1
    )
    assert len(image_files) == 2
    assert all(f.endswith('.jpg') for f in image_files)


def test_main_function(test_dirs, monkeypatch):
    """Test the main function with different scenarios."""
    input_dir, output_dir = test_dirs
    
    # Create test images
    create_test_image(str(input_dir / "test1.jpg"))
    create_test_image(str(input_dir / "test2.jpg"))
    
    # Mock command line arguments
    test_args = [
        "--input-folder", str(input_dir),
        "--output-folder", str(output_dir),
        "--threads", "2"
    ]
    monkeypatch.setattr(sys, 'argv', ["crop.py"] + test_args)
    
    # Run main function
    main()
    
    # Check results
    output_files = os.listdir(output_dir)
    assert len(output_files) >= 8  # Should have at least 8 cropped images (4 from each input)


def test_invalid_threshold_values(test_dirs):
    """Test behavior with invalid threshold values."""
    input_dir, output_dir = test_dirs
    test_image_path = input_dir / "test_image.jpg"
    create_test_image(str(test_image_path))

    # Test with invalid threshold values
    remove_white_borders(
        str(test_image_path),
        str(output_dir),
        threshold_value=300,  # Invalid value
        threshold_max=255,
        min_contour_width=50,
        min_contour_height=50
    )


def test_small_contours(test_dirs):
    """Test handling of small contours."""
    input_dir, output_dir = test_dirs
    test_image_path = input_dir / "test_image.jpg"
    create_test_image(str(test_image_path))

    # Test with large minimum contour size
    remove_white_borders(
        str(test_image_path),
        str(output_dir),
        threshold_value=240,
        threshold_max=255,
        min_contour_width=2000,  # Larger than image
        min_contour_height=2000
    )

    # Should not create any output files
    output_files = os.listdir(output_dir)
    assert len(output_files) == 0
