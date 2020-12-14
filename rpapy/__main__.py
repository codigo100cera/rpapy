"""RPAPY is a open source easy tool for automating boring stuffs on any screen with robotframework, pyautogui, pywinauto and others.
--------

- realpython-reader v1.0.1
"""
import sys
from pathlib import Path

import pyautogui
import pyperclip
from pynput import keyboard, mouse
from PySide2.QtCore import QObject, QThread, Signal
from PySide2.QtWidgets import QApplication
from pywinauto import Desktop
from win10toast import ToastNotifier

from rpapy.core.screenshots import (capiturar_imagem,
                                    mensagem_timeout_predefinido)
from rpapy.core.uploads import create_robot_default_dirs, upload_robot
from rpapy.core import templates



def get_position_element(x, y):
    print('{0} at {1}'.format('Pressed', (x, y)))
    pyperclip.copy('{0}, {1}'.format(x, y))


class MouseThread(QThread):
    controle_key = keyboard.Controller()

    def run(self):
        
        def on_move(x, y):   
            positionStr = 'X: ' + str(x).rjust(4, ' ') + ' Y: ' + str(y).rjust(4, ' ')
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)            
            
        def on_click(x, y, button, pressed):
            if pressed:        
                # get_position_element(x, y)
                pass

        # ...or, in a non-blocking fashion:
        self.listener = mouse.Listener(
            on_move=on_move,
            on_click=on_click)
        self.listener.start()


class HotkeysThread(QThread):
    capiturar_imagem = Signal(object)
    alterar_arquivo = Signal(bool)
    set_backend_uia = Signal(object)
    set_backend_win32 = Signal(object)
    show_config = Signal()
    upload_example = Signal()
    inspect_element = Signal()
    off = Signal(object)

    def run(self):
        flag_backend = True
        def capiturar_imagem():
            self.capiturar_imagem.emit('Alterar imagem')

        def alterar_arquivo():
            self.alterar_arquivo.emit(True)
        
        def set_backend_uia_win32():
            nonlocal flag_backend
            flag_backend = not flag_backend
            if flag_backend:
                self.set_backend_uia.emit('uia')
            else:
                self.set_backend_win32.emit('win32')
        
        def inspect_element():
            self.inspect_element.emit()
        
        def show_config():
            self.show_config.emit()

        def upload_example():
            self.upload_example.emit()

        def turn_off_agentpy():
            h.stop()
                
        with keyboard.GlobalHotKeys({
                '<ctrl>+<alt>+p': capiturar_imagem,
                '<ctrl>+<alt>+r': alterar_arquivo,
                '<ctrl>+<alt>+b': set_backend_uia_win32,
                '<ctrl>+i':       inspect_element,
                '<ctrl>+<cmd>+c': show_config,
                '<ctrl>+<cmd>+e': upload_example,
                '<ctrl>+<cmd>+x': turn_off_agentpy}) as h:
            h.join()
      
        self.off.emit('Global hotkey turned_off_agent.')


