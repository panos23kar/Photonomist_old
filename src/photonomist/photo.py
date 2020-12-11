""" This module hosts the Photo class 
"""
import exifread
import os, shutil
import re 

class Photo:
    """This class is used to represent a photo.
    A photo object holds a photo's metadata.
    It can also move itself to another directory and return its captured date.

    :param photo_path: Path to photo
    :type photo_path: str
    |
    """

    def __init__(self, photo_path:str):
        """Constructor method
        |
        """
        self.path = photo_path
        self.__metadata_dict()
    
    def __str__(self)->str:
        """Returns the name of the photo.

        :return: name of the photo
        :rtype: str
        |
        """
        return os.path.split(self.path)[1]

    def __extract_exif_tags(self):
        """Extracts the metadata tags from a photo using `exifread <https://exif-py.readthedocs.io/en/latest/>`_ library.
        It contains duplicate values with different tags.
        
        |
        """
        self.__tags = {}
        try:
            photo_file = open(self.path, 'rb')
            # details=False --> Faster Processing: Don’t process makernote tags, don’t extract the thumbnail image (if any).
            self.__tags = exifread.process_file(photo_file, details=False)
        except: #TODO Log it
            print("I didn't manage to extract photo's tags!")

    def __metadata_dict(self):
        """Populates the metadata dictionary with all key/tags (extracted using the 
        `exifread <https://exif-py.readthedocs.io/en/latest/>`_ library) that contain values.
        It also avoids duplicate keys with different tags:

        | *Example:*
        | *Image DateTimeOriginal, value 2019:12:14 15:04:33*
        | *EXIF DateTimeOriginal, value 2019:12:14 15:04:33*
        |
        """
        self.__extract_exif_tags()
        self.metadata = {}
        
        if self.__tags:
            for tag_key in self.__tags.keys():
                # Image DateTimeOriginal = 2019:12:14 15:04:33 --> tag = Image || key = DateTimeOriginal || value = 2019:12:14 15:04:33
                key_no_tag = tag_key.split()[1]

                #len(str(self.__tags[tag_key]))>0 because self.__tags[tag_key] doesn't work
                if (len(str(self.__tags[tag_key]))>0) and (key_no_tag not in self.metadata):
                    self.metadata[key_no_tag] = self.__tags[tag_key]

    def get_date(self)->str:
        """Returns the date of a photo from the metadata dictionary. 
        As date considered the value of the "DateTimeOriginal" tag. 
        
        :return: date of photo
        :rtype: str
        |
        """
        if self.metadata and "DateTimeOriginal" in self.metadata:
            date = str(self.metadata["DateTimeOriginal"]).split()[0]
            return date
        else:
            return None

    def find_parentheses_numbers(self, new_path:str):
        """Finds all set of parentheses which contain a number

        :param new_path: the path to the destination folder together with photo's name
        :type new_path: str

        :return: a list of tupes with the start and finish indices of parentheses with numbers 
        :rtype: list
        |
        """
        return [(m.start(0), m.end(0)) for m in re.finditer(r'\([1-9][0-9]*\)', new_path)]


    def construct_new_photo_path(self, filepath:str, counter:int, extension:str):
        """Appends a set of parentheses with a number indicating how many times the specified photo exists.

        :param filepath: the path to the destination folder with photo's name
        :type filepath: str

        :param counter: a number indicating the number of occurrences of the photo in the destination folder
        :type counter: int

        :param extension: file extension of the photo
        :type extension: str

        :return: the path to the destination folder together with photo's name and a set of parentheses with a number
        :rtype: str
        |
        """
        return filepath + f"({counter})" + extension


    def check_same_name(self, new_path:str):
        """Checks if the photo which is being transfered already exists in the destination folder.

        :param new_path: the path to the destination folder together with photo's name
        :type new_path: str

        :return: the path to the destination folder together with photo's name and a set of parentheses with a number (if this photo already exists)
        :rtype: str
        |
        """
        counter = 1
        while os.path.exists(new_path):
            filepath, file_extension = os.path.splitext(new_path)
            if counter >= 2:
                matches_list = self.find_parentheses_numbers(new_path)
                new_path = self.construct_new_photo_path(new_path[:matches_list[-1][0]], counter, file_extension)
            else:
                new_path = self.construct_new_photo_path(filepath, counter, file_extension)
            counter += 1
        return new_path
    
    def move_to_folder(self, new_folder_path:str):
        """If a photo's path is different than the destination path, moves the photo to the destination folder.
        If directory doesn't exist it creates one.

        :param new_folder_path: the path to directory
        :type new_folder_path: str
        |
        """
        new_path = os.path.join(new_folder_path, self.__str__())        
        try:
            if self.path != new_path:
                self.check_same_name(new_path)
                shutil.move(self.path, new_path)
        except:
            os.makedirs(new_folder_path)
            shutil.move(self.path, new_path)
        finally:
            self.path = new_path


if __name__ == "__main__":
    #pass
    #photo_path = Photo(r"C:\repos\photonomist\test\data\testing_folder_with_photos\bla\DSC_0262.NEF")
    photo_path = Photo(r"C:\Users\potis\Pictures\photonomist\0_test\20160815_005049.jpg")
    #my_photo = Photo(photo_path).get_date()
    photo_path.move_to_folder(r"C:\Users\potis\Pictures\photonomist\0_test\2016_08_15_place_reason_people")