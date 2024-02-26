import pyautogui
import PySimpleGUI as sg


def confirm_ok_cancel(msg:str)-> bool:
    option = pyautogui.confirm(text=msg, title='RPAPY', buttons=['OK','CANCEL'])        
    if option is None or option == 'CANCEL':
        return False
    return True


def message_to_set_timeout(msg: str, timeout: bool=True):

    sg.ChangeLookAndFeel("SystemDefault")

    text = sg.Text(msg, background_color="#ffde27", text_color="black")

    choices = ['OK', 'TIMEOUT 5s', 'TIMEOUT 10s'] if timeout else ['OK']

    buttons = [
        sg.Button(choice, button_color=("black", "#e3b200")) for choice in choices
    ]

    layout = [[text], buttons]

    window3 = sg.Window(
        "Select Anchor",
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

    pyautogui.sleep({
        'OK': 1.0,
        'TIMEOUT 5s': 5.0,
        'TIMEOUT 10s': 10.0,
    }.get(choice, 1.0))
