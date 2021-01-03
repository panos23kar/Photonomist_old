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
from photonomist.__main__ import path_exists, path_items, clean_path, path_string,\
     path_photos, traverse_photos_path, photos_size, disk_space, photo_dir_name,\
          dir_name_exists, create_photo_dir, transfer_photo, paths_same_disk,\
               input_path_validation, export_path_validation, tidy_photos, replace_backslashes,\
                   group_by_message, group_by_, group_option

@pytest.mark.parametrize("sample_path", [("blablabla"), 
                                         (r'test\data\blablabla'), 
                                         (r'test/data/blablabla')])
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
    sample_path = r'test\data\testing_empty_folder\empty'
    with pytest.raises(Exception, match="The provided path does not contain any files!"):
        path_items(sample_path)

def test_clean_path():
    """Test src\\photonomist\\__main__ > clean_path
    """
    sample_path = r"'test\data\testing_empty_folder'"
    sample_path = clean_path(sample_path)
    assert sample_path == r"test\data\testing_empty_folder"

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
    sample_path =  r'test\data\testing_empty_folder'
    assert len(traverse_photos_path(sample_path)) == 0

def test_extracts_photo_roots():
    """Test src\\photonomist\\__main__ > traverse_photos_path
    """
    sample_path =  r'test\data\testing_folder_with_photos'
    num_of_photos = 0
    for photo_list in traverse_photos_path(sample_path).values():
        print(photo_list)
        num_of_photos += len(photo_list)
    assert num_of_photos == 9

def test_path_does_not_contain_jpg_jpeg_nef_cr2_files():
    """Test src\\photonomist\\__main__ > path_photos
    """
    sample_photo_roots = traverse_photos_path(r'test\data\testing_empty_folder')
    with pytest.raises(Exception, match="The provided path does not contain any files with .jpg, .jpeg, .nef or .cr2 extension!"):
        path_photos(sample_photo_roots)

@pytest.mark.skip(reason="commented it out")
def test_path_contains_files_extensions_jpg_nef_cr2(capsys):
    """Test src\\photonomist\\__main__ > path_photos
    """
    sample_photo_roots = traverse_photos_path(r'test\data\testing_folder_with_photos')
    path_photos(sample_photo_roots)
    captured = capsys.readouterr()
    assert r'test\data\testing_folder_with_photos\bla\blanef\blablanef\blablablanef' in captured.out
    assert r'test\data\testing_folder_with_photos\bla\blabla\blablabla' in captured.out
    assert r'C:\repos\photonomist\test\data\testing_folder_with_photos\bla\blablacr2' in captured.out

def test_photos_total_size():
    """Test src\\photonomist\\__main__ > photos_size
    """
    sample_photo_roots = traverse_photos_path(r'test\data\testing_folder_with_photos')
    photos_total_size = photos_size(sample_photo_roots)
    assert photos_total_size == 140855708

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

@pytest.mark.parametrize("date, year, month, expected", [
    ("2016", True, False, "2016_place_reason_people"),
    ("2016:12:17", False, False, "2016_12_17_place_reason_people"),
    ("2016:12", False, True, "2016_12_place_reason_people"),
])
def test_create_photo_folder_name(date, year, month, expected):
    """Test src\\photonomist\\__main__ > photo_dir_name
    """
    assert expected == photo_dir_name(date, year=year, month=month)

def test_create_photo_folder_name_no_keyword_arguments():
    """Test src\\photonomist\\__main__ > photo_dir_name
    """
    date = "2016:12:17"
    assert "2016_12_17_place_reason_people" == photo_dir_name(date)

@pytest.mark.parametrize("date, year, expected", [
    ("2016", True, "2016_place_reason_people"),
    ("2016:12:17", False, "2016_12_17_place_reason_people"),
])
def test_create_photo_folder_name_no_month_keyword(date, year, expected):
    """Test src\\photonomist\\__main__ > photo_dir_name
    """
    assert expected == photo_dir_name(date, year=year)

