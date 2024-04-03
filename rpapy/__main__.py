"""RPAPY is a open source easy tool for automating boring stuffs on any screen with robotframework, pyautogui, pywinauto and others.
--------

- rpapy v1.1.3
"""
import sys
from pathlib import Path
from unittest.mock import patch

import pyperclip
from pynput import keyboard, mouse
from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QApplication

with patch("ctypes.windll.user32.SetProcessDPIAware", autospec=True):
    import pyautogui  # noqa # pylint:disable=unused-import

from rpapy.core.config import Config
from rpapy.core.snipps import capture_image_crop, update_image
from rpapy.core.snipps.loads import (create_default_script_file,
                                     load_robot_example)
from rpapy.core.utils import draw_outline
from rpapy.core.utils.messages import message_to_set_timeout, select_item_list


def get_element_position(x, y):
    print('{0} at {1}'.format('Pressed', (x, y)))
    pyperclip.copy('{0}, {1}'.format(x, y))


class MouseThread(QThread):
    key_controll = keyboard.Controller()

    def run(self):
        
        def on_move(x, y):   
            positionStr = 'X: ' + str(x).rjust(4, ' ') + ' Y: ' + str(y).rjust(4, ' ')
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)            
            
        def on_click(x, y, button, pressed):
            if pressed:        
                # get_element_position(x, y)
                pass

        # ...or, in a non-blocking fashion:
        self.listener = mouse.Listener(
            on_move=on_move,
            on_click=on_click)
        self.listener.start()


class HotkeysThread(QThread):
    capture_image = Signal(object)
    change_file = Signal(bool)
    set_backend_uia = Signal(object)
    set_backend_win32 = Signal(object)
    show_config = Signal()
    load_example = Signal()
    inspect_element = Signal()
    update_image = Signal()
    off = Signal(object)

    def run(self):
        flag_backend = True
        def capture_image():
            self.capture_image.emit('Change image')

        def change_file():
            self.change_file.emit(True)
        
        def set_backend_uia_win32():
            nonlocal flag_backend
            flag_backend = not flag_backend
            if flag_backend:
                self.set_backend_uia.emit('uia')
            else:
                self.set_backend_win32.emit('win32')

        def update_image():
            self.update_image.emit()
        
        def inspect_element():
            self.inspect_element.emit()
        
        def show_config():
            self.show_config.emit()

        def load_example():
            self.load_example.emit()

        def turn_off_agentpy():
            h.stop()
                
        with keyboard.GlobalHotKeys({
                '<ctrl>+<alt>+p': capture_image,
                '<ctrl>+<alt>+r': change_file,
                '<ctrl>+<alt>+b': set_backend_uia_win32,
                '<ctrl>+<alt>+u': update_image,
                '<ctrl>+i':       inspect_element,
                '<ctrl>+<cmd>+c': show_config,
                '<ctrl>+<cmd>+e': load_example,
                '<ctrl>+<cmd>+x': turn_off_agentpy}) as h:
            h.join()
      
        self.off.emit('Global hotkey turned_off_agent.')


class AgentPy(QObject):
    
    def __init__(self, config=None):
        super(AgentPy, self).__init__()
        
        self.config: Config = Config if config is None else config

        self._file_name = 'main.robot'
        self.backend = 'uia'

        self.hotkeys_thread = HotkeysThread(self)
        self.hotkeys_thread.change_file.connect(self._change_file)
        self.hotkeys_thread.capture_image.connect(self._capture_imagem)
        self.hotkeys_thread.set_backend_uia.connect(self.set_backend_uia)
        self.hotkeys_thread.set_backend_win32.connect(self.set_backend_win32)
        self.hotkeys_thread.inspect_element.connect(self._backend_inspect)
        self.hotkeys_thread.show_config.connect(self._show_config)
        self.hotkeys_thread.load_example.connect(self._load_example)
        self.hotkeys_thread.update_image.connect(self._update_image)
        self.hotkeys_thread.off.connect(self._turn_off)
        self.hotkeys_thread.start()

        self.mouse_thread = MouseThread(self)
        self.mouse_thread.start()
        
        self._turn_on()
        self._change_file()
    
    def _turn_on(self):
        HOTKEYS_ACTIONS = """\n***Turn on AgentPy***
        
        **************Teclas de atalho*************
        <ctrl>+<alt>+p: capiturar imagem ou ocr
        <ctrl>+<alt>+r: alterar nome do arquivo
        <ctrl>+<alt>+b: alternar entre os backends
        <ctrl>+<alt>+u: atualizar imagem do elem
        <ctrl>+i:       inspecionar elemento de UI
        <ctrl>+<cmd>+c: exibir configuração atual
        <ctrl>+<cmd>+e: load implemetação exemplo
        <ctrl>+<cmd>+x: desligar o Agente
        *******************************************
        """
        print(HOTKEYS_ACTIONS.upper())

    def _turn_off(self):
        print('\nTurn off')
        self.mouse_thread.listener.stop()
        print('>>>> Agente RPA desligado.')
        exit(0)

    def _show_config(self):
        message_to_set_timeout(self.config.get_config(), timeout=False)

    def _load_example(self):
        load_robot_example()

    def set_backend_uia(self, backend: str):
        self.backend = backend
        print('>>>> Backend changed to "UIA".')             

    def set_backend_win32(self, backend: str):
        self.backend = backend        
        print('>>>> Backend changed to "WIN32".')             
    
    def _backend_inspect(self):
        x, y = pyautogui.position()
        get_element_position(x, y)
        draw_outline(x, y, backend=self.backend)

    def _capture_imagem(self):
        capture_image_crop(self._file_name)

    def _change_file(self):        
        file_name = create_default_script_file(default_name=self._file_name)
        if file_name is None:
            pyautogui.alert(title='RPAPY', text='O agente será desligado.')
            pyautogui.hotkey('ctrl', 'win', 'x')
            return
        self._file_name = file_name
    
    def _update_image(self):
        from rpapy.core.image_mapper import map_images

        map_images_regions_anchors = map_images()        
        image_name_list = list(map_images_regions_anchors)

        image_name = select_item_list(text='Selecione o nome da imagem a ser atualizada',
                                      title='Update Image',
                                      item_type_name='Image',
                                      item_list=image_name_list,
                                      index=0)
        
        if image_name is None or image_name.strip() == '':
            return

        image_name_path = map_images_regions_anchors.get(image_name, {}).get('image')

        if image_name_path is not None:
            update_image(image_name_path)
        else:
            pyautogui.alert(title='RPAPY',
                            text=f'A imagem "{image_name}" não foi encontrada no diretório {self.config.IMAGES_DIR_NAME}.')


def main():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    agent = AgentPy()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
