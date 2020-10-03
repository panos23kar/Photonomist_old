"""Test suite for the __main__ module.

This test suite aims to test user's input and its validity!

The script can be executed on its own or incorporated into a larger test suite.
However the tests are run, be aware of which version of the module is actually
being tested. If the library is installed in site-packages, that version takes
precedence over the version in this project directory. Use a virtualenv test
environment or setuptools develop mode to test against the development version.
"""
import pytest
import os, shutil
from photonomist.__main__ import path_exists, path_items, clean_path, path_string, path_photos, traverse_photos_path, photos_size, disk_space, photo_dir_name, dir_name_exists, create_photo_dir, transfer_photo, paths_same_disk, input_path_validation, export_path_validation

@pytest.mark.parametrize("sample_path", [("blablabla"), 
                                         (r'C:\repos\photonomist\test\data\blablabla'), 
                                         (r'C:/repos/photonomist/test\data/blablabla')])
def test_invalid_path(sample_path):
    """ Test for src\\photonomist\\__main__ > path_exists

    Parametrized to test invalid str and paths
    """
    with pytest.raises(FileNotFoundError, match="The provided path was not found!"):
        path_exists(sample_path)

def test_path_contains_photos():
    """ Test for src\\photonomist\\__main__ > path_items

    Testing_empty_folder was created in test\\data for testing purposes.
    """
    #Need an empty dir for testing
    sample_path = r'test\data\testing_empty_folder'
    with pytest.raises(Exception, match="The provided path does not contain any files!"):
        path_items(sample_path)

def test_clean_path():
    """Test src\\photonomist\\__main__ > clean_path
    """
    sample_path = r"'C:\repos\photonomist\test\data\testing_empty_folder'"
    sample_path = clean_path(sample_path)
    assert sample_path == r"C:\repos\photonomist\test\data\testing_empty_folder"

@pytest.mark.parametrize("sample_path", [(0), 
                                         (None), 
                                         (1),
                                         (1.0),
                                         (True),
                                         (False),
                                         ('0')])
def test_user_input_is_string(sample_path):
    """Test src\\photonomist\\__main__ > path_string

    Parametrized to test invalid int, floats, boolean and NoneType arguments.
    """
    with pytest.raises(Exception, match="Your input is not a valid path!"):
        path_string(sample_path)

def test_extracts_0_photo_roots():
    """Test src\\photonomist\\__main__ > traverse_photos_path
    """
    sample_path =  r'C:\repos\photonomist\test\data\testing_empty_folder'
    assert len(traverse_photos_path(sample_path)) == 0

def test_extracts_photo_roots():
    """Test src\\photonomist\\__main__ > traverse_photos_path
    """
    sample_path =  r'C:\repos\photonomist\test\data\testing_folder_with_photos'
    assert len(traverse_photos_path(sample_path)) == 5

def test_path_does_not_contain_jpg_neff_files():
    """Test src\\photonomist\\__main__ > path_photos
    """
    sample_photo_roots = traverse_photos_path(r'C:\repos\photonomist\test\data\testing_empty_folder')
    with pytest.raises(Exception, match="The provided path does not contain any files with .jpg or .nef extension!"):
        path_photos(sample_photo_roots)

def test_path_contains_files_extensions_jpg_nef(capsys):
    """Test src\\photonomist\\__main__ > path_photos
    """
    sample_photo_roots = traverse_photos_path(r'C:\repos\photonomist\test\data\testing_folder_with_photos')
    path_photos(sample_photo_roots)
    captured = capsys.readouterr()
    assert r'C:\repos\photonomist\test\data\testing_folder_with_photos\bla\blanef\blablanef\blablablanef' in captured.out
    assert r'C:\repos\photonomist\test\data\testing_folder_with_photos\bla\blabla\blablabla' in captured.out

def test_photos_total_size():
    """Test src\\photonomist\\__main__ > photos_size
    """
    sample_photo_roots = traverse_photos_path(r'C:\repos\photonomist\test\data\testing_folder_with_photos')
    photos_total_size = photos_size(sample_photo_roots)
    assert photos_total_size == 53316894

def test_enough_free_disk_space(capsys):
    """Test src\\photonomist\\__main__ > disk_space
    """
    sample_path = r'C:'
    photos_total_size = 500
    disk_space(sample_path, photos_total_size)
    captured = capsys.readouterr()
    assert 'You have enough free disk space!' in captured.out

def test_not_enough_free_disk_space(capsys):
    """Test src\\photonomist\\__main__ > disk_space
    """
    sample_path = r'C:'
    photos_total_size = 5000000000000000000
    with pytest.raises(Exception, match="You need at least 5000000001073741824 free bytes but you only have"):
        disk_space(sample_path, photos_total_size)