@pytest.mark.parametrize("date, month, expected", [
    ("2016:12", True, "2016_12_place_reason_people"),
    ("2016:12:17", False, "2016_12_17_place_reason_people"),
])
def test_create_photo_folder_name_no_year_keyword(date, month, expected):
    """Test src\\photonomist\\__main__ > photo_dir_name
    """
    assert expected == photo_dir_name(date, month=month)

@pytest.mark.parametrize("date, name_pattern, expected", [
    ("2016:12:17", "_place", "2016_12_17_place"),
    ("2016:12:17", "_place_reason", "2016_12_17_place_reason"),
    ("2016:12:17", "_place_people", "2016_12_17_place_people"),
    ("2016:12:17", "_reason", "2016_12_17_reason"),
    ("2016:12:17", "_reason_people", "2016_12_17_reason_people"),
    ("2016:12:17", "_people", "2016_12_17_people"),
    ("2016:12:17", "", "2016_12_17"),
])
def test_create_photo_folder_name_specified_name_pattern(date, name_pattern, expected):
    """Test src\\photonomist\\__main__ > photo_dir_name
    """
    assert expected == photo_dir_name(date, name_pattern=name_pattern)

def test_photo_folder_exist_in_export_path():
    """Test src\\photonomist\\__main__ > dir_name_exists
    """
    dir_name = "2016_12_17_place_reason_people"
    export_path = r"test\data\testing_empty_folder"
    assert dir_name_exists(dir_name, export_path) == True

def test_photo_folder_does_not_exist_in_export_path():
    """Test src\\photonomist\\__main__ > dir_name_exists
    """
    dir_name = "random_random"
    export_path = r"test\data\testing_empty_folder"
    assert dir_name_exists(dir_name, export_path) == False

@pytest.fixture()
def delete_folder_after_test():
    delete_folder_after_test = "1990_07_23_place_reason_people"
    yield delete_folder_after_test
    os.rmdir(r"test\data\testing_empty_folder\1990_07_23_place_reason_people")

def test_create_photo_folder(delete_folder_after_test):
    """Test src\\photonomist\\__main__ > create_photo_dir
    """
    dir_name = delete_folder_after_test
    export_path = r"test\data\testing_empty_folder"
    create_photo_dir(dir_name, export_path)
    assert r"1990_07_23_place_reason_people" in os.listdir(export_path)

@pytest.fixture()
def move_photo_del_folder():
    move_photo_del_folder = r"test\data\testing_folder_with_photos\bla\DSC_0262.NEF"
    yield move_photo_del_folder
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2019_12_14_place_reason_people\DSC_0262.NEF", r"test\data\testing_folder_with_photos\bla\DSC_0262.NEF")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2019_12_14_place_reason_people")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder")

def test_transfer_photo_to_another_folder_if_it_has_valid_date(move_photo_del_folder):
    """Test src\\photonomist\\__main__ > transfer_photo
    """
    export_path = r"test\data\testing_folder_with_photos\move_folder"
    transfer_photo(move_photo_del_folder, export_path)
    assert "DSC_0262.NEF" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2019_12_14_place_reason_people")

@pytest.fixture()
def move_photo_del_folder_month_keyword():
    move_photo_del_folder_month_keyword = r"test\data\testing_folder_with_photos\bla\DSC_0262.NEF"
    yield move_photo_del_folder_month_keyword
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2019_12_place_reason_people\DSC_0262.NEF", r"test\data\testing_folder_with_photos\bla\DSC_0262.NEF")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2019_12_place_reason_people")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder")

def test_transfer_photo_to_another_folder_if_it_has_valid_date_month_keyword(move_photo_del_folder_month_keyword):
    """Test src\\photonomist\\__main__ > transfer_photo
    """
    export_path = r"test\data\testing_folder_with_photos\move_folder"
    transfer_photo(move_photo_del_folder_month_keyword, export_path, year=False, month=True)
    assert "DSC_0262.NEF" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2019_12_place_reason_people")

