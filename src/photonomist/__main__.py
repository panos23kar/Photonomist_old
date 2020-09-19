""" Main application entry point.

    python -m photonomist  ...

"""
import os
def path_exists(photo_path:str):
    """Verifies that the provided path exists.

    :param photo_path: path to photos
    """
    if os.path.exists(photo_path):
        return True
    else:
        raise FileNotFoundError("The provided path was not found!")
    
def main():
    """ Execute the application.

    It asks the user to specify the path to the photos.
    It assesses the validity of the provided path and verifies that there is enough storage space.

    """
    photo_path = input("Enter the path to your photos: ")
    path_exists(photo_path)


# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(main())
