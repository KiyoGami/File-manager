import PySimpleGUI as sg
from file_handling import ROOT_DIRECTORIES


def create_layout():

    files = sg.Listbox(
        values=ROOT_DIRECTORIES,
        select_mode="LISTBOX_SELECT_MODE_SINGLE",
        size=(50, 50),
        no_scrollbar=True,
        key='options',
        bind_return_key=True
    )

    files_col = [[files]]
    btns_col = create_buttons()

    return [
        [sg.Text(key='message')],
        [sg.Column(files_col), sg.Column(btns_col)]
    ]


def create_buttons():
    buttons = {
        "back_btn": "Go Back",
        "rename_btn": "Rename",
        "copy_btn": "Copy",
        "paste_btn": "Paste",
        "move_btn": "Move",
        "delete_btn": "Delete"
    }
    btns_col = [[sg.Button(value, key=key)] for key, value in buttons.items()]
    btns_col.append([sg.Cancel(key="cancel_btn")])

    return btns_col
