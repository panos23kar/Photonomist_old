""" Main application

    Run the application (via **Anaconda Command Prompt**):
        python -m photonomist
    |
"""
import os, shutil, subprocess
import collections
from .photo import Photo


def path_string(path:str)->str:
    """Verifies that the provided path is of type string.

    :param path: provided path
    :type path: str

    :return: provided path
    :rtype: str
    |
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
    |
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
    |
    """
    if not os.path.exists(path):
        raise FileNotFoundError("The provided path was not found!")#TODO Log it

def path_items(path:str):
    """Verifies that the provided path contains files (not only photos).

    :param path: provided path
    :type path: str
    |
    """
    if not os.listdir(path):
        raise Exception("The provided path does not contain any files!")#TODO Log it

def traverse_photos_path(photos_path:str)->list:
    """Recursively traverses all the directories under the provided path.
    Identified .jpg, .jpeg .nef and .cr2 files are appended to the photos_roots dictionary.
   
    :param photos_path: path to photos
    :type photos_path: str

    :return: A dictionary with key a path with photos and value a list of .jpg, .jpeg, .nef or .cr2 photos
    :rtype: dict
    |
    """
    photos_roots = collections.defaultdict(list)

    # traverse root directory, and list directories as dirs and files as files. List comp was less readable
    for root, dirs, files in os.walk(photos_path):
        for _file in files:
            if _file.lower().endswith('jpg') or _file.lower().endswith('nef') or _file.lower().endswith('jpeg') or _file.lower().endswith('cr2'):
                photos_roots[root].append(root + '\\' + _file)
    
    return photos_roots

def path_photos(photos_roots:dict):
    """Prints the photo paths. If there aren't any, it raises an error.

    :param photos_roots: a dict with all the paths that contain photos
    :type photos_roots: dict
    |
    """
    if not photos_roots:
        raise Exception("The provided path does not contain any files with .jpg, .jpeg, .nef or .cr2 extension!")#TODO Log it
    else:#TODO Log it
        print('I found photos in: ')
        #print(*photos_roots, sep = "\n")

def photos_size(photos_roots:dict)->int:
    """Calculates the size (in bytes) of all photos found in the provided path.

    :param photos_roots: a dict with all the paths that contain photos
    :type photos_roots: dict

    :return: The total size (in bytes) of photos
    :rtype: int
    |
    """
    # It is an extra loop. I could have generated the total size in traverse_photo_path function
    # With the extra function is more readdable and testable
    total_size = 0
    for photo_list in photos_roots.values():
         for photo in photo_list:
             total_size += os.stat(photo).st_size
    return total_size

def paths_same_disk(photos_path:str, export_path:str)->bool:
    """Checks if the provided input path and the export path are "located" on the same disk.

    :param photos_path: path to photos
    :type photos_path: str
    :param export_path: path to the directory where the photo folder structure will be created
    :type export_path: str
    |
    """
    return True if photos_path[0].lower() == export_path[0].lower() else False

def disk_space(export_path:str, photos_total_size:int):
    """Obtains the total, used and free space of the exported path disk.
    If the total size of the photos is greater than the free space, it raises an exception.

    :param export_path: path to the directory where the photo folder structure will be created
    :type export_path: str
    :param photos_total_size: the total size of photos which were identified in the provided input path
    :type photos_total_size: int
    |
    """
    total, used, free = shutil.disk_usage(export_path)
    if free > photos_total_size:
        print('You have enough free disk space!')
    else:
        raise Exception(f"You need at least {photos_total_size + 1073741824} free bytes but you only have {free} avaialable!")#TODO Log it

def photo_dir_name(date:str)->str:
    """Generates the name of the folder where the photos will be moved according to their dates.
    
    | **Name pattern**: *year_month_day_place_reason_people*
    |
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
    |
    """
    year, month, day = date.split(':')
    return f"{year}_{month}_{day}_place_reason_people"

def dir_name_exists(dir_name:str, export_path:str)->bool:
    """Checks if a folder's name already contains the date of a photo

    :param dir_name: the folder's name to check if exists
    :type dir_name: str
    :param export_path: path to the directory where the photo folder will be created
    :type export_path: str
    |
    """
    for folder_name in os.walk(export_path):
        if os.path.join(export_path, dir_name) == folder_name[0]: 
            return True
    return False

