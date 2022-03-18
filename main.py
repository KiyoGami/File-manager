import PySimpleGUI as sg
from file_handling import ROOT_DIRECTORIES
from keyboard_values import keyboard_values as kv
from event_functions import *
from layout import create_layout

# ---------- VARIABLES --------

# stores the current directory the user is on
curr_dir = ""
# the filepath of the file to be copied
file_to_copy = ""
# filepath of file to be moved
file_to_move = ""

# ------- CREATING WINDOW -------
window = sg.Window(
    "File Explorer",
    create_layout(),
    grab_anywhere=True,
    resizable=True,
    return_keyboard_events=True,
    use_default_focus=False)

# setting focus
# window.find_element('options').set_focus(True)

# ------- EVENT LOOP -------
while True:
    event, values = window.read()
    # open the file or folder when the option is double clicked
    if event in ("options", kv['open']):
        curr_dir = select_file(window, values, curr_dir)
    # go back one hierarchy
    elif event in ("back_btn", kv['back']):
        curr_dir = go_back(window, curr_dir)
    # rename file/folder
    elif event in ('rename_btn', kv['rename']):
        rename_file(window, values, curr_dir)
    # copy files/folders
    elif event in ('copy_btn', kv['copy']):
        file_to_copy = copy_file(values, curr_dir)
    # paste copied files/folders
    elif event in ('paste_btn', kv['paste']):
        paste_file(window, curr_dir, file_to_copy)
    # move files/folders
    elif event in ('move_btn', kv['move']):
        file_to_move = move_file(window, values, curr_dir, file_to_move)
    elif event in ('delete_btn', kv['delete']):
        delete_file(window, values, curr_dir)
    # cancel current operation
    elif event in ('cancel_btn', 'cancel'):
        file_to_copy, file_to_move = cancel(window)
    # quit the program if the window is closed
    elif event == sg.WINDOW_CLOSED:
        break


window.close()
