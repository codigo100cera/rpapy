import contextlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pyautogui
import pyperclip
import PySimpleGUI as sg
from PIL import Image

from . import templates
from .config import Config
from rpapy.core.uploads import create_python_default_dirs, create_robot_default_dirs


coordinates = None

class ScreenshotAreaError(Exception):
    pass


class ParamNotFoundError(Exception):
    pass


class ImageNotFoundError(Exception):
    """[summary]
    Arguments:
    |ValueError: Exception {[type]} -- [description]
    """


class ImageNotDisappearError(Exception):
    """[summary]
    Arguments:
        Exception {[type]} -- [description]
    """    


def remove_duplicate_images(img_name, dir_name_imgs):
    images_file_found_path: Path = list(Path(dir_name_imgs).glob(f'{img_name}-*.png'))
    if len(images_file_found_path) > 0:
        texto = f'Foram encontrados {len(images_file_found_path)} imagem(s) com o nome "{img_name}", deseja substituir todos?'
        opcao = pyautogui.confirm(text=texto, title='RPA-PY', buttons=['SIM','NAO'])
        if opcao == 'SIM':                
            for path_img in images_file_found_path:
                with contextlib.suppress(FileExistsError):
                    path_img.unlink()
            return True
    return False
    

_templates = {
    'py': {
        '0': templates.CONTROL_RPA_0, 
        '1': templates.CONTROL_RPA_1, 
        '2':templates.CONTROL_RPA_2,
        '3':{'click': templates.ActivityPy.CLICK_VISION, 'click_input': templates.ActivityPy.CLICK_VISION, 
            'double_click': templates.ActivityPy.DOUBLE_CLICK_VISION, 'double_click_input': templates.ActivityPy.DOUBLE_CLICK_VISION, 
            'type_keys': templates.ActivityPy.WRITE_TEXT_VISION, 'triple_click': templates.ActivityPy.TRIPLE_CLICK_VISION,
            'get_element_vision': templates.ActivityPy.GET_ELEMENT_VISION, 'wait_element_vision': templates.ActivityPy.WAIT_ELEMENT_VISION,
            'doubleClick': templates.ActivityPy.DOUBLE_CLICK_VISION, 'scroll': templates.ActivityPy.GET_ELEMENT_VISION, 
            'typewrite': templates.ActivityPy.WRITE_TEXT_VISION, 'ocr_img_to_text':templates.ActivityPy.GET_TEXT_OCR_VISION},
        '4': templates.CONTROL_RPA_OCR_IMG_PY

    },
    'robot': {
        '3': {'click': templates.ActivityRobot.CLICK_VISION, 'click_input': templates.ActivityRobot.CLICK_VISION, 
             'double_click': templates.ActivityRobot.DOUBLE_CLICK_VISION, 'double_click_input': templates.ActivityRobot.DOUBLE_CLICK_VISION, 
             'type_keys': templates.ActivityRobot.WRITE_TEXT_VISION, 'triple_click': templates.ActivityRobot.TRIPLE_CLICK_VISION,
             'get_element_vision': templates.ActivityRobot.GET_ELEMENT_VISION, 'wait_element_vision': templates.ActivityRobot.WAIT_ELEMENT_VISION,
             'doubleClick': templates.ActivityRobot.DOUBLE_CLICK_VISION, 'scroll': templates.ActivityRobot.GET_ELEMENT_VISION,
             'typewrite': templates.ActivityRobot.WRITE_TEXT_VISION, 'ocr_img_to_text':templates.ActivityRobot.GET_TEXT_OCR_VISION},
        '4': templates.ActivityRobot.GET_TEXT_OCR_VISION 
    },
}

_templates_ocr_region = {
    'py': {'1': templates.CONTROL_RPA_OCR_PY, '2': templates.ActivityPy.GET_TEXT_OCR_REGION},
    'robot': {'1': templates.ActivityRobot.GET_TEXT_OCR_REGION}
}

_metodos = {
    'py': {'1':'click', '2':'click_input', '3':'double_click', '4':'double_click_input', '5':'select', 
           '6':'type_keys', '7':'wait_element_vision', '8': 'ocr_img_to_text'},
    'robot': {'1':'click', '2':'click_input', '3':'double_click', '4':'double_click_input', 
              '5':'get_element_vision', '6':'type_keys', '7':'wait_element_vision', '8': 'ocr_img_to_text'},
    'gui': {'1':'click', '2':'click', '3':'doubleClick', '4':'doubleClick', '5':'scroll', '6':'typewrite', 
            '7':'wait_element_vision'},
}

_backends = {
    'py': {'uia': 'uia', 'win32': 'win32', 'gui':'gui', 'ocr': 'ocr'},
    'robot': {'uia': 'uia', 'win32': 'win32', 'gui':'${None}', 'ocr': 'ocr'}
}


