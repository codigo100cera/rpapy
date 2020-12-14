import os
from .config import Config
from pathlib import Path
import contextlib 
import pyautogui


def upload_robot():

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
    create_file_confirm(path_desenho_robotframework, paint_robot.ROBOTFRAMEWORK)
    
    path_desenho_borboleta = Path(Config.BASE_DIR, 'resources/desenhos/borboleta.txt')
    create_file_confirm(path_desenho_borboleta, paint_robot.BORBOLETA)
    
    path_custom_keywords = Path(Config.BASE_DIR, 'resources/custom_keywords.py')
    create_file_confirm(path_custom_keywords, paint_robot.CUSTOM_KEYWORDS)
    
    path_keywords = Path(Config.BASE_DIR, 'resources/keywords.robot')
    create_file_confirm(path_keywords, paint_robot.KEYWORDS_ROBOT)
    
    path_main_robot = Path(Config.BASE_DIR, 'tasks/main.robot')
    create_file_confirm(path_main_robot, paint_robot.MAIN_ROBOT)


def create_file_confirm(path_file: Path, content: str):
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


def create_example_default_dirs():
    
    create_python_default_dirs()
    path_desenhos_dir = Path(Config.BASE_DIR, Config.RESOURCES_DIR_NAME, 'desenhos')
    with contextlib.suppress(FileExistsError):
        path_desenhos_dir.mkdir()