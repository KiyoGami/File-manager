import os


def open(path):
    """Opens the file if the path points to a file or returns a list of the folders/files in that specific directory."""
    if os.path.isfile(path):
        os.startfile(path)
        return None

    return os.listdir(path)


def create_path(suffix, curr_dir):
    """Creates the appropriate path for the chosen folder/file."""
    if curr_dir:
        return curr_dir + "/" + suffix
    return curr_dir + suffix
