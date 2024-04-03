import time
from typing import List

import PySimpleGUI as sg


def confirm_ok_cancel(text:str, title:str = 'Janela de Confirmação')-> bool:
    sg.ChangeLookAndFeel("SystemDefault")

    text = sg.Text(text, background_color="#ffde27", text_color="black")

    choices = ['OK', 'CANCEL']

    buttons = [sg.Button(choice, button_color=("black", "#e3b200")) for choice in choices]

    layout = [[text], buttons]

    window = sg.Window(
        title,
        layout,
        # icon="icon.ico",
        no_titlebar=True,
        background_color="#ffde27",
        element_justification="center",
        use_default_focus=False,
        keep_on_top=True
    )

    choice, _ = window.Read()
    window.Close()
    del(window)

    if choice is None or choice.upper() == 'CANCEL':
        sg.popup(f'O processo foi cancelado', 
                          keep_on_top=True)
        return False
    return True


def confirm_yes_no_cancel(text:str, title:str = 'Janela de Confirmação')-> bool:
    sg.ChangeLookAndFeel("SystemDefault")

    text = sg.Text(text, background_color="#ffde27", text_color="black")

    choices = ['YES', 'NO', 'CANCEL']

    buttons = [sg.Button(choice, button_color=("black", "#e3b200")) for choice in choices]

    layout = [[text], buttons]

    window = sg.Window(
        title,
        layout,
        # icon="icon.ico",
        no_titlebar=True,
        background_color="#ffde27",
        element_justification="center",
        use_default_focus=False,
        keep_on_top=True
    )

    choice, _ = window.Read()
    window.Close()
    del(window)

    if choice.upper() == 'CANCEL':
        sg.popup_annoying(f'O processo foi cancelado', 
                          keep_on_top=True)
        return None
    elif choice == 'YES':
        return True    
    return False


def confirm_yes_no(text:str, title:str = 'Janela de Confirmação')-> bool:
    sg.ChangeLookAndFeel("SystemDefault")

    text = sg.Text(text, background_color="#ffde27", text_color="black")

    choices = ['YES', 'NO']

    buttons = [sg.Button(choice, button_color=("black", "#e3b200")) for choice in choices]

    layout = [[text], buttons]

    window = sg.Window(
        title,
        layout,
        # icon="icon.ico",
        no_titlebar=True,
        background_color="#ffde27",
        element_justification="center",
        use_default_focus=False,
        keep_on_top=True
    )

    choice, _ = window.Read()
    window.Close()
    del(window)

    if choice == 'YES':
        return True    
    return False


def message_to_set_timeout(text: str, timeout: bool=True):

    sg.ChangeLookAndFeel("SystemDefault")

    text = sg.Text(text, background_color="#ffde27", text_color="black")

    choices = ['OK', 'TIMEOUT 5s', 'TIMEOUT 10s'] if timeout else ['OK']

    buttons = [
        sg.Button(choice, button_color=("black", "#e3b200")) for choice in choices
    ]

    layout = [[text], buttons]

    window3 = sg.Window(
        "RPA-PY",
        layout,
        # icon="icon.ico",
        no_titlebar=True,
        background_color="#ffde27",
        element_justification="center",
        use_default_focus=False,
        keep_on_top=True
    )

    choice, _ = window3.Read()
    window3.Close()
    del(window3)

    time.sleep({
        'OK': 1.0,
        'TIMEOUT 5s': 5.0,
        'TIMEOUT 10s': 10.0,
    }.get(choice, 1.0))


def select_item_list(*, text : str, title, item_type_name : str, item_list : List[str] = [], index: int = 0):

    item_list.insert(0, '') 

    sg.ChangeLookAndFeel("SystemDefault")

    NAME_SIZE = 9 + len(item_type_name)
    ITEM_LIST_MAX_LEN = max([len(n) for n in item_list])
    background_color = "#ffde27"

    def name(name):
        dots = NAME_SIZE-len(name)-2
        return sg.Text(name + ' ' + '•'*dots, 
                       size=(NAME_SIZE,1), 
                       justification='r',
                       pad=(0,0), 
                       background_color=background_color,
                       font='Courier 10')


    text = [sg.Text(text, background_color=background_color, text_color="black")]
    choices = ['CANCEL']
    buttons = [sg.Button(choice, button_color=("black", "#e3b200")) for choice in choices]
    combo = [
        name(f'Select {item_type_name}'),
        sg.Combo(item_list, 
                 default_value=item_list[index], 
                 enable_events=True, 
                 readonly=True, 
                 s=(ITEM_LIST_MAX_LEN,22),
                 k='-COMBO-')
    ]

    layout = [text, combo, buttons]

    window = sg.Window(
        title,
        layout,
        icon="icon.ico",
        no_titlebar=False,
        background_color=background_color,
        element_justification="center",
        use_default_focus=False,
        keep_on_top=True
    )

    choice, values = window.Read()
    window.Close()
    del(window)

    result = values.get('-COMBO-')

    if choice is None or choice == 'CANCEL' or result == '':
        sg.popup_annoying(f'O processo foi cancelado', 
                          keep_on_top=True)
        return None
    
    return result


def prompt(text='', title='RPA-PY', default=''):
    sg.ChangeLookAndFeel("SystemDefault")

    NAME_SIZE = 10
    background_color = "#ffde27"

    def name(name):
        dots = NAME_SIZE-len(name)-2
        return sg.Text(name + ' ' + '•'*dots, background_color=background_color, size=(NAME_SIZE,1), justification='r',pad=(0,0), font='Courier 10')


    text = sg.Text(text, background_color=background_color, text_color="black")

    input_field =  [name('File name'), sg.Input(s=40, default_text=default, k='-INPUT-')]

    choices = ['OK', 'CANCEL']
    buttons = [sg.Button(choice, button_color=("black", "#e3b200")) for choice in choices]

    layout = [[text], input_field, buttons]

    window = sg.Window(
        title,
        layout,
        # icon="icon.ico",
        no_titlebar=True,
        background_color=background_color,
        element_justification="center",
        use_default_focus=False,
        keep_on_top=True
    )

    choice, values = window.Read()
    window.Close()
    del(window)

    if choice is None or choice.upper() == 'CANCEL':
        sg.popup_annoying(f'O processo foi cancelado', 
                          keep_on_top=True)
        return False
    else:
        return values['-INPUT-']



    

if '__main__' == __name__:
    # select_item_list('mensagem', 'Update Image', 'image', ['img1', 'img2', 'img3'])
    # confirm_ok_cancel('deseja realizar a alteração ?', 'Update Image')
    print(prompt('Insirá o nome do arquivo a ser editado com a extensão .robot ou .py', 
                 default='main.py'))