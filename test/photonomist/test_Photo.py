"""Test suite for the Photo Class.

This test suite aims to test Photo's methds with regard to extracting and returning metadata,
moving photos to other directories.

The script can be executed on its own or incorporated into a larger test suite.
However the tests are run, be aware of which version of the module is actually
being tested. If the library is installed in site-packages, that version takes
precedence over the version in this project directory. Use a virtualenv test
environment or setuptools develop mode to test against the development version.
"""

import pytest
from photonomist.photo import Photo

@pytest.fixture
def my_photo():
    photo_path = r"C:\repos\photonomist\test\data\testing_folder_with_photos\bla\DSC_0262.NEF"
    my_photo = Photo(photo_path)
    return my_photo

def test_is_photo_object():
    """Test src\\photonomist\\photo.Photo> __init__
    """
    photo_path = r"a\\random\\path\\to\\a\\photo"
    my_photo = Photo(photo_path)
    assert isinstance(my_photo, Photo)

def test_extract_tags_from_a_valid_photo(my_photo):
    """Test src\\photonomist\\photo.Photo> extract_exif
    """
    my_photo.extract_exif_tags()
    assert "EXIF DateTimeOriginal" in list(my_photo.tags.keys())
    assert "Image DateTimeOriginal" in list(my_photo.tags.keys())

def test_extract_tags_from_a_invalid_photo():
    """Test src\\photonomist\\photo.Photo> extract_exif_tags
    """
    photo_path = r"a\\random\\path\\to\\a\\photo"
    my_photo = Photo(photo_path)
    my_photo.extract_exif_tags()
    assert my_photo.tags == 'NoTags'

def test_extract_metadata(my_photo):
    """Test src\\photonomist\\photo.Photo> metadata_dict
    """
    my_photo.metadata_dict()
    assert "DateTimeOriginal" in list(my_photo.metadata.keys())

def test_extract_metadata_does_not_extract_empty_values(my_photo):
    """Test src\\photonomist\\photo.Photo> metadata_dict
    """
    my_photo.metadata_dict()
    assert "Copyright" not in list(my_photo.metadata.keys())

def test_extract_metadata_with_extracted_tags(my_photo):
    """Test src\\photonomist\\photo.Photo> metadata_dict
    """
    my_photo.extract_exif_tags()
    my_photo.metadata_dict()
    assert "DateTimeOriginal" in list(my_photo.metadata.keys())

def test_return_date(my_photo):
    """Test src\\photonomist\\photo.Photo> metadata_dict
    """
    assert "2019:12:14" == my_photo.get_date()