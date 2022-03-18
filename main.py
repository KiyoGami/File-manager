import PySimpleGUI as sg
from file_handling import open, create_path, ROOT_DIRECTORIES, rename

# stores the current directory the user is on
curr_dir = ""

# ---------- GUI UPDATE FUNCTIONS -----------


def update_options(new_files):
    """Updates the Listbox showing all the folders/files with the given ones."""
    
    lb = window.find_element("options")
    lb.update(new_files)


def refresh():
    """Refreshes the Listbox by refreshing the files in the current directory."""

    new_files = open(curr_dir)
    update_options(new_files)


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
btns_col = [
    [sg.Button("Go Back", key='back_btn')],
    [sg.Button("Rename", key="rename-btn")]
]

layout = [
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
        choice = values['options'][0]
        path = create_path(curr_dir, choice)
        new_files = open(path)
        if new_files is not None:
            curr_dir = path
            update_options(new_files)
        print(curr_dir)

    # go back one hierarchy
    if event == 'back_btn':
        curr_dir = create_path(curr_dir, back=True)
        new_files = open(curr_dir)
        update_options(new_files)

    # rename file/folder
    if event == 'rename-btn':
        if values['options']:
            new_name = sg.popup_get_text(
                "Enter the new name:",
                title="Rename",
            )
            rename(curr_dir, values['options'][0], new_name)
            refresh()
        else:
            sg.popup_auto_close("No file was chosen!",
                                title="Error", auto_close_duration=3)

window.close()
