import contextlib
from typing import Tuple

from pywinauto import Desktop

from rpapy.core.localizador import LocalizadorImagem, max_wait_attr
from rpapy.core.prepare_text import prepare_text_to_pyautogui
from rpapy.core.snipps.snippingtools import ImageNotFoundError

###########################################################
_identifier_img = LocalizadorImagem()
###########################################################

def toast_process_start_notifier():
    from win10toast import ToastNotifier
    
    toaster = ToastNotifier()
    toaster.show_toast('Robo.py iniciando processo', duration=5, threaded=True)
    print('Robo.py iniciando processo...')


def _get_ui_element(x: int, y: int,*,attr_name: str, backend: Desktop, wait_attr: float):
    UI_element = Desktop(backend=backend).from_point(x, y)
    max_wait_attr(UI_element, attr_name=attr_name, max_wait=wait_attr)
    return UI_element


def wait_element_vision(*args, **kwargs):
    get_element_vision(*args, **kwargs)


def get_element_vision(image_name: str, *args,        
        attr_name: str=None,
        identifier_img: LocalizadorImagem=None,
        backend: str=None,             # As opções são: 'uia' ou 'win32'
        before: float=0.0,
        after: float=0.0,
        max_wait: float=None, 
        interval: float=None,
        confidence: float=None,
        wait_vanish: bool=False,
        execute: bool=False,
        wait_attr: float=5.0,
        move_x: int=0,
        move_y: int=0,
        delay: float=0.0,
        ignore_error:bool=False,
        ignore_set_focus=False,
        click_before_typing=None,
        arguments: tuple=(),
        kwarguments: dict={},
        **kwargs):

    from time import sleep
    
    sleep(float(before))
    identifier_img = identifier_img or _identifier_img
    
    coordinate = None
    try:
        coordinate = identifier_img(
                image_name, 
                max_wait=max_wait, 
                confidence=confidence,
                wait_vanish=wait_vanish,
                interval=interval, 
                deslocar_x=move_x, 
                deslocar_y=move_y
        )
    except ImageNotFoundError as error:
        if ignore_error:
            return
        raise ImageNotFoundError(str(error))
    
    if attr_name is None:
        return coordinate

    args = args + arguments
    kwargs.update(kwarguments)    
    
    if backend is None:
        import pyautogui

        if execute is True:
            pyautogui_attr = getattr(pyautogui, attr_name)
            if attr_name in 'press type_write write':
                if click_before_typing:
                    pyautogui.click(*coordinate, interval=float(delay), button=kwargs.get('button', 'left'))                    
                    sleep(.2)
                pyautogui_attr(*args, interval=float(delay), **kwargs)
            else:
                pyautogui_attr(*coordinate, *args, interval=float(delay), **kwargs)
        sleep(float(after))
        return coordinate

    elif backend in ['win32', 'uia']:
        UI_element = _get_ui_element(*coordinate, attr_name=attr_name, backend=backend, wait_attr=wait_attr)
        if not ignore_set_focus:
            UI_element.set_focus()
        if execute is True:
            UI_element_attr = getattr(UI_element, attr_name)
            if attr_name in 'type_keys':
                if click_before_typing:
                    UI_element.click_input(button=kwargs.get('button', 'left'))
                    sleep(.2)
                UI_element_attr(*args, with_spaces=True, pause=float(delay), **kwargs)
            elif attr_name == 'triple_click_input':
                UI_element_attr = getattr(UI_element, 'click_input')
                for _ in range(3):
                    UI_element_attr(*args,**kwargs)
                    sleep(float(delay))
            else:
                UI_element_attr(*args,**kwargs)
        sleep(float(after))
        return UI_element
    else:
        raise Exception(f'O backend "{backend}" não identificado.')


def write_text_vision(image_name: str,*,
        text: str,
        identifier_img: LocalizadorImagem=None,
        backend: str=None,             # As opções são: 'uia' ou 'win32'
        max_wait: float=None, 
        wait_vanish: bool=False,
        move_x: int=0,
        move_y: int=0,
        delay: float=0.0,
        before: float=0.0,
        after: float=0.0,
        interval: float=None,
        confidence: float=None,
        wait_attr: float=5.0,
        ignore_error:bool=False,
        ignore_set_focus: bool=False):

    attr_name = 'type_keys' if backend is not None else 'press'
    if backend is None:
        text = prepare_text_to_pyautogui(text)

    execute = True
    
    return get_element_vision(image_name, text, identifier_img=identifier_img, backend=backend, max_wait=max_wait, 
                                attr_name=attr_name, wait_vanish=wait_vanish, move_x=move_x, move_y=move_y, delay=delay, 
                                before=before, after=after, interval=interval, confidence=confidence, wait_attr=wait_attr, 
                                execute=execute, ignore_error=ignore_error, ignore_set_focus=ignore_set_focus)


