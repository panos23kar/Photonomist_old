""" This module hosts the Photo class 

"""
import exifread
import os, shutil

class Photo:
    """This class is used to represent a photo.
    A photo object holds a photo's metadata and methods to return it.
    It can also move itself to another directory

    :param photo_path: Path to photos
    :type photo_path: str
    """

    def __init__(self, photo_path:str):
        """Constructor method
        """
        self.path = photo_path
        self.metadata_dict()
    
    def __str__(self)->str:
        """Returns the string representation (name) of the photo

        :return: name of the photo
        :rtype: str
        """
        return os.path.split(self.path)[1]

    def extract_exif_tags(self):
        """Extracts the metadata tags from a photo using `exifread <https://exif-py.readthedocs.io/en/latest/>`_ library.
        It contains duplicate values with different tags.
        """
        self.tags = {}
        try:
            photo_file = open(self.path, 'rb')
            self.tags = exifread.process_file(photo_file, details=False)
        except:
            print("I didn't manage to extract photo's tags!")
            #self.tags = 'NoTags' # I didn't use None because of the check in metadata_dict

    def metadata_dict(self):
        """Populates the metadata dictionary with all key tags that contain values.
        It also avoids duplicate keys with different tags:

        | *Example:*
        | *Image DateTimeOriginal, value 2019:12:14 15:04:33*
        | *EXIF DateTimeOriginal, value 2019:12:14 15:04:33*
        """
        self.extract_exif_tags()
        self.metadata = {}
        
        if self.tags:
            for tag_key in self.tags.keys():
                key_no_tag = tag_key.split()[1]
                if (len(str(self.tags[tag_key]))>0) and (key_no_tag not in self.metadata): #len(str(self.tags[tag_key]))>0 because ``if self.tags[tag_key]`` doesn't work
                    self.metadata[key_no_tag] = self.tags[tag_key]

    def get_date(self)->str:
        """Returns the date of a photo from the metadata dictionary
        
        :return: date of photo
        :rtype: str
        """
        if self.metadata and "DateTimeOriginal" in self.metadata:
            date = str(self.metadata["DateTimeOriginal"]).split()[0]
            return date
        else:
            return None
    
    def move_to_folder(self, new_folder_path:str):
        """Moves the photo to a new directory.
        If directory doesn't exist it creates one

        :param new_folder_path: the path to dir where the photo will be moved to
        :type new_folder_path: str
        """
        new_path = os.path.join(new_folder_path, self.__str__())        
        try:
            shutil.move(self.path, new_path)
        except:
            os.makedirs(new_folder_path)
            shutil.move(self.path, new_path)
            self.path = new_path


if __name__ == "__main__":
    #kati = Photo(r"C:\repos\photonomist\test\data\testing_folder_with_photos\bla\DSC_0262.NEF")
    #kati.extract_exif_tags()
    #kati.metadata_dict()
    # for key,value in kati.metadata.items():
    #     print(f"key--> {key} \t\t value--> {value}")
    #print(kati)
    #kati.move_to_folder(r"C:\repos\photonomist\test\data\testing_folder_with_photos\move_folder")
    #photo_path = r"C:\Users\potis\Pictures\2016\2016-08-31\IMG-20160831-WA0020.jpg"
    photo_path = r"C:\Users\potis\Pictures\Lg_G3_14-12-2016\Facebook\FB_IMG_1470137678394.jpg"
    my_photo = Photo(photo_path).get_date()