import PySimpleGUI as sg

from constants import file_types
from file_handling import ROOT_DIRECTORIES


def create_layout():

    files = sg.Listbox(
        values=ROOT_DIRECTORIES,
        select_mode="LISTBOX_SELECT_MODE_SINGLE",
        right_click_menu=['&Right',['Back', 'Sort', 'Find', 'Zip', 'Unzip', 'New File', 'New Folder', 'Rename', 'Copy', 'Paste','Move', 'Delete']],
        size=(150, 30),
        background_color="#ffffff",
        text_color="black",
        sbar_arrow_color='#dfdfec',
        sbar_background_color="#efeff5",
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
        [sg.Button(image_filename='img_icon\\question.png', key="shortcut_btn",button_color='#FFFFFF',
                   mouseover_colors='#d1d1e0',tooltip="Keyboard Shortcuts")]
    ]


def create_buttons():
    buttons = {
        "back_btn": " Go Back ",
        "sort": " Sort ",
        "find_btn": " Find ",
        "zip_btn": " Zip ",
        "unzip_btn": " UnZip ",
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

    # for key, value in buttons.items():
    #     s=key+".png"
    #     btns_col.append(sg.Button(image_filename=s, key=key, expand_x=True))

    btns_col.append(sg.Button(image_filename='img_icon\\back_btn.png', key="back_btn", expand_x=True, tooltip=" Go Back ",
                              button_color='#FFFFFF',mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\new_file_btn.png', key="new_file_btn", expand_x=True, tooltip=" Create New File ",
                              button_color='#FFFFFF',mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\new_dir_btn.png', key="new_dir_btn", expand_x=True, tooltip=" Create New Folder ",
                              button_color='#FFFFFF',mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\rename_btn.png', key="rename_btn", expand_x=True, tooltip=" Rename ",
                              button_color='#FFFFFF',mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\copy_btn.png', key="copy_btn", expand_x=True, tooltip=" Copy ",
                              button_color='#FFFFFF',mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\paste_btn.png', key="paste_btn", expand_x=True, tooltip=" Paste ",
                              button_color='#FFFFFF',mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\move_btn.png', key="move_btn", expand_x=True, tooltip=" Move ",
                              button_color='#FFFFFF',mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\zip_btn.png', key="zip_btn", expand_x=True, tooltip=" Zip ",
                              button_color='#FFFFFF', mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\unzip_btn.png', key="unzip_btn", expand_x=True, tooltip=" UnZip ",
                              button_color='#FFFFFF', mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\sort.png', key="sort", expand_x=True, tooltip=" Sort ",
                              button_color='#FFFFFF', mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\find_btn.png', key="find_btn", expand_x=True, tooltip=" Find ",
                              button_color='#FFFFFF', mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\delete_btn.png', key="delete_btn", expand_x=True, tooltip=" Delete ",
                              button_color='#FFFFFF',mouseover_colors='#d1d1e0'))
    btns_col.append(sg.Button(image_filename='img_icon\\cancel_btn.png', key="cancel_btn", expand_x=True, tooltip=" Cancel ",
                              button_color='#FFFFFF',mouseover_colors='#d1d1e0'))

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