def create_photo_dir(dir_name:str, export_path:str):
    """Creates a folder with the specified name

    :param dir_name: name of the folder to be created
    :type dir_name: str
    :param export_path: path to the directory where the photo folder will be created
    :type export_path: str
    |
    """
    os.makedirs(os.path.join(export_path, dir_name))

def write_not_transferred_photos(photo_path:str, export_path:str):
    """Writes the paths of the photos that was not possible to be transferred. 

    :param photo_path: path to photo
    :type photo_path: str
    :param export_path: path to the directory where the photo folder will be created
    :type export_path: str
    |
    """
    with open(os.path.join(export_path, "not_transferred.txt"), "a") as myfile:
        myfile.write(photo_path + "\n")

def transfer_photo(photo_path:str, export_path:str):
    """Moves a photo to a "date" folder, if a date was extracted.

    :param photo_path: path to photo
    :type photo_path: str
    :param export_path: path to the directory where the photo folder will be created
    :type export_path: str
    |
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

def input_path_validation(photos_path:str)->list:
    """Validates if the provided input path:
    | 1) exists 
    | 2) contains files 
    | 3)contains .jpg, .jpeg, .nef or .cr2 photos

    :param photos_path: path to photos
    :type photos_path: str

    :return: A dictionary with key a path with photos and value a list of .jpg, .jpeg, .nef or .cr2 photos
    :rtype: dict
    |
    """
    path_exists(photos_path)
    path_items(photos_path)

    # Extract photos' paths
    photos_roots = traverse_photos_path(photos_path)
    path_photos(photos_roots)
    return photos_roots

def export_path_validation(export_path:str, photos_path:str, photos_roots:dict):
    """Validates if the export path:
    | 1) exists 
    | 2) there is enough disk space

    :param export_path: path to the directory where the photo folder structure will be created
    :type export_path: str
    :param photos_path: path to photos
    :type photos_path: str
    :param photos_roots: a dict with all the paths that contain photos
    :type photos_roots: dict
    |
    """
    path_exists(export_path)

    # Disk space validation
    if not paths_same_disk(photos_path, export_path):
        photos_total_size = photos_size(photos_roots)
        disk_space(export_path, photos_total_size)

def tidy_photos(export_path:str, photos_roots:dict):
    """Initiates the transfer process for each photo

    :param export_path: path to the directory where the photo folder structure will be created
    :type export_path: str
    :param photos_roots: a dict with all the paths that contain photos
    :type photos_roots: dict
    |
    """

    # Iterate over list of photos
    for photo_list in photos_roots.values():
        for photo in photo_list:
            transfer_photo(photo, export_path)

def replace_backslashes(path:str):
    """Replaces the backslashes of string-paths with double forward slashes

    :param path: a random path that might contain backslashes
    :type path: str

    :return: A string-path with forward slashes 
    :rtype: str
    |
    """
    return path.replace("/", "\\")

def open_export_folder(export_path:str):
    """Opens the export path on file explorer to inform the users that the process is done

    :param export_path: path to the directory where the photo folder structure will be created
    :type export_path: str
    |
    """
    # export_path = replace_backslashes(export_path)
    # subprocess.Popen(f'explorer "{export_path}"')
    subprocess.Popen(f'explorer "{replace_backslashes(export_path)}"')

def main():
    """ Executes the application. It is responsible for getting the user's input, asserting its validity
    and initiating the transfer process

    |
    """
    # Input path 
    photos_path = clean_path(path_string(input("Enter the path to your photos: ")))
    photos_roots = input_path_validation(photos_path)

    # Export path
    export_path = clean_path(path_string(input("Enter the path where your photo-folders will be created: ")))
    export_path_validation(export_path, photos_path, photos_roots)

    # Moves photos
    tidy_photos(export_path, photos_roots)

    # Open export path on file explorer
    open_export_folder(export_path)
     
# Make the script executable.
if __name__ == "__main__":
    raise SystemExit(main())
