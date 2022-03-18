import os
import stat
import string
import shutil
from pathlib import Path


def get_drives():
    """Get all the drives and devices connected on this PC/laptop."""

    drives = []
    for letter in string.ascii_uppercase:
        if os.path.exists(f"{letter}:"):
            drives.append(f"{letter}:")
    return drives


def open(path):
    """Opens the file if the path points to a file or returns a list of the folders/files in that specific directory."""
    # for displaying root directories
    if not path:
        return ROOT_DIRECTORIES

    # opens the choice if it's a file
    if os.path.isfile(path):
        os.startfile(path)
        return None

    # return list of files in the directory chosen
    files = [file for file in os.listdir(path) if not is_hidden(file, path)]
    return files


def create_path(curr_dir, suffix=None, back=False):
    """Creates the appropriate path.

    Parameters
    ----------
    curr_dir: str
              The current directory the user is on.

    back: bool
          If True, it the returned path will be that of the folder just above the current hierarchy. If it's at the root, it will return the same path.
    """
    # path of previous hierarchy
    if back:
        if curr_dir.rstrip("/") in ROOT_DIRECTORIES:
            return ""
        return os.path.dirname(curr_dir)

    # path of chosen file
    if curr_dir:
        return os.path.join(curr_dir, suffix)
    return suffix + "/"


def is_hidden(file, path):
    # todo: fix isse of not finding all hidden files
    """Checks if the file/folder is hidden or not."""
    full_file_path = os.path.join(path, file)
    if file[0] == "$" or file[0] == ".":
        return True

    return False


def rename(curr_dir, old_name, new_name):
    """Renames the chosen file to the new name."""
    old_name = create_path(curr_dir, old_name)
    new_name = create_path(curr_dir, new_name)
    os.rename(old_name, new_name)


def move(dst, file_to_move):
    """Moves the file to the paste location. Returns True if there was a FileExistsError."""

    try:
        shutil.move(file_to_move, dst)
    except shutil.Error:
        return True
    return False


def copy(dst, file_to_copy):
    """Copies a file to the paste location."""
    if os.path.isfile(file_to_copy):
        shutil.copy(file_to_copy, dst)
    else:
        file = Path(file_to_copy).stem
        dst = os.path.join(dst, file)
        shutil.copytree(file_to_copy, dst)


ROOT_DIRECTORIES = get_drives()