@pytest.fixture()
def move_photo_del_folder_year_keyword():
    move_photo_del_folder_year_keyword = r"test\data\testing_folder_with_photos\bla\DSC_0262.NEF"
    yield move_photo_del_folder_year_keyword
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2019_place_reason_people\DSC_0262.NEF", r"test\data\testing_folder_with_photos\bla\DSC_0262.NEF")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2019_place_reason_people")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder")

def test_transfer_photo_to_another_folder_if_it_has_valid_date_year_keyword(move_photo_del_folder_year_keyword):
    """Test src\\photonomist\\__main__ > transfer_photo
    """
    export_path = r"test\data\testing_folder_with_photos\move_folder"
    transfer_photo(move_photo_del_folder_year_keyword, export_path, year=True, month=False)
    assert "DSC_0262.NEF" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2019_place_reason_people")

@pytest.fixture()
def move_canon_photo_del_folder():
    move_canon_photo_del_folder = r"C:\repos\photonomist\test\data\testing_folder_with_photos\bla\blablacr2\IMG_5494.CR2"
    yield move_canon_photo_del_folder
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2020_10_25_place_reason_people\IMG_5494.CR2", r"C:\repos\photonomist\test\data\testing_folder_with_photos\bla\blablacr2\IMG_5494.CR2")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2020_10_25_place_reason_people")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder")

def test_transfer_canon_photo_to_another_folder_if_it_has_valid_date(move_canon_photo_del_folder):
    """Test src\\photonomist\\__main__ > transfer_photo (canon raw photo)
    """
    export_path = r"test\data\testing_folder_with_photos\move_folder"
    transfer_photo(move_canon_photo_del_folder, export_path)
    assert "IMG_5494.CR2" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2020_10_25_place_reason_people")

@pytest.fixture()
def move_photo_del_folder_place():
    move_photo_del_folder_place = r"test\data\testing_folder_with_photos\bla\DSC_0262.NEF"
    yield move_photo_del_folder_place
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2019_12_14_place\DSC_0262.NEF", r"test\data\testing_folder_with_photos\bla\DSC_0262.NEF")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2019_12_14_place")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder")

def test_transfer_photo_to_another_folder_place_name_convention(move_photo_del_folder_place):
    """Test src\\photonomist\\__main__ > transfer_photo
    """
    export_path = r"test\data\testing_folder_with_photos\move_folder"
    transfer_photo(move_photo_del_folder_place, export_path, name_pattern="_place")
    assert "DSC_0262.NEF" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2019_12_14_place")

@pytest.fixture()
def move_photo_del_folder_place_reason():
    move_photo_del_folder_place_reason = r"test\data\testing_folder_with_photos\bla\DSC_0262.NEF"
    yield move_photo_del_folder_place_reason
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2019_12_14_place_reason\DSC_0262.NEF", r"test\data\testing_folder_with_photos\bla\DSC_0262.NEF")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2019_12_14_place_reason")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder")

def test_transfer_photo_to_another_folder_place_reason_name_convention(move_photo_del_folder_place_reason):
    """Test src\\photonomist\\__main__ > transfer_photo
    """
    export_path = r"test\data\testing_folder_with_photos\move_folder"
    transfer_photo(move_photo_del_folder_place_reason, export_path, name_pattern="_place_reason")
    assert "DSC_0262.NEF" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2019_12_14_place_reason")

@pytest.fixture()
def move_photo_del_folder_place_people():
    move_photo_del_folder_place_people = r"test\data\testing_folder_with_photos\bla\DSC_0262.NEF"
    yield move_photo_del_folder_place_people
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2019_12_14_place_people\DSC_0262.NEF", r"test\data\testing_folder_with_photos\bla\DSC_0262.NEF")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2019_12_14_place_people")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder")

def test_transfer_photo_to_another_folder_place_people_name_convention(move_photo_del_folder_place_people):
    """Test src\\photonomist\\__main__ > transfer_photo
    """
    export_path = r"test\data\testing_folder_with_photos\move_folder"
    transfer_photo(move_photo_del_folder_place_people, export_path, name_pattern="_place_people")
    assert "DSC_0262.NEF" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2019_12_14_place_people")

