""" Main application entry point.

    python -m photonomist  ...

"""
def main():
    """ Execute the application.

    It asks the user to specify the path to the photos.
    It assesses the validity of the provided path and verifies that there is enough storage space.

    """
    photo_path = input("Enter the path to your photos: ")


# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(main())