path_base_dir = Path(Config.BASE_DIR)
    

def get_screenshot_region(left: int, top: int, right: int, bottom: int) -> Tuple[int]:
    screenshot_area = left, top, right - left, bottom - top
    if min(screenshot_area) < 0:
        raise ScreenshotAreaError('Um ou mais valores informados para a area do screenshot são negativos')
    return screenshot_area


def capiturar_imagem(nome_arquivo_py:str=None, trocar_img=False, config=None)-> Optional[bool]:    
    
    create_python_default_dirs()
    path_resources = path_base_dir / Config.RESOURCES_DIR_NAME    
    images_dir_path = path_resources / Config.IMAGES_DIR_NAME
        
    snippet_type = None
    im_crop = image_recorder()      # Funcao para capiturar o recorte da imagem no screenshot da tela principar
    if im_crop == 'CANCEL':
        return    
        
    region = region_recorder()      # Funcao para capiturar as coordenadas da região onde o robo deverá procurar a imagem
    if region is None:
        return
    
    if im_crop == 'OCR':
        snippet_type = 'OCR'
    if isinstance(im_crop, Image.Image):
        snippet_type = 'IMG'

    if not trocar_img:            
        default = nome_img = ''
        while nome_img.strip() == '':
            if snippet_type == 'OCR':
                msg_text = templates.MSG_OPCOES_OCR_PY if '.py' in nome_arquivo_py.lower() \
                                                        else templates.MSG_OPCOES_OCR_ROBOT            
                nome_img = pyautogui.prompt(text=msg_text, title='RPA-PY', default=default)
            else:
                nome_img = pyautogui.prompt(text=templates.MSG_OPCOES_IMG, title='RPA-PY', default=default)                
            
            if nome_img is None:
                return
            
            if nome_img.strip() == '':
                continue
            
            parametros = nome_img.split()
            nome_img = parametros[0].replace('-','_').lower()
            parametros[0] = nome_img
            parametros = [nome_arquivo_py] + parametros

            region_ocr_img = None
            with contextlib.suppress(IndexError):
                if parametros[3] == 'ocr' and snippet_type != 'OCR':
                    region_ocr_img = region_recorder(msg_timeout='Selecione a região da tela onde será aplicado o OCR.')
                    if region_ocr_img is None:
                        return
            try:
                writing_code_snippet(*parametros, snippet_type=snippet_type, region=region, region_ocr_img=region_ocr_img)
            except ParamNotFoundError as error:
                pyautogui.alert(title='RPAPY', text=str(error))
                default = ''
                with contextlib.suppress(Exception) as target:
                    default = ' '.join(parametros[1:])            
                nome_img = ''           
    else:
        nome_img = nome_arquivo_py
        opcao = pyautogui.confirm(text=f'Nome da imagem a ser substituida: \n"{nome_img}"', title='RPA-PY', buttons=['OK','CANCEL'])        
        if opcao is None or opcao == 'CANCEL':
            return        

    if 'OCR' != snippet_type:
        remove_duplicate_images(nome_img, dir_name_imgs=images_dir_path)

        im_crop.save(f'{images_dir_path}/{nome_img}-{region}.png', 'PNG')
        
        opcao = pyautogui.confirm(title='RPAPY - Capitura de Imagem', text='Deseja visualizar a imagem adicionada?', buttons=['OK', 'NÃO'])
        if opcao == 'OK':
            im_crop.show()
            
    return True


def writing_code_snippet(
        nome_arquivo:str, 
        nome_img:str, 
        template:str='3', 
        backend:str='gui', 
        metodo:str='7', 
        *args: List[str],
        **kwargs: Dict[str,str]) -> None:

    if not nome_img.isidentifier():
        raise ParamNotFoundError(f'O nome "{nome_img}" não é um identificador Python válido.')
    
    # Recupera a extenção do nome do arquivo em que será escrito o snippet de código
    extensao = nome_arquivo.lower().split('.')[-1]    

    # Seleciona e chama a funcao responsavel por compor o snippet passando os argumentos necessarios
    snippet_type = kwargs.get('snippet_type', 'IMG')
    code = {
        'IMG':code_snippet_compose_img, 
        'OCR': code_snippet_compose_ocr
    }[snippet_type](extensao, nome_img, template, backend, metodo, *args, **kwargs)
    
    code = complete_robot_syntax(code)
    code = complete_python_syntax(code)
    pyperclip.copy(code)
        
    # Decide qual arquivo será aberto para escrita do snippet de código
    if Config.ARQUIVO_TEMPORARIO_ATIVO:
        path_file = Path(Config.BASE_DIR, Config.NOME_ARQUIVO_TEMPORARIO)
        if not path_file.exists():
            path_file.touch()
    elif extensao == 'robot':
        create_robot_default_dirs()
        path_dir_task = Path(Config.BASE_DIR, Config.TASKS_DIR_NAME)        
        path_file = path_dir_task / nome_arquivo
    else:
        path_file:Path = Config.BASE_DIR / Path(nome_arquivo)

    # Armazena o conteúdo do arquivo para concatenar com o snippet de código
    conteudo = path_file.read_text().splitlines()
    # Concatena o conteúdo existente no arquivo com o snippet de código criado e escreve no arquivo
    conteudo += code.splitlines()
    
    if extensao == 'robot':
        path_file.write_text('\n'.join(conteudo), encoding='utf-8')
    path_file.write_text('\n'.join(conteudo))


