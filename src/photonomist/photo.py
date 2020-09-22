""" This module hosts the Photo class 

"""
class Photo:
    """This class is used to represent a photo.
    A photo object holds a photo's metadata and methods to return it.
    It can also move itself to another directory

    :param photo_path: Path to photos
    :type photo_path: str
    """

    def __init__(self, photo_path):
        self.original_path = photo_path