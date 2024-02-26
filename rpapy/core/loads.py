import contextlib
import os
from pathlib import Path

import pyautogui

from .config import Config
from .utils import templates


def load_robot_example():

    from rpapy.core.utils.example import paint_robot

    text = f'***ATENÇÃO***\n\nAlguns arquivos poderão ser substituidos!\nVocê deseja carregar a implementação de exemplo do robo-rpapy?'
    opcao = pyautogui.confirm(text=text, title='RPA-PY', buttons=['OK','CANCEL'])        
    if opcao is None or opcao == 'CANCEL':
        return

    pyautogui.alert(title='ATENÇÃO!', text='Após terminar de carregar os arquivos, execute\no seguinte comando no terminal:\n\nrobot -d log tasks')

    create_example_default_dirs()
    create_robot_default_dirs()

    # The directory containing this file
    HERE = os.path.abspath(os.path.dirname(__file__))
    
    path_desenho_robotframework = Path(Config.BASE_DIR, 'resources/desenhos/robotframework.txt')
    replace_file_confirm(path_desenho_robotframework, paint_robot.ROBOTFRAMEWORK)
    
    path_desenho_borboleta = Path(Config.BASE_DIR, 'resources/desenhos/borboleta.txt')
    replace_file_confirm(path_desenho_borboleta, paint_robot.BORBOLETA)
    
    path_custom_keywords = Path(Config.BASE_DIR, 'resources/custom_keywords.py')
    replace_file_confirm(path_custom_keywords, paint_robot.CUSTOM_KEYWORDS)
    
    path_keywords = Path(Config.BASE_DIR, 'resources/keywords.robot')
    replace_file_confirm(path_keywords, paint_robot.KEYWORDS_ROBOT)
    
    path_main_robot = Path(Config.BASE_DIR, 'tasks/main.robot')
    replace_file_confirm(path_main_robot, paint_robot.MAIN_ROBOT)


def replace_file_confirm(path_file: Path, content: str):
    if path_file.exists():
        text = f'O arquivo "{path_file.name}" será subistuido, para confirmar clique em OK.'
        opcao = pyautogui.confirm(text=text, title='RPA-PY', buttons=['OK','CANCEL'])        
        if opcao is not None or opcao != 'CANCEL':
            if '.py' not in path_file.name:
                path_file.write_text(content, encoding='utf-8')
            else:
                path_file.write_text(content)
    else:
        if '.py' not in path_file.name:
                path_file.write_text(content, encoding='utf-8')
        else:
            path_file.write_text(content)


def create_robot_default_dirs():

    path_dir_task = Path(Config.BASE_DIR, Config.TASKS_DIR_NAME)
    with contextlib.suppress(FileExistsError):
        path_dir_task.mkdir()

    create_python_default_dirs()  


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


def create_example_default_dirs():
    
    create_python_default_dirs()
    path_desenhos_dir = Path(Config.BASE_DIR, Config.RESOURCES_DIR_NAME, 'desenhos')
    with contextlib.suppress(FileExistsError):
        path_desenhos_dir.mkdir()


def create_default_script_file(*, file_name:str=None, default_name:str='main.robot'):    
    if file_name is None:
        file_name = pyautogui.prompt(text='Insirá o nome do arquivo com extensão .robot ou .py', title='Alteração de Arquivo', default=default_name)    
        if file_name is None:
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
