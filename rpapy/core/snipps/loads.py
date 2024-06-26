import contextlib
import os
import shutil
from pathlib import Path
from typing import Dict, Tuple

import pyautogui

from rpapy.core.utils.messages import confirm_ok_cancel, prompt

from ..config import Config


def create_python_default_dirs():
    path_dir_resources = Path(Config.BASE_DIR, Config.RESOURCES_DIR_NAME)
    with contextlib.suppress(FileExistsError):
        path_dir_resources.mkdir()

    path_dir_images = Path(path_dir_resources, Config.IMAGES_DIR_NAME)
    with contextlib.suppress(FileExistsError):
        path_dir_images.mkdir()

    error_images_dir_path = path_dir_resources / Config.IMAGES_ERROR_DIR_NAME
    with contextlib.suppress(FileExistsError):
        error_images_dir_path.mkdir()


def replace_file_confirm(path_file: Path, content: str = None,* , origin_file: Path = None):
    if path_file.exists():
        text = f'O arquivo "{path_file.name}" será subistuido, para confirmar clique em OK.'
        opcao = confirm_ok_cancel(text=text, title='RPA-PY')        
        if opcao:
            if '.py' in path_file.name:
                path_file.write_text(content)
            elif '.svg' in path_file.name:
                shutil.copy(origin_file, path_file)
            else:
                path_file.write_text(content, encoding='utf-8')            
    else:
        if '.py' in path_file.name:
                path_file.write_text(content)
        elif '.svg' in path_file.name:
            shutil.copy(origin_file, path_file)
        else:
            path_file.write_text(content, encoding='utf-8')


def load_robot_example():

    from rpapy.core.utils.example import paint_robot

    text = f'***ATENÇÃO***\n\nAlguns arquivos poderão ser substituidos!\nVocê deseja carregar a implementação de exemplo do robo-rpapy?'
    opcao = confirm_ok_cancel(text=text, title='RPA-PY')        
    if not opcao:
        return

    pyautogui.alert(title='ATENÇÃO!', text='Após terminar de carregar os arquivos, execute\no seguinte comando no terminal:\n\nrobot -d log tasks')

    create_example_default_dirs()
    create_robot_default_dirs()

    # The directory containing this file
    HERE = os.path.abspath(os.path.dirname(__file__))
    
    path_desenho_codigo100cera = Path(Config.BASE_DIR, 'resources/desenhos/codigo100cera.txt')
    replace_file_confirm(path_desenho_codigo100cera, paint_robot.CODIGO100CERA)
    
    path_custom_keywords = Path(Config.BASE_DIR, 'resources/custom_keywords.py')
    replace_file_confirm(path_custom_keywords, paint_robot.CUSTOM_KEYWORDS)
    
    path_keywords = Path(Config.BASE_DIR, 'resources/keywords.robot')
    replace_file_confirm(path_keywords, paint_robot.KEYWORDS_ROBOT)
    
    path_main_robot = Path(Config.BASE_DIR, 'tasks/main.robot')
    replace_file_confirm(path_main_robot, paint_robot.MAIN_ROBOT)

    origin_file_svg = Path(HERE) / 'utils/imagens/template_win11_screen_1920x1080.svg'
    svg_template_path = Path(Config.BASE_DIR, 'resources/desenhos/template_win11_screen_1920x1080.svg')
    replace_file_confirm(svg_template_path, origin_file=origin_file_svg)


def create_robot_default_dirs():
    path_dir_task = Path(Config.BASE_DIR, Config.TASKS_DIR_NAME)
    with contextlib.suppress(FileExistsError):
        path_dir_task.mkdir()

    create_python_default_dirs()  


def create_example_default_dirs():    
    create_python_default_dirs()
    draw_dir_path = Path(Config.BASE_DIR, Config.RESOURCES_DIR_NAME, 'desenhos')
    with contextlib.suppress(FileExistsError):
        draw_dir_path.mkdir()


def create_default_script_file(*, file_name:str=None, default_name:str='main.robot'):
    from . import templates

    if file_name is None:
        file_name = prompt(text='Insirá o nome do arquivo com extensão .robot ou .py', title='Alteração de Arquivo', default=default_name)
        if file_name is False:
            return

    file_name = default_name if file_name is None or file_name.strip() == '' else file_name

    name, extention, *_ = file_name.lower().split('.')

    file_name = file_name if extention == 'py' or extention == 'robot' else f'{name}.robot'

    path_file = Path(Config.BASE_DIR, file_name)
    path_file_env = Path(Config.BASE_DIR, '.env')

    MODULES_IMPORT = templates.MODULES_IMPORT_PY
        
    if extention == 'robot':
        create_robot_default_dirs()
        
        path_file = Path(Config.TASKS_DIR_NAME) / file_name
        MODULES_IMPORT = templates.MODULES_IMPORT_ROBOT
        
        path_file_keywords = Path(Config.RESOURCES_DIR_NAME) / Config.RESOURCES_KEYWORDS_FILE_NAME
        if not path_file_keywords.exists():
            path_file_keywords.touch()
            path_file_keywords.write_text('\n'.join(templates.MODULES_IMPORT_RESOURCE.splitlines()), encoding='utf-8')
    
    if not path_file_env.exists():
        path_file_env.touch()
        path_file_env.write_text(templates.VARIAVEIS_AMBIENTE,encoding='utf-8')
    
    if not path_file.exists():
        path_file.touch()

    content = path_file.read_text().splitlines()

    # Inclui os imports padrões no inicio do arquivo quando não for encontrado nenhuma palavra "import" ou
    #  *** Settings *** nos arquivos .py ou .robot 
    if 'import' not in '\n'.join(content) and '*** Settings ***' not in '\n'.join(content):    
        content = MODULES_IMPORT.splitlines() + content

        if extention == 'robot':
            path_file.write_text('\n'.join(content), encoding='utf-8')
        else:
            path_file.write_text('\n'.join(content))

    return file_name
