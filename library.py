import os
import pyzipper
from util import logger

PATH_FILES = "files"

class LibraryManager:
    def __init__(self):
        self.names = []
        self._cur_library = None

        # init files directory
        if not os.path.isdir(PATH_FILES):
            os.makedirs(PATH_FILES)

            # if did not exist, make default library
            self.new_library("Default")
        else:
            # files directory did exist, so read existing libraries from the folder
            for file in os.listdir(PATH_FILES):
                name, ext = os.path.splitext(file)
                if ext == ".zip":
                    self.names.append(name)

        logger.info("{} libraries detected".format(len(self.names)))

    def new_library(self, name) -> "Library":
        if name in self.names:
            raise KeyError
        else:
            with Library(name) as library:
                library.save()
                self.names.append(name)
                return self.get_library(name)

    def get_library(self, name) -> "Library":
        if name not in self.names:
            raise KeyError
        else:
            if self._cur_library is not None:
                self._cur_library.close()  # dispose of old library if any

            with Library(name) as library:
                self._cur_library = library
                return self._cur_library

    def close(self):
        if self._cur_library is not None:
            self._cur_library.close()

    def __del__(self):
        self.close()

class Library:
    def __init__(self, name):
        self.name = name
        self.path = os.path.join(PATH_FILES, self.name + ".zip")
        self._fh = pyzipper.AESZipFile(self.path, "w")  # file handle. NB: remember to dispose correctly

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def set_password(self, pwd):
        self._fh.setpassword(pwd)

    def save(self):
        pass

    def close(self):
        self._fh.close()

if __name__ == '__main__':
    # for during dev only
    manager = LibraryManager()
    manager.new_library("Bruh")