class AgentPy(QObject):
    
    def __init__(self, config=None):
        super(AgentPy, self).__init__()
        from rpapy.core.config import Config

        self._config: Config = Config if config is None else config

        self._nome_arquivo = 'main.robot'
        self.backend = 'uia'

        self.toaster = ToastNotifier()       
        self.toaster.show_toast('Agente RPA acionado.', duration=2, threaded=True)

        self.hotkeys_thread = HotkeysThread(self)
        self.hotkeys_thread.alterar_arquivo.connect(self._alterar_arquivo)
        self.hotkeys_thread.capiturar_imagem.connect(self._capiturar_imagem)
        self.hotkeys_thread.set_backend_uia.connect(self.set_backend_uia)
        self.hotkeys_thread.set_backend_win32.connect(self.set_backend_win32)
        self.hotkeys_thread.inspect_element.connect(self._backend_inspect)
        self.hotkeys_thread.show_config.connect(self._show_config)
        self.hotkeys_thread.upload_example.connect(self._upload_example)
        self.hotkeys_thread.off.connect(self._turn_off)
        self.hotkeys_thread.start()

        self.mouse_thread = MouseThread(self)
        self.mouse_thread.start()
        
        self._turn_on()
        self._alterar_arquivo()
    
    def _turn_on(self):
        HOTKEYS_ACTIONS = """***Turn on AgentPy***
        **************Teclas de atalho**************
        <ctrl>+<alt>+p: capiturar imagem ou ocr,
        <ctrl>+<alt>+r: alterar nome do arquivo,
        <ctrl>+<alt>+b: alternar entre os backends,
        <ctrl>+i:       inspecionar elemento de UI,
        <ctrl>+<cmd>+c: exibir configuração atual,
        <ctrl>+<cmd>+e: upload implemetação exemplo,
        <ctrl>+<cmd>+x: desligar o Agente
        ********************************************
        """
        print(HOTKEYS_ACTIONS.upper())

    def _turn_off(self):
        print('\nTurn off')
        self.mouse_thread.listener.stop()
        self.toaster.show_toast('Agente RPA desligado.', duration=2, threaded=True)
        exit(0)

    def _show_config(self):
        mensagem_timeout_predefinido(self._config.get_config(), timeout=False)

    def _upload_example(self):
        upload_robot()

    def set_backend_uia(self, backend: str):
        self.backend = backend
        self.toaster.show_toast('Backend alterado para "UIA".', duration=1.5, threaded=True)             

    def set_backend_win32(self, backend: str):
        self.backend = backend        
        self.toaster.show_toast('Backend alterado para "WIN32".', duration=1.5, threaded=True)             
    
    def _backend_inspect(self):
        x, y = pyautogui.position()
        get_position_element(x, y)
        Desktop(backend=self.backend).from_point(x, y).draw_outline(thickness=3)

    def _capiturar_imagem(self):
        capiturar_imagem(self._nome_arquivo, config=self._config)

    def _alterar_arquivo(self, prompt=True):
        nome_arquivo = self._nome_arquivo
        if prompt:
            nome_arquivo = pyautogui.prompt(text='Insirá o nome do arquivo .py', title='Alteração de Arquivo', default=self._nome_arquivo)

        if nome_arquivo is None:
            pyautogui.alert(title='RPAPY', text='O agente foi cancelado.')
            pyautogui.hotkey('ctrl', 'win', 'x')
            return
        
        if nome_arquivo.strip() == '':
            nome_arquivo = self._nome_arquivo

        extensao = nome_arquivo.lower().split('.')[-1]

        self._nome_arquivo = nome_arquivo if extensao == 'py' or extensao == 'robot' else f'{nome_arquivo}.robot'

        path_file = Path(self._config.BASE_DIR, self._nome_arquivo)
        path_file_env = Path(self._config.BASE_DIR, '.env')

        MODULES_IMPORT = templates.MODULES_IMPORT_PY
            
        if extensao == 'robot':
            create_robot_default_dirs()
            
            path_file = Path(self._config.TASKS_DIR_NAME) / self._nome_arquivo
            MODULES_IMPORT = templates.MODULES_IMPORT_ROBOT
            
            path_file_keywords = Path(self._config.RESOURCES_DIR_NAME) / self._config.RESOURCES_KEYWORDS_FILE_NAME
            if not path_file_keywords.exists():
                path_file_keywords.touch()
                path_file_keywords.write_text('\n'.join(templates.MODULES_IMPORT_RESOURCE.splitlines()), encoding='utf-8')
        
        if not path_file_env.exists():
            path_file_env.touch()
            path_file_env.write_text(templates.VARIAVEIS_AMBIENTE,encoding='utf-8')
        
        if not path_file.exists():
            path_file.touch()

        conteudo = path_file.read_text().splitlines()

        # Inclui os imports padrões no inicio do arquivo quando não for encontrado nenhuma palavra "import" ou
        #  *** Settings *** nos arquivos .py ou .robot 
        if 'import' not in '\n'.join(conteudo) and '*** Settings ***' not in '\n'.join(conteudo):    
            conteudo = MODULES_IMPORT.splitlines() + conteudo

            if extensao == 'robot':
                path_file.write_text('\n'.join(conteudo), encoding='utf-8')
            else:
                path_file.write_text('\n'.join(conteudo))


def main():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    agent = AgentPy()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