def test_if_export_and_input_paths_point_to_the_same_disk():
    """Test src\\photonomist\\__main__ > paths_same_disk
    """
    photos_path = r"C:\a\random\path\to\photos"
    export_path = r"C:\test\data\testing_folder_with_photos\move_folder"
    assert paths_same_disk(photos_path, export_path) == True

def test_if_export_and_input_paths_do_not_point_to_the_same_disk():
    """Test src\\photonomist\\__main__ > paths_same_disk
    """
    photos_path = r"G:\DCIM\104D5500"
    export_path = r"test\data\testing_folder_with_photos"
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
    sample_path = r'test\data\testing_empty_folder\empty'
    with pytest.raises(Exception, match="The provided path does not contain any files!"):
        input_path_validation(sample_path)

def test_input_path_validation_traverse_photos_path():
    """ Test for src\\photonomist\\__main__ > input_path_validation
    """
    sample_path =  r'test\data\testing_folder_with_photos'
    num_of_photos = 0
    for photo_list in traverse_photos_path(sample_path).values():
        print(photo_list)
        num_of_photos += len(photo_list)
    assert num_of_photos == 9

def test_export_path_validation_path_exists():
    """ Test for src\\photonomist\\__main__ > export_path_validation
    """
    export_path = "blablabla"
    input_path = "blablabla"
    path_roots = ["blablabla"]
    with pytest.raises(FileNotFoundError, match="The provided path was not found!"):
        export_path_validation(export_path, input_path, path_roots)

@pytest.fixture()
def move_photos_del_folders():
    photo_roots = traverse_photos_path(r"C:\repos\photonomist\test\data\testing_folder_with_photos\bla\blabla")
    yield photo_roots
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2019_12_14_place_reason_people\DSC_0262.NEF", r"test\data\testing_folder_with_photos\bla\blabla\DSC_0262.NEF")
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2020_04_24_place_reason_people\DSC_1402.JPG", r"test\data\testing_folder_with_photos\bla\blabla\blablabla\DSC_1402.JPG")
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2020_10_25_place_reason_people\IMG_5494.CR2", r"C:\repos\photonomist\test\data\testing_folder_with_photos\bla\blabla\IMG_5494.CR2")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2019_12_14_place_reason_people")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2020_04_24_place_reason_people")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2020_10_25_place_reason_people")
    os.remove(r"test\data\testing_folder_with_photos\move_folder\not_transferred.txt")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder")

def test_move_all_photos_of_all_folders(move_photos_del_folders):
    """ Test for src\\photonomist\\__main__ > tidy_photos
    """
    export_path = r"test\data\testing_folder_with_photos\move_folder"
    tidy_photos(export_path, move_photos_del_folders)
    assert "DSC_0262.NEF" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2019_12_14_place_reason_people")
    assert "DSC_1402.JPG" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2020_04_24_place_reason_people")
    assert "IMG_5494.CR2" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2020_10_25_place_reason_people")

@pytest.fixture()
def move_photos_del_folders_month():
    photo_roots = traverse_photos_path(r"C:\repos\photonomist\test\data\testing_folder_with_photos\bla\blabla")
    yield photo_roots
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2019_12_place_reason_people\DSC_0262.NEF", r"test\data\testing_folder_with_photos\bla\blabla\DSC_0262.NEF")
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2020_04_place_reason_people\DSC_1402.JPG", r"test\data\testing_folder_with_photos\bla\blabla\blablabla\DSC_1402.JPG")
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2020_10_place_reason_people\IMG_5494.CR2", r"test\data\testing_folder_with_photos\bla\blabla\IMG_5494.CR2")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2019_12_place_reason_people")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2020_04_place_reason_people")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2020_10_place_reason_people")
    os.remove(r"test\data\testing_folder_with_photos\move_folder\not_transferred.txt")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder")

