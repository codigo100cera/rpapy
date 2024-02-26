import time
from pathlib import Path
from typing import Optional

from PIL import Image
from rpapy.core.config import Config
from rpapy.core.loads import create_python_default_dirs
from rpapy.core.snipps.codesnippets import add_new_activity
from rpapy.core.snipps.snippingtools import (ImageNotFoundError,
                                             close_window_with_title,
                                             record_image, record_region,
                                             remove_duplicate_images,
                                             show_image_crop)
from rpapy.core.utils.messages import confirm_ok_cancel


def capture_image_crop(file_name:str=None)-> Optional[bool]:    
    
    if file_name is not None and ('.py' not in file_name.lower() and '.robot' not in file_name.lower()):
        raise Exception('O nome do arquivo deve ter a extensão .py ou .robot')

    create_python_default_dirs()
    resources_path = Path(Config.BASE_DIR, Config.RESOURCES_DIR_NAME)
    images_dir_path = resources_path / Config.IMAGES_DIR_NAME
    
    msg = 'Clique em IMG, IMG_OCR e selecione o retângulo do elemento de interface na tela ou OCR.'
    snippet_type = None
    im_crop = record_image(msg)      # Funcao para capiturar o recorte da imagem no screenshot da tela principar
    if im_crop == 'CANCEL':
        return    
        
    region = record_region()      # Funcao para capiturar as coordenadas da região onde o robo deverá procurar a imagem
    if region is None:
        return
    
    if isinstance(im_crop, Image.Image):
        snippet_type = 'IMG'
    else:
        snippet_type = 'OCR'

    image_name = add_new_activity(file_name, snippet_type, region)
    if image_name is None:
        return
    
    if 'OCR' != snippet_type:
        remove_duplicate_images(image_name, dir_name_imgs=images_dir_path)

        im_crop.save(f'{images_dir_path}/{image_name}-{region}.png', 'PNG')
        
        if confirm_ok_cancel('Deseja visualizar a imagem adicionada?'):
            show_image_crop(im_crop, timeout=5000)
            
    return True


def update_image(image_name_path: str)-> bool:

    """Ulizado quando o RPA esta no modo manutenção para efetuar a troca da imagem que não foi encontrada
    
    Arguments:
        image_name_path {str} -- [path absoluto do nome imagem para ser trocada]
    
    Raises:
        ImageNotFoundError: [Exception lançada quando a troca da img for cancelada]
    
    Returns:
        [bool] -- [retorna True se a imagem foi trocada, senão False]
    """
    
    create_python_default_dirs()
    resources_path = Path(Config.BASE_DIR, Config.RESOURCES_DIR_NAME)
    images_dir_path = resources_path / Config.IMAGES_DIR_NAME

    # Recupera apenas o nome da imagem sem dados da região para utilizar na capitura da nova imagem
    image_name = image_name_path.split('/')[-1].split('-')[0]

    # Abre a imagem a ser trocada para ser exibida pelo visualizador de imagens
    im_crop = Image.open(image_name_path)
    im_crop.show()

    # Apresenta aviso de confirmação com nome do path absoluto da imagem que será trocada,
    # Lança a exception caso a troca seja cancelada na caixa de confirmação
    if not confirm_ok_cancel(f'A imagem "{image_name}" será alterada!'):
        close_window_with_title('Fotos')
        raise ImageNotFoundError('A imagem "{image_name}" não foi encontrada.')

    close_window_with_title('Fotos')
    
    msg = 'Clique em IMG e selecione o retângulo do elemento de interface na tela'
    im_crop = record_image(msg, choices=['IMG', 'CANCEL'])      # Funcao para capiturar o recorte da imagem no screenshot da tela principar
    if im_crop == 'CANCEL':
        return False
        
    region = record_region()      # Funcao para capiturar as coordenadas da região onde o robo deverá procurar a imagem
    if region is None:
        return False
    
    if not isinstance(im_crop, Image.Image):
        raise Exception('Ocorreu um erro inesperado o recorte não é um objeto Image.')

    if not confirm_ok_cancel(f'Nome da imagem que será substituida: \n"{image_name}"'):
        return False

    remove_duplicate_images(image_name, dir_name_imgs=images_dir_path)

    im_crop.save(f'{images_dir_path}/{image_name}-{region}.png', 'PNG')
    
    if confirm_ok_cancel('Deseja visualizar a imagem adicionada?'):
        # im_crop.show()
        # # Fecha janela do visualizador de imagem após confirmacao de troca
        # close_window_with_title('Fotos')
        show_image_crop(im_crop, timeout=5000)
        time.sleep(.5)
        
    return True
