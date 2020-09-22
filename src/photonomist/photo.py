""" This module hosts the Photo class 

"""
import exifread

class Photo:
    """This class is used to represent a photo.
    A photo object holds a photo's metadata and methods to return it.
    It can also move itself to another directory

    :param photo_path: Path to photos
    :type photo_path: str
    """

    def __init__(self, photo_path):
        """Constructor method
        """
        self.original_path = photo_path

    def extract_exif_tags(self):
        """Extracts the metadata tags from a photo using `exifread <https://exif-py.readthedocs.io/en/latest/>`_ library.
        It contains duplicate values with different tags.
        """
        try:
            photo_file = open(self.original_path, 'rb')
            self.tags = exifread.process_file(photo_file, details=False)
        except:
            self.tags = None

if __name__ == "__main__":
    kati = Photo(r"C:\repos\photonomist\test\data\testing_folder_with_photos\bla\DSC_0262.NEF")
    kati.extract_exif_tags()
    #print(type(tags))
    for tag in kati.tags.keys():
        print(f"Key: {tag}, value {kati.tags[tag]}")