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

def test_is_photo_object():
    """Test src\\photonomist\\photo.Photo> __init__

    """
    photo_path = r"a\\random\\path\\to\\a\\photo"
    my_photo = Photo(photo_path)
    assert isinstance(my_photo, Photo)