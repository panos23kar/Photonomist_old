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
            print("I didn't manage to extract photo's tags!")
            self.tags = 'NoTags' # I didn't use None because of the check in metadata_dict

    def metadata_dict(self):
        """Populates the metadata dictionary with all key tags that contain values.
        It also avoids duplicate keys with different tags:
        *Example: 
        Image DateTimeOriginal, value 2019:12:14 15:04:33
        EXIF DateTimeOriginal, value 2019:12:14 15:04:33
        *
        """
        # if not self.tags:
        #     self.extract_exif_tags()
        try:
            self.tags
        except:
            self.extract_exif_tags()
        
        self.metadata = {}
        for tag_key in self.tags.keys():
            key_no_tag = tag_key.split()[1]
            if (len(str(self.tags[tag_key]))>0) and (key_no_tag not in self.metadata): #len(str(self.tags[tag_key]))>0 because ``if self.tags[tag_key]`` doesn't work
                self.metadata[key_no_tag] = self.tags[tag_key]

if __name__ == "__main__":
    kati = Photo(r"C:\repos\photonomist\test\data\testing_folder_with_photos\bla\DSC_0262.NEF")
    #kati.extract_exif_tags()
    kati.metadata_dict()
    for key,value in kati.metadata.items():
        print(f"key--> {key} \t\t value--> {value}")