def code_snippet_compose_ocr(extensao:str, nome_img:str, template:str, *args, **kwargs) -> str:
    try:
        language = args[0]
        if language not in 'por eng':
            language = 'por'
    except IndexError:
        language = 'por'    
    # Converte todos os caracteres do nome da imagem para minúsculos
    nome_img = nome_img.lower()
    _template = _templates_ocr_region.get(extensao, {}).get(template)
    if _template is None:
        raise ParamNotFoundError(f'O template "{template}"  não foi encontrado, por favor insirá um número válido.')
    return _template.format(nome_img, kwargs.get('region'), language)
        

def code_snippet_compose_img(extensao:str, nome_img:str, template:str, backend:str, metodo:str, *args, **kwargs) -> str:
    
    # Recupera a partir da tipo de extenção o template código que será 
    # utilizado para o snippet e valida se existe no dicionário
    code = _templates.get(extensao, {}).get(template)    
    if code is None:
        raise ParamNotFoundError('Código "{}" de Template não encontrado.'.format(template))

    # Efetua a recuperação do backend e valida se ele existe no dicionário
    _backend = _backends.get(extensao, {}).get(backend)
    if _backend is None:
        raise ParamNotFoundError('Backend "{}" não encontrado.'.format(backend))

    # Recupera o método que será utilizado no snippet a partir da extensão 
    # para os backends exceto para o backend "gui" que é recuperado pelo próprio nome
    _metodo = None
    if 'gui' != _backend or template == 3:
        _metodo = _metodos.get(extensao, {}).get(metodo)
    else:
        _metodo = _metodos.get('gui',{}).get(metodo)
    
    if _metodo is None:
        raise ParamNotFoundError('O método "{}" não é permitido ser utilizado com backend "{}".'.format(metodo, _backend))
    
    # Monta o snippet de código conforme o template passado por parametro
    if   template == '0':
        code = code.format(nome_img)
    elif template == '1':
        code = code.format(nome_img, _backend, _metodo, list(args)).replace('[', '').replace(']', '')
    elif template == '2':
        code = code.format(nome_img, _metodo, list(args)).replace('[', '').replace(']', '')
    elif template == '3':        
        if code.get(_metodo)is not None:
            if metodo == '5':
                code = code.get(_metodo).format(nome_img, _backend, list(args)).replace('[', '').replace(']', '')
            elif metodo == '6':
                code = code.get(_metodo).format(nome_img, _backend, ' '.join(args))
            elif metodo == '8':
                code = code.get(_metodo).format(nome_img, _backend, kwargs.get('region_ocr_img'), ' '.join(args))
            else:
                code = code.get(_metodo).format(nome_img, _backend, *args)
        else:
            raise ParamNotFoundError('O template "{}" não pode ser usado com o backend "{}" e método "{}".'.format(template, backend, _metodo))
    elif template == '4':
        if len(args) < 1:
            raise ParamNotFoundError('O argumento para a "lang" deve ser adicionado após o backend "ocr" separado por espaço.')
        code = code.format(nome_img, kwargs.get('region_ocr_img'), args[0])    

    return code


def complete_robot_syntax(code: str):
    return code.replace('^~', '{').replace('$~', '}').replace('=ocr', '=None')

def complete_python_syntax(code: str):
    return code.replace("='gui'", '=None')


def capture_screen():
    """
    Captures the screen to a Pillow Image object
    """
    import mss
    from PIL import Image

    monitor = None

    with mss.mss() as sct:

        # Find primary monitor
        for monitor in sct.monitors:
            if monitor["left"] == 0 and monitor["top"] == 0:
                break

        sct_img = sct.grab(monitor)

    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

    return img


def select_rectangle_on_screen(screenshot, info=''):
    """
    Presents the user with a window which allows him/her to select
    a rectangle on the screen and returns the coordinates in the carthesian
    coordinate system
    """
    global coordinates

    try:
        SnippingTool(screenshot, info=info)
        return coordinates
    except KeyboardInterrupt:
        return