def test_move_all_photos_of_all_folders_month(move_photos_del_folders_month):
    """ Test for src\\photonomist\\__main__ > tidy_photos
    """
    export_path = r"test\data\testing_folder_with_photos\move_folder"
    tidy_photos(export_path, move_photos_del_folders_month, year=False, month=True)
    assert "DSC_0262.NEF" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2019_12_place_reason_people")
    assert "DSC_1402.JPG" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2020_04_place_reason_people")
    assert "IMG_5494.CR2" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2020_10_place_reason_people")

@pytest.fixture()
def move_photos_del_folders_year():
    photo_roots = traverse_photos_path(r"C:\repos\photonomist\test\data\testing_folder_with_photos\bla\blabla")
    yield photo_roots
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2019_place_reason_people\DSC_0262.NEF", r"test\data\testing_folder_with_photos\bla\blabla\DSC_0262.NEF")
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2020_place_reason_people\DSC_1402.JPG", r"test\data\testing_folder_with_photos\bla\blabla\blablabla\DSC_1402.JPG")
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2020_place_reason_people\IMG_5494.CR2", r"test\data\testing_folder_with_photos\bla\blabla\IMG_5494.CR2")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2019_place_reason_people")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2020_place_reason_people")
    os.remove(r"test\data\testing_folder_with_photos\move_folder\not_transferred.txt")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder")

def test_move_all_photos_of_all_folders_year(move_photos_del_folders_year):
    """ Test for src\\photonomist\\__main__ > tidy_photos
    """
    export_path = r"test\data\testing_folder_with_photos\move_folder"
    tidy_photos(export_path, move_photos_del_folders_year, year=True, month=False)
    assert "DSC_0262.NEF" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2019_place_reason_people")
    assert "DSC_1402.JPG" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2020_place_reason_people")
    assert "IMG_5494.CR2" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2020_place_reason_people")

@pytest.fixture()
def move_photos_del_folders_place():
    photo_roots = traverse_photos_path(r"C:\repos\photonomist\test\data\testing_folder_with_photos\bla\blabla")
    yield photo_roots
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2019_place\DSC_0262.NEF", r"test\data\testing_folder_with_photos\bla\blabla\DSC_0262.NEF")
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2020_place\DSC_1402.JPG", r"test\data\testing_folder_with_photos\bla\blabla\blablabla\DSC_1402.JPG")
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2020_place\IMG_5494.CR2", r"test\data\testing_folder_with_photos\bla\blabla\IMG_5494.CR2")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2019_place")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2020_place")
    os.remove(r"test\data\testing_folder_with_photos\move_folder\not_transferred.txt")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder")

def test_move_all_photos_of_all_folders_place(move_photos_del_folders_place):
    """ Test for src\\photonomist\\__main__ > tidy_photos
    """
    export_path = r"test\data\testing_folder_with_photos\move_folder"
    tidy_photos(export_path, move_photos_del_folders_place, year=True, month=False, name_pattern="_place")
    assert "DSC_0262.NEF" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2019_place")
    assert "DSC_1402.JPG" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2020_place")
    assert "IMG_5494.CR2" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2020_place")

@pytest.fixture()
def move_photos_del_folders_place_reason():
    photo_roots = traverse_photos_path(r"C:\repos\photonomist\test\data\testing_folder_with_photos\bla\blabla")
    yield photo_roots
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2019_place_reason\DSC_0262.NEF", r"test\data\testing_folder_with_photos\bla\blabla\DSC_0262.NEF")
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2020_place_reason\DSC_1402.JPG", r"test\data\testing_folder_with_photos\bla\blabla\blablabla\DSC_1402.JPG")
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2020_place_reason\IMG_5494.CR2", r"test\data\testing_folder_with_photos\bla\blabla\IMG_5494.CR2")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2019_place_reason")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2020_place_reason")
    os.remove(r"test\data\testing_folder_with_photos\move_folder\not_transferred.txt")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder")

def test_move_all_photos_of_all_folders_place_reason(move_photos_del_folders_place_reason):
    """ Test for src\\photonomist\\__main__ > tidy_photos
    """
    export_path = r"test\data\testing_folder_with_photos\move_folder"
    tidy_photos(export_path, move_photos_del_folders_place_reason, year=True, month=False, name_pattern="_place_reason")
    assert "DSC_0262.NEF" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2019_place_reason")
    assert "DSC_1402.JPG" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2020_place_reason")
    assert "IMG_5494.CR2" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2020_place_reason")

