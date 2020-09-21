"""Test suite for the __main__ module.

This tesy suite aims to test user's input and its validity!

The script can be executed on its own or incorporated into a larger test suite.
However the tests are run, be aware of which version of the module is actually
being tested. If the library is installed in site-packages, that version takes
precedence over the version in this project directory. Use a virtualenv test
environment or setuptools develop mode to test against the development version.
"""
import pytest
from photonomist.__main__ import path_exists, path_items, clean_path, path_string, path_photos

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
    with pytest.raises(Exception, match="Your input is not valid!"):
        path_string(sample_path)

def test_path_does_not_contain_jpg_neff_files():
    """Test src\\photonomist\\__main__ > path_photos
    """
    sample_path = r'C:\repos\photonomist\test\data\testing_empty_folder'
    with pytest.raises(Exception, match="The provided path does not contain any files with .jpg or .nef extension!"):
        path_photos(sample_path)

def test_path_contains_files_extensions_jpg_nef(capsys):
    """Test src\\photonomist\\__main__ > path_photos
    """
    sample_path = r'C:\repos\photonomist\test\data\testing_folder_with_photos'
    path_photos(sample_path)
    captured = capsys.readouterr()
    assert r'C:\repos\photonomist\test\data\testing_folder_with_photos\bla\blanef\blablanef\blablablanef' in captured.out
    assert r'C:\repos\photonomist\test\data\testing_folder_with_photos\bla\blabla\blablabla' in captured.out



# Make the script executable.
if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))