class SnippingTool():
    def __init__(self, image, info=''):
        """
        Starts a full screen snipping tool for selecting coordinates
        """
        import tkinter as tk
        from tkinter.font import Font

        from PIL import ImageTk

        self.root = tk.Tk()

        self.root.bind("<Escape>", self._quit)

        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()

        # Change window to size of full screen
        self.root.geometry("{}x{}".format(w, h))

        # Bring window to full screen and top most level
        self.root.attributes('-fullscreen', True)
        self.root.attributes("-topmost", True)

        # Keep reference of some things
        self.x = self.y = 0
        self.rect = None
        self.start_x = None
        self.start_y = None

        # Create the canvas
        self.canvas = tk.Canvas(
            self.root,
            width=w,
            height=h,
            cursor="crosshair")

        self.canvas.pack()

        # Add the screenshot
        img = ImageTk.PhotoImage(image, master=self.root)

        self.canvas.create_image(
            (0, 0), image=img, anchor="nw")

        # Connect the event handlers
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        if info:
            font = Font(family='Helvetica', size=30)

            self.canvas.create_text(
                int(w/2), int(h*2/3), text=info, fill='#1B97F3', font=font
            )

        self.root.mainloop()

    def _quit(self):
        self.root.destroy()

    def on_button_press(self, event):
        # Update coordinates
        self.start_x = event.x
        self.start_y = event.y

        # If no rectangle is drawn yet, draw one
        if not self.rect:
            self.rect = self.canvas.create_rectangle(
                self.x, self.y, 1, 1, outline="#ff0000",
                fill="#1B97F3", stipple="gray12")

    def on_move_press(self, event):
        # Update coordinates
        self.end_x, self.end_y = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x,
                           self.start_y, self.end_x, self.end_y)

    def on_button_release(self, event):
        # Update global variable
        global coordinates

        if hasattr(self, 'end_x'):
            coordinates = (
                min(self.start_x, self.end_x),
                min(self.start_y, self.end_y),
                max(self.start_x, self.end_x),
                max(self.start_y, self.end_y)
            )

            # Close the window
            self.root.quit()
            self.root.destroy()


def image_recorder():
    
    sg.ChangeLookAndFeel("SystemDefault")

    # Prompt to instruct the user
    text = sg.Text('Clique em IMG, IMG_OCR e selecione o retângulo do elemento de interface na tela ou OCR.',
                   background_color="#2196F3", text_color="white")

    choices = ['IMG', 'IMG_OCR', 'OCR', 'CANCEL']

    buttons = [
        sg.Button(choice, button_color=("white", "#0069C0")) for choice in choices
    ]

    layout = [[text], buttons]

    window2 = sg.Window(
        "",
        layout,
        # icon="icon.ico",
        no_titlebar=True,
        background_color="#2196F3",
        element_justification="center",
        use_default_focus=False,
        keep_on_top=True
    )

    choice, _ = window2.Read()  # Read button click from window
    window2.Close()
    del(window2)

    if choice == 'CANCEL':
        return choice
    elif 'IMG' not in choice:
        return 'OCR'    

    msg = 'Clique em TIMEOUT e selecione o objeto, se deseja gravar mudanças de aspecto da imagem a ser salva.'
    mensagem_timeout_predefinido(msg)

    screenshot = capture_screen()

    # Present the user with a selection window
    target = select_rectangle_on_screen(screenshot)
      
    im_crop = screenshot.crop(target)
    return im_crop


def region_recorder(msg_timeout: str=None):

    sg.ChangeLookAndFeel("SystemDefault")

    message = 'Click em OK e selecione a região da tela onde deverá ser procurada a imagem ou aplicado o OCR.'
    
    text = sg.Text(message, background_color="#2196F3", text_color="white")

    choices = ['OK', 'CANCEL']

    buttons = [
        sg.Button(choice, button_color=("white", "#0069C0")) for choice in choices
    ]

    layout = [[text], buttons]

    window3 = sg.Window(
        "Select Anchor",
        layout,
        # icon="icon.ico",
        no_titlebar=True,
        background_color="#2196F3",
        element_justification="center",
        use_default_focus=False,
        keep_on_top=True
    )

    choice, _ = window3.Read()
    window3.Close()
    del(window3)

    region = None
    if choice == 'OK':
        if msg_timeout:
            mensagem_timeout_predefinido(msg_timeout)
        screenshot = capture_screen()
        region = select_rectangle_on_screen(screenshot)

    return region


def mensagem_timeout_predefinido(msg: str, timeout: bool=True):

    sg.ChangeLookAndFeel("SystemDefault")

    region = None

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

    return region