def test_create_photo_folder_name():
    """Test src\\photonomist\\__main__ > photo_dir_name
    """
    date = "2016:12:17"
    assert "2016_12_17_place_reason_people" == photo_dir_name(date)

def test_photo_folder_exist_in_export_path():
    """Test src\\photonomist\\__main__ > dir_name_exists
    """
    dir_name = "2016_12_17_place_reason_people"
    export_path = r"C:\Users\potis\Pictures\2016\blabla"
    assert dir_name_exists(dir_name, export_path) == True

def test_photo_folder_does_not_exist_in_export_path():
    """Test src\\photonomist\\__main__ > dir_name_exists
    """
    dir_name = "random_random"
    export_path = r"C:\Users\potis\Pictures\2016\blabla"
    assert dir_name_exists(dir_name, export_path) == False

@pytest.fixture()
def delete_folder_after_test():
    delete_folder_after_test = "1990_07_23_place_reason_people"
    yield delete_folder_after_test
    os.rmdir(r"C:\Users\potis\Pictures\2016\blabla\1990_07_23_place_reason_people")

def test_create_photo_folder(delete_folder_after_test):
    """Test src\\photonomist\\__main__ > create_photo_dir
    """
    dir_name = delete_folder_after_test
    export_path = r"C:\Users\potis\Pictures\2016\blabla"
    create_photo_dir(dir_name, export_path)
    assert r"1990_07_23_place_reason_people" in os.listdir(export_path)

@pytest.fixture()
def move_photo_del_folder():
    move_photo_del_folder = r"C:\repos\photonomist\test\data\testing_folder_with_photos\bla\DSC_0262.NEF"
    yield move_photo_del_folder
    shutil.move(r"C:\repos\photonomist\test\data\testing_folder_with_photos\move_folder\2019_12_14_place_reason_people\DSC_0262.NEF", r"C:\repos\photonomist\test\data\testing_folder_with_photos\bla\DSC_0262.NEF")
    os.rmdir(r"C:\repos\photonomist\test\data\testing_folder_with_photos\move_folder\2019_12_14_place_reason_people")
    os.rmdir(r"C:\repos\photonomist\test\data\testing_folder_with_photos\move_folder")

def test_transfer_photo_to_another_folder_if_it_has_valid_date(move_photo_del_folder):
    """Test src\\photonomist\\__main__ > transfer__photo
    """
    export_path = r"C:\repos\photonomist\test\data\testing_folder_with_photos\move_folder"
    transfer_photo(move_photo_del_folder, export_path)
    assert "DSC_0262.NEF" in os.listdir(r"C:\repos\photonomist\test\data\testing_folder_with_photos\move_folder\2019_12_14_place_reason_people")

def test_if_export_and_input_paths_point_to_the_same_disk():
    """Test src\\photonomist\\__main__ > paths_same_disk
    """
    photos_path = r"C:\a\random\path\to\photos"
    export_path = r"C:\repos\photonomist\test\data\testing_folder_with_photos\move_folder"
    assert paths_same_disk(photos_path, export_path) == True

def test_if_export_and_input_paths_do_not_point_to_the_same_disk():
    """Test src\\photonomist\\__main__ > paths_same_disk
    """
    photos_path = r"G:\DCIM\104D5500"
    export_path = r"C:\repos\photonomist\test\data\testing_folder_with_photos"
    assert paths_same_disk(photos_path, export_path) == False

def test_input_path_validation_path_exists():
    """ Test for src\\photonomist\\__main__ > input_path_validation
    """
    sample_path = "blablabla"
    with pytest.raises(FileNotFoundError, match="The provided path was not found!"):
        input_path_validation(sample_path)

def test_input_path_validation_path_items():
    """ Test for src\\photonomist\\__main__ > input_path_validation
    """
    sample_path = r'test\data\testing_empty_folder'
    with pytest.raises(Exception, match="The provided path does not contain any files!"):
        input_path_validation(sample_path)

def test_input_path_validation_traverse_photos_path():
    """ Test for src\\photonomist\\__main__ > input_path_validation
    """
    sample_path =  r'C:\repos\photonomist\test\data\testing_folder_with_photos'
    assert len(input_path_validation(sample_path)) == 5

def test_export_path_validation_path_exists():
    """ Test for src\\photonomist\\__main__ > export_path_validation
    """
    export_path = "blablabla"
    input_path = "blablabla"
    path_roots = ["blablabla"]
    with pytest.raises(FileNotFoundError, match="The provided path was not found!"):
        export_path_validation(export_path, input_path, path_roots)

# Make the script executable.
if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))