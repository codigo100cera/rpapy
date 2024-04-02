import os
from pathlib import Path

from dotenv import load_dotenv

basedir = Path.cwd()
load_dotenv()


class Config:

    BASE_DIR = os.environ.get('BASE_DIR_RPAPY') or basedir

    RESOURCES_DIR_NAME = os.environ.get('RESOURCES_DIR_NAME') or 'resources'
    RESOURCES_KEYWORDS_FILE_NAME = os.environ.get('RESOURCES_KEYWORDS_FILE_NAME') or 'keywords.robot'
    IMAGES_DIR_NAME = os.environ.get('IMAGES_DIR_NAME') or 'images'
    IMAGES_ERROR_DIR_NAME = os.environ.get('IMAGES_ERROR_DIR_NAME') or 'images_error'
    TASKS_DIR_NAME = os.environ.get('TASKS_DIR_NAME') or 'tasks'
    MAX_WAIT_MAINTENANCE = int(os.environ.get('MAX_WAIT_MAINTENANCE') or 5)
    CHECK_MODE = os.environ.get('CHECK_MODE') or False
    FAILSAFE_OFF = os.environ.get('FAILSAFE_OFF') or False
    ACTIVE_TEMPORARY_ARCHIVE = os.environ.get('ACTIVE_TEMPORARY_ARCHIVE') or False
    TEMPORALY_FILE_NAME = os.environ.get('TEMPORALY_FILE_NAME') or 'temp.txt'


    RESOURCES_DIR_PATH = Path(BASE_DIR, RESOURCES_DIR_NAME)
    IMAGES_DIR_PATH =  RESOURCES_DIR_PATH / IMAGES_DIR_NAME
    ERROR_IMAGES_DIR_PATH = RESOURCES_DIR_PATH / IMAGES_ERROR_DIR_NAME



    @classmethod
    def get_config(cls):
        return (f"""***ENVIRONMENT VARIABLES***
                
            BASE_DIR={cls.BASE_DIR}
            RESOURCES_DIR_NAME={cls.RESOURCES_DIR_NAME}
            RESOURCES_KEYWORDS_FILE_NAME={cls.RESOURCES_KEYWORDS_FILE_NAME}
            IMAGES_DIR_NAME={cls.IMAGES_DIR_NAME}
            IMAGES_ERROR_DIR_NAME={cls.IMAGES_ERROR_DIR_NAME}
            TASKS_DIR_NAME={cls.TASKS_DIR_NAME}
            MAX_WAIT_MAINTENANCE={cls.MAX_WAIT_MAINTENANCE}
            CHECK_MODE={cls.CHECK_MODE}
            FAILSAFE_OFF={cls.FAILSAFE_OFF}
            ACTIVE_TEMPORARY_ARCHIVE={cls.ACTIVE_TEMPORARY_ARCHIVE}
            TEMPORALY_FILE_NAME={cls.TEMPORALY_FILE_NAME}
        """)
