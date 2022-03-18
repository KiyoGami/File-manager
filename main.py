import PySimpleGUI as sg
from file_handling import open, create_path, ROOT_DIRECTORIES, rename, copy, move

# ---------- VARIABLES --------

# stores the current directory the user is on
curr_dir = ""
# the filepath of the file to be copied
file_to_copy = ""
# filepath of file to be moved
file_to_move = ""

# ---------- EVENT FUNCTIONS -----------


def update_options(new_files):
    """Updates the Listbox showing all the folders/files with the given ones."""

    lb = window.find_element("options")
    lb.update(new_files)


def select_file():
    """Opens the file or folder selected by the user."""

    choice = values['options'][0]
    path = create_path(curr_dir, choice)
    new_files = open(path)
    if new_files is not None:
        update_options(new_files)
    return path


def rename_file():
    """Renames selected file."""

    if values['options']:
        new_name = sg.popup_get_text(
            "Enter the new name:",
            title="Rename",
        )
        rename(curr_dir, values['options'][0], new_name)
        refresh()
    else:
        no_file_error()


def copy_file():
    """Gets filepath of file to copy."""
    if values['options']:
        file_to_copy = create_path(curr_dir, values['options'][0])
    else:
        no_file_error()


def paste_file():
    """Pastes the file in the current directory."""

    if file_to_copy:
        copy(curr_dir, file_to_copy)
        refresh()
    else:
        no_file_error()


def move_file(file):
    """Moves selected file."""
    if not window['move_btn'].metadata and not values['options']:
        no_file_error()
        return

    if update_move_btn():
        file = create_path(curr_dir, values['options'][0])
        toggle_all_btns(exceptions=["move_btn", "back_btn"])
    else:
        error = move(curr_dir, file)
        if error:
            sg.popup_error("A file with that name exists here already!")
            update_move_btn()
        else:
            toggle_all_btns(disable=False)
            refresh()

    return file


def update_move_btn():
    """Updates the name of the move button when moving files. Returns True if a file is being moved."""
    move_btn = window['move_btn']

    # metadata of move_btn will decide if a file is being moved or not
    # if metadata is True, then a file is being moved
    if not move_btn.metadata:
        move_btn.update(text="Move Here")
        move_btn.metadata = True
    else:
        move_btn.update(text="Move")
        move_btn.metadata = False

    return move_btn.metadata


def go_back():
    """Goes back a hierarchy."""

    path = create_path(curr_dir, back=True)
    new_files = open(path)
    update_options(new_files)

    return path


def refresh():
    """Refreshes the Listbox by refreshing the files in the current directory."""
    new_files = open(curr_dir)
    update_options(new_files)


def no_file_error(msg="No file was chosen!"):
    """Displays erorr popup when no file is chosen."""

    sg.popup_auto_close(msg,
                        title="Error", auto_close_duration=3)


def toggle_all_btns(disable=True, exceptions=[]):
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


# ---------- WINDOW LAYOUT ----------
files = sg.Listbox(
    values=ROOT_DIRECTORIES,
    select_mode="LISTBOX_SELECT_MODE_SINGLE",
    size=(50, 50),
    no_scrollbar=True,
    key='options',
    bind_return_key=True
)

files_col = [[files]]
buttons = {
    "back_btn": "Go Back",
    "rename_btn": "Rename",
    "copy_btn": "Copy",
    "paste_btn": "Paste",
    "move_btn": "Move",
}
btns_col = [[sg.Button(value, key=key)] for key, value in buttons.items()]

layout = [
    [sg.Text(key='message')],
    [sg.Column(files_col), sg.Column(btns_col)]
]

# ------- CREATING WINDOW -------
window = sg.Window(
    "File Explorer",
    layout,
    grab_anywhere=True,
    resizable=True)

# ------- EVENT LOOP -------
while True:
    event, values = window.read()
    # quit the program if the window is closed
    if event == sg.WINDOW_CLOSED:
        break
    # open the file or folder when the option is double clicked
    if event == 'options':
        curr_dir = select_file()
    # go back one hierarchy
    if event == 'back_btn':
        curr_dir = go_back()
    # rename file/folder
    if event == 'rename_btn':
        rename_file()
    # copy files/folders
    if event == "copy_btn":
        copy_file()
    # paste copied files/folders
    if event == "paste_btn":
        paste_file()
    # move files/folders
    if event == "move_btn":
        file_to_move = move_file(file_to_move)

window.close()
