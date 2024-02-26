import os
from pathlib import Path

from dotenv import load_dotenv

basedir = Path.cwd()
load_dotenv(os.path.join(basedir, '.env'))

CONFIG = """
***VARIÁVEIS DE AMBIENTE***

BASE_DIR={}
RESOURCES_DIR_NAME={}
RESOURCES_KEYWORDS_FILE_NAME={}
IMAGES_DIR_NAME={}
IMAGES_ERROR_DIR_NAME={}
TASKS_DIR_NAME={}
MAX_WAIT_MANUTENCAO={}
VERIFICAR_MODO={}
ARQUIVO_TEMPORARIO_ATIVO={}
NOME_ARQUIVO_TEMPORARIO={}
"""

class Config:

    BASE_DIR = os.environ.get('BASE_DIR_RPAPY') or basedir

    RESOURCES_DIR_NAME = os.environ.get('RESOURCES_DIR_NAME') or 'resources'
    RESOURCES_KEYWORDS_FILE_NAME = os.environ.get('RESOURCES_KEYWORDS_FILE_NAME') or 'keywords.robot'
    IMAGES_DIR_NAME = os.environ.get('IMAGES_DIR_NAME') or 'images'
    IMAGES_ERROR_DIR_NAME = os.environ.get('IMAGES_ERROR_DIR_NAME') or 'images_error'
    TASKS_DIR_NAME = os.environ.get('TASKS_DIR_NAME') or 'tasks'
    MAX_WAIT_MANUTENCAO = int(os.environ.get('MAX_WAIT_MANUTENCAO') or 5)
    VERIFICAR_MODO = bool(os.environ.get('VERIFICAR_MODO') or False)
    ARQUIVO_TEMPORARIO_ATIVO = bool(os.environ.get('ARQUIVO_TEMPORARIO_ATIVO') or False)
    NOME_ARQUIVO_TEMPORARIO = os.environ.get('NOME_ARQUIVO_TEMPORARIO') or 'temp.txt'


    @classmethod
    def get_config(cls):
        return CONFIG.format(
            cls.BASE_DIR,
            cls.RESOURCES_DIR_NAME,
            cls.RESOURCES_KEYWORDS_FILE_NAME,
            cls.IMAGES_DIR_NAME,
            cls.IMAGES_ERROR_DIR_NAME,
            cls.TASKS_DIR_NAME,
            cls.MAX_WAIT_MANUTENCAO,
            cls.VERIFICAR_MODO,
            cls.ARQUIVO_TEMPORARIO_ATIVO,
            cls.NOME_ARQUIVO_TEMPORARIO,
        )
