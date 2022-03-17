import os
import string
import PySimpleGUI as sg
from file_handling import open, create_path

curr_dir = ""


def get_drives():
    """Get all the drives and devices connected on this PC/laptop."""
    drives = []
    for letter in string.ascii_uppercase:
        if os.path.exists(f"{letter}:"):
            drives.append(f"{letter}:")
    return drives


# ---------- GUI UPDATE FUNCTIONS -----------
def update_options(choices):
    """Updates the Listbox showing all the folders/files with the given ones."""
    lb = window.find_element("options")
    lb.update(choices)

# ---------- WINDOW LAYOUT ----------


drives = get_drives()
drives_list = sg.Listbox(
    values=drives,
    select_mode="LISTBOX_SELECT_MODE_SINGLE",
    size=(50, 50),
    no_scrollbar=True,
    key='options',
    bind_return_key=True
)

layout = [[drives_list, sg.Button("Open", key='open_btn')]]

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
        choice = values['options'][0]
        path = create_path(choice, curr_dir)
        new_choices = open(path)
        print(path)
        if new_choices is not None:
            curr_dir = path
            update_options(new_choices)

window.close()
