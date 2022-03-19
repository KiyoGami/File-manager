import PySimpleGUI as sg
from file_handling import open, create_path, rename, copy, move, delete, create_dir, create_file
from layout import file_details_win_layout
from constants import file_types, key_shortcuts


def show_key_shortcuts():
    msg = ""
    for operation, key in key_shortcuts.items():
        msg += f"{operation}: {key}" + "\n\n"
    sg.popup_no_buttons(
        msg,
        title="",
    )


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


def create_new_file(window, values, curr_dir):
    file_name = new_file_details()
    if file_name:
        error = create_file(curr_dir, file_name)
        if error == "exists":
            file_exists_error()
        elif error == "file name error":
            sg.popup_auto_close(f"The file name, '{file_name}' is invalid.")

    refresh(window, curr_dir)


def create_new_dir(window, values, curr_dir):
    """Creates a new directory in the current directory."""

    dir_name = sg.popup_get_text("Enter the name of the new folder")
    if dir_name:
        error = create_dir(curr_dir, dir_name)
        if error:
            file_exists_error(type="folder")
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

# ------- CREATING NEW FILE ---------


def new_file_details():
    """Gets the file name of the new file to be created. Returns None if the given file details are invalid."""

    # creating new window for user to enter file details
    win = create_file_details_window()
    while True:
        event, values = win.read()
        if event == "cancel":
            win.close()
        elif event == "create_file":
            # getting the file name and file type and returning properly formatted file name if possible
            file_name, file_type = valid_file_details(values)
            if file_name and file_type:
                file_name = formatted_file_name(file_name)
                win.close()
                return file_name + file_type
            if file_name:
                file_type = get_file_type(file_name)
                file_name = formatted_file_name(file_name)
                win.close()
                return file_name + file_type
        elif event == sg.WIN_CLOSED:
            break
    return None


def formatted_file_name(filename):
    return filename.split(".")[0]


def get_file_type(filename):
    return "." + filename.split(".")[1]


def valid_file_details(values):
    """Validates file details and returns filename and file type, whichever ones are available. The ones not available are returned the value of None."""

    file_name = values['file_name']
    file_type = values['file_type']
    if file_name and file_type:
        return file_name, file_types[file_type]
    elif file_name and not file_type:
        # returns the file name if a proper file type can be found from it else an error popup is shown
        if '.' in file_name:
            return file_name, None
        else:
            sg.popup_auto_close(
                "Please select a file type or include it in the file name.", auto_close_duration=4, keep_on_top=True)
    return None, None


def create_file_details_window():
    """Creates the window that will be used to get the details of the file from the user."""

    return sg.Window(
        "File Details",
        layout=file_details_win_layout(),
        no_titlebar=True,
        disable_minimize=True,
        keep_on_top=True,

    )

# ---------- UTILITY FUNCTIONS -----------


def file_exists_error(type="file"):
    """Displays error popup when the operation is not possible because the file/folder already exists."""
    sg.popup_auto_close(f"A {type} already exists!",
                        title="Error", auto_close_duration=4, keep_on_top=True)


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