@pytest.fixture()
def move_photos_del_folders_place_people():
    photo_roots = traverse_photos_path(r"C:\repos\photonomist\test\data\testing_folder_with_photos\bla\blabla")
    yield photo_roots
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2019_place_people\DSC_0262.NEF", r"test\data\testing_folder_with_photos\bla\blabla\DSC_0262.NEF")
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2020_place_people\DSC_1402.JPG", r"test\data\testing_folder_with_photos\bla\blabla\blablabla\DSC_1402.JPG")
    shutil.move(r"test\data\testing_folder_with_photos\move_folder\2020_place_people\IMG_5494.CR2", r"test\data\testing_folder_with_photos\bla\blabla\IMG_5494.CR2")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2019_place_people")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder\2020_place_people")
    os.remove(r"test\data\testing_folder_with_photos\move_folder\not_transferred.txt")
    os.rmdir(r"test\data\testing_folder_with_photos\move_folder")

def test_move_all_photos_of_all_folders_place_people(move_photos_del_folders_place_people):
    """ Test for src\\photonomist\\__main__ > tidy_photos
    """
    export_path = r"test\data\testing_folder_with_photos\move_folder"
    tidy_photos(export_path, move_photos_del_folders_place_people, year=True, month=False, name_pattern="_place_people")
    assert "DSC_0262.NEF" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2019_place_people")
    assert "DSC_1402.JPG" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2020_place_people")
    assert "IMG_5494.CR2" in os.listdir(r"test\data\testing_folder_with_photos\move_folder\2020_place_people")

@pytest.mark.parametrize("random_slashes_path, expected", [
    ("this/is/a/random/path/with/backslashes", "this\\is\\a\\random\\path\\with\\backslashes"),
    ("this/is\\a\\random/path/with/backslashes", "this\\is\\a\\random\\path\\with\\backslashes"),
    ("this\\is/a/random/path/with\\backslashes", "this\\is\\a\\random\\path\\with\\backslashes"),
    ("this\\is\\a\\random\\path\\without\\backslashes", "this\\is\\a\\random\\path\\without\\backslashes"),
    ("thisisarandompathwithbackslashes", "thisisarandompathwithbackslashes"),
])
def test_a_path_does_not_have_backslashes(random_slashes_path, expected):
    """ Test for src\\photonomist\\__main__ > replace_backslashes
    Parametrized to test different paths with and without backslashes
    """
    assert replace_backslashes(random_slashes_path) == expected

def test_informative_print_message_for_grouping_options(capsys):
    """ Test for src\\photonomist\\__main__ > group_by_message
    """
    group_by_message()
    captured = capsys.readouterr()
    assert 'Dear user,\nYou can group your photos by:\n\t1)Day\n\t2)Month\n\t3)Year\nPlease let me know your option!' in captured.out

@pytest.mark.parametrize("user_input, expected", [
    ("blabla", True),
    ("", True),
    ("y", True),
    ("Yes", True),
    ("Parakalw polu", True),
    ("n", False),
    ("no", False),
    ("No", False),
    ("nO", False),
    ("0", False),
    ("false", False),
    ("False", False),
])
def test_group_by_returns_true_or_false_on_user_value(monkeypatch, user_input, expected):
    """ Test for src\\photonomist\\__main__ > group_by_
    """
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    assert group_by_(user_input) == expected

def test_group_option_prints_group_message(capsys, monkeypatch):
    """ Test for src\\photonomist\\__main__ > group_option
    """
    monkeypatch.setattr('builtins.input', lambda _: "kati")
    group_option()
    captured = capsys.readouterr()
    assert 'Dear user,\nYou can group your photos by:\n\t1)Day\n\t2)Month\n\t3)Year\nPlease let me know your option!' in captured.out

# Make the script executable.
if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))