import os
import pyzipper

PATH_FILES = "files"

class LibraryManager:
    def __init__(self):
        self.libraries = set()  # set is like list but no duplicates
        self._cur_library = None

        # init files directory
        if not os.path.isdir(PATH_FILES):
            os.makedirs(PATH_FILES)

            # if did not exist, make default library
            with Library("Default") as default_library:
                default_library.save()
        else:
            # files directory did exist, so read existing libraries from the folder
            pass

    def new_library(self, name) -> "Library":
        with Library(name) as library:
            library.save()
            self.libraries.add(name)
            return self.get_library(name)

    def get_library(self, name) -> "Library":
        if name not in self.libraries:
            raise KeyError
        else:
            if self._cur_library is not None:
                self._cur_library.close()  # dispose of old library if any
            self._cur_library = Library(name)
            return self._cur_library

    def __del__(self):
        self._cur_library.close()

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
