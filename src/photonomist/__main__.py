""" Main application entry point.

    python -m photonomist  ...

"""
import os

def path_string(photo_path:str)->str:
    """Verifies that the provided path is string

    :param photo_path: path to photos
    :return: photo to paths
    """
    if (photo_path is None) or (type(photo_path) != str) or (len(photo_path)<3):
        raise Exception("Your input is not valid!")
    return photo_path

def clean_path(photo_path:str)->str:
    """Removes second quotes/apostrophes in case that a user has typed/pasted the path with quote.

    :param photo_path: 'raw' path to photos
    :return: path to photos without redundant quotes
    """
    if ord(photo_path[0]) == 34 or ord(photo_path[0])==39:
        photo_path = photo_path[1:]
    if ord(photo_path[-1]) == 34 or ord(photo_path[-1])==39:
        photo_path = photo_path[:-1]
    return photo_path

def path_exists(photo_path:str):
    """Verifies that the provided path exists.

    :param photo_path: path to photos
    """
    if not os.path.exists(photo_path):
        raise FileNotFoundError("The provided path was not found!")

def path_items(photo_path:str):
    """Verifies that the provided path contains items (not only photos).

    :param photo_path: path to photos
    """
    if not os.listdir(photo_path):
        raise Exception("The provided path does not contain any files!")

def path_photos(photo_path:str):
    """Verifies that the provided path contains items with .jpg and/or .nef extension.

    :param photo_path: path to photos
    """
    pass
    
def main():
    """ Execute the application.

    It asks the user to specify the path to the photos.
    It assesses the validυity of the provided path and verifies that there is enough storage space.

    """
    photo_path = clean_path(path_string(input("Enter the path to your photos: ")))
    path_exists(photo_path)
    path_items(photo_path)


# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(main())