def click_vision(image_name: str,*,
        identifier_img: LocalizadorImagem=None,
        backend: str=None,             # As opções são: 'uia' ou 'win32'
        button: str='left',
        max_wait: float=None, 
        move_x: int=0,
        move_y: int=0,
        delay: float=0.0,
        before: float=0.0,
        after: float=0.0,
        interval: float=None,
        confidence: float=None,
        wait_vanish: bool=False,       
        wait_attr: float=5.0,
        ignore_error: bool=False):

    attr_name = 'click_input' if backend is not None else 'click'
    execute = True

    return get_element_vision(image_name,attr_name=attr_name, identifier_img=identifier_img, backend=backend, 
                                button=button, delay=delay, before=before, after=after, max_wait=max_wait, 
                                interval=interval, confidence=confidence, wait_vanish=wait_vanish, wait_attr=wait_attr, 
                                move_x=move_x, move_y=move_y,ignore_error=ignore_error, execute=execute)


def double_click_vision(image_name: str,*,
        identifier_img: LocalizadorImagem=None,
        button: str='left',
        delay: float=0.0,
        before: float=0.0,
        after: float=0.0,
        max_wait: float=None, 
        interval: float=None,
        confidence: float=None,
        wait_vanish: bool=False,
        backend: str=None,             # As opções são: 'uia' ou 'win32'
        wait_attr: float=5.0,
        move_x: int=0,
        move_y: int=0,
        ignore_error: bool=False,
        ignore_set_focus: bool=False):
    
    attr_name = 'double_click_input' if backend is not None else 'doubleClick'
    execute = True

    return get_element_vision(image_name,attr_name=attr_name, identifier_img=identifier_img, backend=backend, 
                                button=button, delay=delay, before=before, after=after, max_wait=max_wait, interval=interval, 
                                confidence=confidence, wait_vanish=wait_vanish, wait_attr=wait_attr, move_x=move_x, move_y=move_y,
                                ignore_error=ignore_error, execute=execute, ignore_set_focus=ignore_set_focus)


def triple_click_vision(image_name: str,*,
        identifier_img: LocalizadorImagem=None,
        button: str='left',
        delay: float=0.1,
        before: float=0.0,
        after: float=0.0,
        max_wait: float=None, 
        interval: float=None,
        confidence: float=None,
        wait_vanish: bool=False,
        backend: str=None,             # As opções são: 'uia' ou 'win32'
        wait_attr: float=5.0,
        move_x: int=0,
        move_y: int=0,
        ignore_error: bool=False):
    
    attr_name = 'triple_click_input' if backend is not None else 'tripleClick'
    execute = True

    return get_element_vision(image_name,attr_name=attr_name, identifier_img=identifier_img, backend=backend, 
                                button=button, delay=delay, before=before, after=after, max_wait=max_wait, 
                                interval=interval, confidence=confidence, wait_vanish=wait_vanish, wait_attr=wait_attr, 
                                move_x=move_x, move_y=move_y,ignore_error=ignore_error, execute=execute)



def get_element_coord(x, y, *args,
        backend: str=None,             # As opções são: 'uia' ou 'win32'
        attr_name: str=None,
        before: float=0.0,
        after: float=0.0,
        delay: float=0.0,
        execute: bool=True,
        click_before_typing=None,        
        arguments: tuple=(),
        kwarguments: dict={},
        wait_attr: float=5.0,
        **kwargs):

    from time import sleep

    sleep(float(before))    
    coordinate = int(float(x)), int(float(y))

    args = args + arguments
    kwargs.update(kwarguments)
    
    if backend is None:
        import pyautogui

        if execute is True:
            pyautogui_attr = getattr(pyautogui, attr_name)
            if attr_name in 'press type_write write':
                pyautogui_attr(*args, interval=float(delay), **kwargs)
            else:
                pyautogui_attr(*coordinate, *args, interval=float(delay), **kwargs)
        sleep(float(after))
        return coordinate

    elif backend in ['win32', 'uia']:
        UI_element = _get_ui_element(*coordinate, attr_name=attr_name, backend=backend, wait_attr=wait_attr)
        UI_element.set_focus()
        if execute is True:
            UI_element_attr = getattr(UI_element, attr_name)
            if attr_name in 'type_keys':
                UI_element_attr(*args, with_spaces=True, pause=float(delay), **kwargs)
            elif attr_name == 'triple_click_input':
                UI_element_attr = getattr(UI_element, 'click_input')
                for _ in range(3):
                    UI_element_attr(*args,**kwargs)
                    sleep(float(delay))
            else:
                UI_element_attr(*args,**kwargs)
        sleep(float(after))
        return UI_element
    else:
        raise Exception(f'O backend "{backend}" não identificado.')


def write_text_coord(x: int, y: int,*,
        text: str,        
        delay: float=0.0,
        before: float=0.0,
        after: float=0.0,
        backend: str=None,             # As opções são: 'uia' ou 'win32'
        wait_attr: float=5.0):

    attr_name = 'type_keys' if backend is not None else 'press'
    if backend is None:
        text = prepare_text_to_pyautogui(text)    

    return get_element_coord(x, y, text, attr_name=attr_name, backend=backend, before=before, after=after, delay=delay, wait_attr=wait_attr)
    

