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
import os, shutil
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
    """Test src\\photonomist\\photo.Photo> __extract_exif
    """
    my_photo._Photo__extract_exif_tags()
    assert "EXIF DateTimeOriginal" in list(my_photo._Photo__tags.keys())
    assert "Image DateTimeOriginal" in list(my_photo._Photo__tags.keys())

def test_extract_tags_from_a_invalid_photo():
    """Test src\\photonomist\\photo.Photo> __extract_exif_tags
    """
    photo_path = r"a\\random\\path\\to\\a\\photo"
    my_photo = Photo(photo_path)
    my_photo._Photo__extract_exif_tags()
    assert my_photo._Photo__tags == {}

def test_extract_metadata(my_photo):
    """Test src\\photonomist\\photo.Photo> __metadata_dict
    """
    my_photo._Photo__metadata_dict()
    assert "DateTimeOriginal" in list(my_photo.metadata.keys())

def test_extract_metadata_does_not_extract_empty_values(my_photo):
    """Test src\\photonomist\\photo.Photo> __metadata_dict
    """
    my_photo._Photo__metadata_dict()
    assert "Copyright" not in list(my_photo.metadata.keys())

def test_extract_metadata_with_extracted_tags(my_photo):
    """Test src\\photonomist\\photo.Photo> __metadata_dict
    """
    my_photo._Photo__extract_exif_tags()
    my_photo._Photo__metadata_dict()
    assert "DateTimeOriginal" in list(my_photo.metadata.keys())

def test_return_date(my_photo):
    """Test src\\photonomist\\photo.Photo> get_date
    """
    assert "2019:12:14" == my_photo.get_date()

def test_date_return_none_if_no_metadata():
    """Test src\\photonomist\\photo.Photo> get_date
    """
    photo_path = r"a\random\path\to\a\photo"
    my_photo = Photo(photo_path)
    assert None == my_photo.get_date()

@pytest.fixture()
def move_photo_del_folder():
    photo_path = r"C:\repos\photonomist\test\data\testing_folder_with_photos\bla\DSC_0262.NEF"
    move_photo_del_folder = Photo(photo_path)
    yield move_photo_del_folder
    shutil.move(r"C:\repos\photonomist\test\data\testing_folder_with_photos\move_folder\DSC_0262.NEF", r"C:\repos\photonomist\test\data\testing_folder_with_photos\bla\DSC_0262.NEF")
    os.rmdir(r"C:\repos\photonomist\test\data\testing_folder_with_photos\move_folder")

def test_move_to_photo_to_other_folder(move_photo_del_folder):
    """Test src\\photonomist\\photo.Photo> move_to_folder
    """
    new_dir = r"C:\repos\photonomist\test\data\testing_folder_with_photos\move_folder"
    move_photo_del_folder.move_to_folder(new_dir)
    file_list = os.listdir(new_dir)
    assert "DSC_0262.NEF" in file_list

def test_object_name_is_photo_name(my_photo, capsys):
    """Test src\\photonomist\\photo.Photo> __str__
    """
    print(my_photo, end='')
    captured = capsys.readouterr()
    assert captured.out == "DSC_0262.NEF"

# Make the script executable.
if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))