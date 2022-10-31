import PySimpleGUI as sg

from constants import file_types
from file_handling import ROOT_DIRECTORIES


def create_layout():

    files = sg.Listbox(
        values=ROOT_DIRECTORIES,
        select_mode="LISTBOX_SELECT_MODE_SINGLE",
        right_click_menu=['&Right',['Back', 'Sort', 'Find', 'Zip', 'Unzip', 'New File', 'New Folder', 'Rename', 'Copy', 'Paste','Move', 'Delete']],
        size=(150, 30),
        # no_scrollbar=True,
        key='options',
        bind_return_key=True,
        expand_y=True

    )

    files_col = [[files]]
    btns_col = create_buttons()

    return [
        # [sg.Text(key='message')],
        create_buttons(),
        [sg.Column(files_col)],
        [sg.Button(image_filename='img_icon\\question.png', key="shortcut_btn",button_color='#FFFFFF',mouseover_colors='#d1d1e0',tooltip="Keyboard Shortcuts")]
    ]


def create_buttons():
    buttons = {
        "back_btn": " Go Back ",
        "new_file_btn": " Create New File ",
        "new_dir_btn": " Create New Folder ",
        "rename_btn": " Rename ",
        "copy_btn": " Copy ",
        "paste_btn": " Paste ",
        "move_btn": " Move ",
        "delete_btn": " Delete ",
        "cancel_btn": " Cancel ",
    }
    btns_col = []
    btns_col.append(sg.Button(image_filename='img_icon\\back.png', key="back_btn", expand_x=True, tooltip=" Go Back ",button_color='#FFFFFF',mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\add-file.png', key="new_file_btn", expand_x=True, tooltip=" Create New File ",button_color='#FFFFFF',mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\add-folder.png', key="new_dir_btn", expand_x=True, tooltip=" Create New Folder ",button_color='#FFFFFF',mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\rename.png', key="rename_btn", expand_x=True, tooltip=" Rename ",button_color='#FFFFFF',mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\copy.png', key="copy_btn", expand_x=True, tooltip=" Copy ",button_color='#FFFFFF',mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\paste.png', key="paste_btn", expand_x=True, tooltip=" Paste ",button_color='#FFFFFF',mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\move.png', key="move_btn", expand_x=True, tooltip=" Move ",button_color='#FFFFFF',mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\delete.png', key="delete_btn", expand_x=True, tooltip=" Delete ",button_color='#FFFFFF',mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\cancel.png', key="cancel_btn", expand_x=True, tooltip=" Cancel ",button_color='#FFFFFF',mouseover_colors='#d1d1e0'))

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
