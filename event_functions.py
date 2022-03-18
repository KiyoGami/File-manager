import PySimpleGUI as sg
from file_handling import open, create_path, ROOT_DIRECTORIES, rename, copy, move, delete


def select_file(window, values, curr_dir):
    """Opens the file or folder selected by the user."""
    if not values['options']:
        no_file_error()
        return curr_dir

    choice = values['options'][0]
    path = create_path(curr_dir, choice)
    new_files = open(path)
    if new_files is None:
        path = create_path(path, back=True)
        print(path)
    else:
        update_options(window, new_files)
    return path


def rename_file(window, values, curr_dir):
    """Renames selected file."""

    if values['options']:
        new_name = sg.popup_get_text(
            "Enter the new name:",
            title="Rename",
        )
        if new_name:
            rename(curr_dir, values['options'][0], new_name)
            refresh(window, curr_dir)
    else:
        no_file_error()


def copy_file(values, curr_dir):
    """Gets filepath of file to copy."""
    if values['options']:
        file_to_copy = create_path(curr_dir, values['options'][0])
    else:
        file_to_copy = ""
        no_file_error()
    return file_to_copy


def paste_file(window, curr_dir, file_to_copy):
    """Pastes the file in the current directory."""

    if file_to_copy:
        copy(curr_dir, file_to_copy)
        refresh(window, curr_dir)
    else:
        no_file_error()


def move_file(window, values, curr_dir, file):
    """Moves selected file."""

    if not window['move_btn'].metadata and not values['options']:
        no_file_error()
        return

    if update_move_btn(window):
        file = create_path(curr_dir, values['options'][0])
        toggle_all_btns(window, exceptions=[
                        "move_btn", "back_btn", "cancel_btn"])
    else:
        error = move(curr_dir, file)
        if error:
            sg.popup_error("A file with that name exists here already!")
            update_move_btn(window)
        else:
            toggle_all_btns(window, disable=False)
            refresh(window, curr_dir)

    return file


def delete_file(window, values, curr_dir):
    """Deletes chosen file."""
    # error if no file is chosen
    if not values['options']:
        no_file_error()
        return

    confirm = sg.popup_yes_no(
        f"Are you sure you want to delete '{values['options'][0]}'?", title="Delete")
    if confirm == "Yes":
        error = delete(curr_dir, values['options'][0])
        if error:
            sg.popup(
                "A file in that diretory is currently under use. Please close it and try again.", title="Error")
        refresh(window, curr_dir)


def go_back(window, curr_dir):
    """Goes back a hierarchy."""

    path = create_path(curr_dir, back=True)
    new_files = open(path)
    update_options(window, new_files)

    return path


def cancel(window):
    """Cancels all file operations such as copying, moving etc."""

    update_move_btn(window, cancel=True)
    toggle_all_btns(window, disable=False)
    return "", ""

# ---------- UTILITY FUNCTIONS -----------


def update_options(window, new_files):
    """Updates the Listbox showing all the folders/files with the given ones."""

    lb = window.find_element("options")
    lb.update(new_files)


def refresh(window, curr_dir):
    """Refreshes the Listbox by refreshing the files in the current directory."""
    new_files = open(curr_dir)
    update_options(window, new_files)


def no_file_error(msg="No file was chosen!"):
    """Displays erorr popup when no file is chosen."""

    sg.popup_auto_close(msg,
                        title="Error", auto_close_duration=3)


def update_move_btn(window, cancel=False):
    """Updates the name of the move button when moving files. Returns True if a file is being moved."""
    move_btn = window['move_btn']

    # metadata of move_btn will decide if a file is being moved or not
    # if metadata is True, then a file is being moved
    if not move_btn.metadata and not cancel:
        move_btn.update(text="Move Here")
        move_btn.metadata = True
    elif move_btn.metadata or cancel:
        move_btn.update(text="Move")
        move_btn.metadata = False

    return move_btn.metadata


def toggle_all_btns(window, disable=True, exceptions=[]):
    """Disables or enables all the buttons on the window. If exceptions are given then those buttons are ignored.

    Parameters
    ----------
    exceptions: list
                List of the keys of the buttons to ignore.
    """

    all_elements = window.element_list()
    for element in all_elements:
        if isinstance(element, sg.Button):
            if element.Key not in exceptions:
                element.update(disabled=disable)
