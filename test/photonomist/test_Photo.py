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
    photo_path = r"test\data\testing_folder_with_photos\bla\DSC_0262.NEF"
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

@pytest.mark.parametrize("year, month, expected", [
    (False, True, "2019:12"),
    (True, False, "2019"),
    (True, True, "2019:12"),
    (False, False, "2019:12:14"),
])
def test_return_date_with_year_month_keywords(my_photo, year, month, expected):
    """Test src\\photonomist\\photo.Photo> get_date
    """
    assert my_photo.get_date(year=year, month=month) == expected

@pytest.mark.parametrize("year, expected", [
    (True, "2019"),
    (False,"2019:12:14"),
])
def test_return_date_with_year_keyword(my_photo, year, expected):
    """Test src\\photonomist\\photo.Photo> get_date
    """
    assert my_photo.get_date(year=year) == expected

@pytest.mark.parametrize("month, expected", [
    (True, "2019:12"),
    (False,"2019:12:14"),
])
def test_return_date_with_month_keyword(my_photo, month, expected):
    """Test src\\photonomist\\photo.Photo> get_date
    """
    assert my_photo.get_date(month=month) == expected

@pytest.fixture()
def move_photo_del_folder():
    photo_path = r"test\data\testing_folder_with_photos\bla\DSC_0262.NEF"
    move_photo_del_folder = Photo(photo_path)
    yield move_photo_del_folder
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\DSC_0262.NEF", r"C:\repos\photonomist\test\data\testing_folder_with_photos\bla\DSC_0262.NEF")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder")

def test_move_to_photo_to_other_folder(move_photo_del_folder):
    """Test src\\photonomist\\photo.Photo> move_to_folder
    """
    new_dir = r"test\data\testing_folder_with_photos\move_folder"
    move_photo_del_folder.move_to_folder(new_dir)
    file_list = os.listdir(new_dir)
    assert "DSC_0262.NEF" in file_list

def test_object_name_is_photo_name(my_photo, capsys):
    """Test src\\photonomist\\photo.Photo> __str__
    """
    print(my_photo, end='')
    captured = capsys.readouterr()
    assert captured.out == "DSC_0262.NEF"

@pytest.mark.parametrize("filepath, counter, extension, expected", [
    (r"a\random\photo", 2, ".jpg", "a\\random\\photo(2).jpg"),
    (r"another\random\photo", 0, ".nef", "another\\random\\photo(0).nef"),
    (r"a\random\photo", 1234321, ".jpg", "a\\random\\photo(1234321).jpg"),
])
def test_add_parentheses_and_counter_to_photo_name(my_photo, filepath, counter, extension, expected):
    """Test src\\photonomist\\photo.Photo> construct_new_photo_path
    Parametrized to test different filepaths, counters and extensions
    """
    assert my_photo.construct_new_photo_path(filepath, counter, extension) == expected

@pytest.mark.parametrize("parentheses_text, expected", [
    ("random_string_without_parentheses", []),
    ("random_string_with(5)_number_parentheses_in_the_middle", [(18,21)]),
    ("random_string_with_number_parentheses_in_the_end(1)", [(48,51)]),
    ("random_string_with_string_parentheses_in_the_end(one)", []),
    ("random_string_with_multiple_(0)number(1)_parentheses(2)_in(3)_the(4)_end(5)", [(37, 40), (52, 55), (58, 61), (65, 68), (72, 75)]),
])
def test_identifies_set_of_parentheses_which_contain_numbers(my_photo, parentheses_text, expected):
    """Test src\\photonomist\\photo.Photo> find_parentheses_numbers
    Parametrized to test different strings with and without parentheses
    """
    assert my_photo.find_parentheses_numbers(parentheses_text) == expected

@pytest.mark.parametrize("date, expected", [
    ("2019:12:14", "2019:12"),
    ("1990:07:23", "1990:07"),
    ("2021:01:02", "2021:01"),
    (":-)_panagiotis", ":-)_panagio"),
])
def test_date_month_returns_only_year_month(my_photo, date, expected):
    """Test src\\photonomist\\photo.Photo> date_month
    """
    assert my_photo.date_month(date) == expected

@pytest.mark.parametrize("date, expected", [
    ("2019:12:14", "2019"),
    ("1990:07:23", "1990"),
    ("2021:01:02", "2021"),
    (":-)_panagiotis", ":-)_pana"),
])
def test_date_year_returns_only_year(my_photo, date, expected):
    """Test src\\photonomist\\photo.Photo> date_year
    """
    assert my_photo.date_year(date) == expected
    
# Make the script executable.
if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))