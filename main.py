import PySimpleGUI as sg
from constants import keyboard_values as kv
import event_functions as ef
from layout import create_layout

# ---------- VARIABLES --------

# stores the current directory the user is on
curr_dir = ""
# the filepath of the file to be copied
file_to_copy = ""
# filepath of file to be moved
file_to_move = ""

# ------- SETTING THEME ------
sg.theme("DarkAmber")

# ------- CREATING WINDOW -------
window = sg.Window(
    "File Explorer",
    create_layout(),
    grab_anywhere=True,
    resizable=True,
    return_keyboard_events=True,
    use_default_focus=False,
    use_ttk_buttons=True,
    finalize=True,
)

# setting focus
window.find_element('options').set_focus(True)

# ------- EVENT LOOP -------
while True:
    event, values = window.read()
    # open the file or folder when the option is double clicked
    if event in ("options", kv['open']):
        curr_dir = ef.select_file(window, values, curr_dir)
    # go back one hierarchy
    elif event in ("back_btn", kv['back']):
        curr_dir = ef.go_back(window, curr_dir)
    # rename file/folder
    elif event in ('rename_btn', kv['rename']):
        ef.rename_file(window, values, curr_dir)
    # copy files/folders
    elif event in ('copy_btn', kv['copy']):
        file_to_copy = ef.copy_file(values, curr_dir)
    # paste copied files/folders
    elif event in ('paste_btn', kv['paste']):
        ef.paste_file(window, curr_dir, file_to_copy)
    # move files/folders
    elif event in ('move_btn', kv['move']):
        file_to_move = ef.move_file(window, values, curr_dir, file_to_move)
    elif event in ('delete_btn', kv['delete']):
        ef.delete_file(window, values, curr_dir)
    # cancel current operation
    elif event in ('cancel_btn', kv['cancel']):
        file_to_copy, file_to_move = ef.cancel(window)
    # new file
    elif event in ('new_file_btn', kv["new_file"]):
        ef.create_new_file(window, values, curr_dir)
    # new folder
    elif event in ('new_dir_btn', kv["new_dir"]):
        ef.create_new_dir(window, values, curr_dir)
    # show keyboard shortcuts
    elif event in ('shortcut_btn', kv["key_shortcuts"]):
        ef.show_key_shortcuts()
    # quit the program if the window is closed
    elif event == sg.WINDOW_CLOSED:
        break


window.close()
