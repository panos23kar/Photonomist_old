""" Main application // Entry point.

    Run the application (via Command Prompt):
        python -m photonomist
"""
import os, shutil
from .photo import Photo


def path_string(path:str)->str:
    """Verifies that the provided path is of type string.

    :param path: provided path
    :type path: str

    :return: provided path
    :rtype: str
    """
    if (path is None) or (type(path) != str) or (len(path)<3):
        raise Exception("Your input is not a valid path!") #TODO Log it
    return path

def clean_path(path:str)->str:
    """Removes redundant quotes/apostrophes from the provided path.
    (In case a user has typed/pasted the path with quotes)

    :param path: 'raw' path
    :type path: str

    :return: path without redundant quotes
    :rtype: str
    """
    if ord(path[0]) == 34 or ord(path[0])==39:
        path = path[1:]
    if ord(path[-1]) == 34 or ord(path[-1])==39:
        path = path[:-1]
    return path

def path_exists(path:str):
    """Verifies that the provided path exists.

    :param path: provided path
    :type path: str
    """
    if not os.path.exists(path):
        raise FileNotFoundError("The provided path was not found!")#TODO Log it

def path_items(path:str):
    """Verifies that the provided path contains files (not only photos).

    :param path: provided path
    :type path: str
    """
    if not os.listdir(path):
        raise Exception("The provided path does not contain any files!")#TODO Log it

def traverse_photos_path(photos_path:str)->list:
    """Recursively traverses all the directories under the provided path.
    Identified .jpg and .nef files are appended to the photos_roots list.
   
    :param photos_path: path to photos
    :type photos_path: str

    :return: A list with all paths to .jpg or .nef photos
    :rtype: list
    """
    # I could have uused a tuple and overwrite at each iteration
    photos_roots = []

    # traverse root directory, and list directories as dirs and files as files. List comp was less readable
    for root, dirs, files in os.walk(photos_path):
        for _file in files:
            if _file.lower().endswith('jpg') or _file.lower().endswith('nef'):
                if root + '\\' + _file not in photos_roots: photos_roots.append(root + '\\' + _file)
        
    return photos_roots

def path_photos(photos_roots:list):
    """Prints the photo paths. If there aren't any, it raises an error.

    :param photos_roots: list with all roots that contain photos
    :type path: list
    """
    if not photos_roots:
        raise Exception("The provided path does not contain any files with .jpg or .nef extension!")#TODO Log it
    else:#TODO Log it
        print('I found photos in: ')
        print(*photos_roots, sep = "\n")

def photos_size(photos_roots:list)->int:
    """Calculates the size (in bytes) of all photos found in the provided path.

    :param photos_roots: a list with all the roots that point to photos
    :type path: list

    :return: The total size (in bytes) of photos
    :rtype: int
    """
    # It is an extra loop. I could have generated the total size in traverse_photo_path function
    # With the extra function is more readdable and testable
    total_size = 0
    for photo_root in photos_roots:
        total_size += os.stat(photo_root).st_size
    return total_size

def paths_same_disk(photos_path:str, export_path:str)->bool:
    """Checks if the provided input path and the export path are "located" on the same disk.

    :param photos_path: path to photos
    :type photos_path: str
    :param export_path: path to the directory where the photo folder structure will be created
    :type export_path: str
    """
    return True if photos_path[0].lower() == export_path[0].lower() else False

def disk_space(export_path:str, photos_total_size:int):
    """Obtains the total, used and free space of the exported path disk.
    If the total size of the photos is greater than the free space, it raises an exception.

    :param export_path: path to the directory where the photo folder structure will be created
    :type export_path: str
    :param photos_total_size: the total size of photos which were identified in the provided input path
    :type photos_total_size: int
    """
    total, used, free = shutil.disk_usage(export_path)
    if free > photos_total_size:
        print('You have enough free disk space!')
    else:
        raise Exception(f"You need at least {photos_total_size + 1073741824} free bytes but you only have {free} avaialable!")#TODO Log it

def photo_dir_name(date:str)->str:
    """Generates the name of the folder where the photos will be moved according to their dates.
    
    | Name pattern: year_month_day_place_reason_people
    | **Year**      : The year when the photo was captured (photo's metadata)
    | **Month**     : The month when the photo was captured (photo's metadata)
    | **Day**       : The day when the photo was captured (photo's metadata)
    | **Place**     : The city/location/place where the photo was captured (user defined)
    | **Reason**    : The reason why you were there (Ex.: vacation, photo shooting, work) (user defined)
    | **People**    : People with whom you were there (Ex.: family, friend1,friend2, boss) (user defined)
    
    :param date: the date which will be used to populate the first three elements of the folder name
    :type date: str
    :return: the wonna be directory name
    :rtype: str
    """
    year, month, day = date.split(':')
    return f"{year}_{month}_{day}_place_reason_people"

def dir_name_exists(dir_name:str, export_path:str):
    """ Checks if the name of a folder already contains the date of a photo

    :param dir_name: name of the folder to check if exists
    :type dir_name: str
    :param export_path: path to the dir where the photo folder will be created
    :type export_path: str
    """
    for folder_name in os.walk(export_path):
        if os.path.join(export_path, dir_name) == folder_name[0]: 
            return True
    return False

def create_photo_dir(dir_name:str, export_path:str):
    """ Creates a folder with the specified name

    :param dir_name: name of the folder to create
    :type dir_name: str
    :param export_path: path to the dir where the photo folder will be created
    :type export_path: str
    """
    os.makedirs(os.path.join(export_path, dir_name))

def write_not_transferred_photos(photo_path:str, export_path:str):
    """Writes the paths of the photos that was not possible to be transferred. 

    :param photo_path: path to photo
    :type photo_path: str
    :param export_path: path to the dir where the photo folder will be created
    :type export_path: str
    """
    with open(os.path.join(export_path, "not_transerred.txt"), "a") as myfile:
        myfile.write(photo_path + "\n")

def transfer_photo(photo_path:str, export_path:str):
    """ Transfers a photo to a date folder, if date was extracted.

    :param photo_path: path to photo
    :type photo_path: str
    :param export_path: path to the dir where the photo folder will be created
    :type export_path: str
    """
    photo = Photo(photo_path)
    date = photo.get_date()
    
    if date:
        photo_folder_name = photo_dir_name(date)
        if not dir_name_exists(photo_folder_name, export_path):
            # I dont simply use a set because the photo_dir might exist from the past
            create_photo_dir(photo_folder_name, export_path)
        photo.move_to_folder(os.path.join(export_path, photo_folder_name))
    else:
        write_not_transferred_photos(photo_path, export_path)

def main():
    """ Executes the application. It is responsible for getting the user's input, asserting its validity
    and initiate the transfer process
    """

    # Photo path validation
    photos_path = clean_path(path_string(input("Enter the path to your photos: ")))
    path_exists(photos_path)
    path_items(photos_path)

    # Extract paths to photos
    photos_roots = traverse_photos_path(photos_path)
    path_photos(photos_roots)

    # Export path validation
    export_path = clean_path(path_string(input("Enter the path where your photo-folders will be created: ")))
    path_exists(export_path)

    # Disk space validation
    if not paths_same_disk:
        photos_total_size = photos_size(photos_roots)
        disk_space(export_path, photos_total_size)

    # Iterate over list of photos
    for photo_path in photos_roots:
        transfer_photo(photo_path, export_path)
 
# Make the script executable.
if __name__ == "__main__":
    raise SystemExit(main())