def click_coord(x: int, y: int,
        button: str='left',
        delay: float=0.0,
        before: float=0.0,
        after: float=0.0,
        backend: str=None,             # As opções são: 'uia' ou 'win32'
        wait_attr: float=5.0):

    attr_name = 'click_input' if backend is not None else 'click'

    return get_element_coord(x, y, button=button, attr_name=attr_name, backend=backend, before=before, after=after, delay=delay, wait_attr=wait_attr)


def double_click_coord(x: int, y: int,
        button: str='left',
        delay: float=0.0,
        before: float=0.0,
        after: float=0.0,
        backend: str=None,             # As opções são: 'uia' ou 'win32'
        wait_attr: float=5.0):
    
    attr_name = 'double_click_input' if backend is not None else 'doubleClick'

    return get_element_coord(x, y, button=button, attr_name=attr_name, backend=backend, before=before, after=after, delay=delay, wait_attr=wait_attr)


def triple_click_coord(x: int, y: int,
        button: str='left',
        delay: float=0.1,
        before: float=0.0,
        after: float=0.0,
        backend: str=None,             # As opções são: 'uia' ou 'win32'
        wait_attr: float=5.0):

    attr_name = 'triple_click_input' if backend is not None else 'doubleClick'

    return get_element_coord(x, y, button=button, attr_name=attr_name, backend=backend, before=before, after=after, delay=delay, wait_attr=wait_attr)


def get_text_ocr_vision(image_name, region:Tuple[int], *args, identifier_img: LocalizadorImagem=None, lang: str='por', **kwargs) -> str:
    import pytesseract as ocr
    from pyautogui import screenshot

    coordinate = wait_element_vision(image_name,identifier_img=identifier_img, **kwargs)
    
    image_region = screenshot(region=region)
    ocr_text_result = ocr.image_to_string(image_region, lang=lang)
    return ocr_text_result


def get_text_ocr_region(region:Tuple[int], lang: str='por') -> str:
    import pytesseract as ocr
    from pyautogui import screenshot

    image_region = screenshot(region=region)
    ocr_text_result = ocr.image_to_string(image_region, lang=lang)
    return ocr_text_result


def drag_to_vision(image:str, x:int, y:int, *args, **kwargs):
    """TODO: Implementation

    Args:
        image (str): [description]
        x (int): [description]
        y (int): [description]
    """


def drag_vision(image:str, x:int, y:int, *args, **kwargs):
    """TODO: Implementation

    Args:
        image (str): [description]
        x (int): [description]
        y (int): [description]
    """



def registrar_credencial(usuario, sistema='Robot_framework'):
    import keyring
    from pyautogui import alert, password, prompt

    secret_value = keyring.get_password(sistema, usuario)
    if secret_value is not None:
        return secret_value    
    
    sistema = prompt(title='RPAPY', text='Insirá no nome do Sistema.', default=sistema)
    if sistema.strip() == None: exit()
    
    usuario = prompt(title='RPAPY', text=f'Insirá o nome de campo que será preenchido no "{sistema}".', default=usuario)
    if usuario is None or usuario.strip() == '': return
    
    secret_value = password(title='RPAPY', text=f'Insirá o valor que deverá ser preenchido no campo "{usuario}".', mask='*')
    if secret_value is None or secret_value.strip() == '': return
    
    if sistema.strip() == '':        
        keyring.set_password('Robot_framework', usuario, secret_value)
    else:
        keyring.set_password(sistema, usuario, secret_value)
        
    alert(title='RPAPY', text=f'A credencial "{usuario}" para o sistema {sistema}, foi registrada com sucesso!')
    
    return keyring.get_password(sistema, usuario)


def open_executable(exec_name: str, window_title: str, *,work_dir: str, max_try: int=5, maximized: bool=True ):    
    from pathlib import Path
    from subprocess import Popen
    from time import sleep

    from pygetwindow import Win32Window

    for w in get_windows_title(window_title):
        w.close()
        sleep(.2)

    path = Path(work_dir)
            
    app: Win32Window = None
    for _ in range(max_try):

        Popen([exec_name], shell=True, cwd=path)
        windows_list = get_windows_title(window_title)

        with contextlib.suppress(IndexError):
            app = windows_list[-1]

            if not app.isActive:
                app.minimize()
                app.restore()

            if maximized:
                app.maximize()
            else:
                app.restore()      
            
        if app is not None:
            break
    else:
        raise Exception(f'A janela do executável "{exec_name}" com o titulo "{window_title}" não foi encontrado.')

    return  app


def get_windows_title(window_title: str):
    from time import sleep

    from pygetwindow import getWindowsWithTitle

    windows_list = None
    for _ in range(5):
        windows_list = getWindowsWithTitle(window_title)
        sleep(1)
        if windows_list:
            break
    return windows_list


def get_path_by_image_name(image_name: str)-> str:
    from rpapy.core.localizador import get_absolute_path_by_image_name
    return get_absolute_path_by_image_name(image_name)
