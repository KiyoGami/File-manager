import PySimpleGUI as sg
from file_handling import ROOT_DIRECTORIES
from constants import file_types


def create_layout():

    files = sg.Listbox(
        values=ROOT_DIRECTORIES,
        select_mode="LISTBOX_SELECT_MODE_SINGLE",
        size=(50, 30),
        # no_scrollbar=True,
        key='options',
        bind_return_key=True,
        expand_y=True
    )

    files_col = [[files]]
    btns_col = create_buttons()

    return [
        # [sg.Text(key='message')],
        [sg.Column(files_col), sg.Column(btns_col)],
        [sg.Button("Keyboard Shortcuts", key="shortcut_btn")]

    ]


def create_buttons():
    buttons = {
        "back_btn": "Go Back",
        "new_file_btn": "Create New File",
        "new_dir_btn": "Create New Folder",
        "rename_btn": "Rename",
        "copy_btn": "Copy",
        "paste_btn": "Paste",
        "move_btn": "Move",
        "delete_btn": "Delete",
        "cancel_btn": "Cancel",
    }
    btns_col = []
    i = 1
    no_of_btns = len(buttons)
    for key, value in buttons.items():
        btns_col.append([sg.Button(value, key=key, expand_x=True)])
        if i < no_of_btns:
            btns_col.append([sg.HorizontalSeparator()])
        i += 1
    return btns_col


def file_details_win_layout():

    file_type_options = [
        key + f" ({value})" for key, value in file_types.items()]

    return [
        [sg.Text("Name of new file:"), sg.InputText(key="file_name")],
        [sg.Text("File Type: "), sg.OptionMenu(
            file_type_options, key="file_type")],
        [sg.Button("Create File", key="create_file"), sg.Cancel(key="cancel")]
    ]
