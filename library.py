import os

PATH_FILES = "files"

class LibraryManager:
    def __init__(self):
        pass

    def _init_dir(self):
        """
        Init the 'files' directory
        """
        if not os.path.isdir(PATH_FILES):
            os.makedirs(PATH_FILES)

            # if did not exist, make

class Library:
    def __init__(self, name="Default"):
        self.name = name

    def save(self):
        pass
