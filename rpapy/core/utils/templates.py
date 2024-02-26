"""[summary]
"""
##########################################################################################

VARIAVEIS_AMBIENTE = """###VARIAVEIS DE AMBIENTE PYTHON-DOTENV

#RESOURCES_DIR_NAME=resources
#RESOURCES_KEYWORDS_FILE_NAME=keywords.robot
#IMAGES_DIR_NAME=images
#IMAGES_ERROR_DIR_NAME=images_error
#TASKS_DIR_NAME=tasks
#MAX_WAIT_MANUTENCAO=5
#VERIFICAR_MODO=True
#ARQUIVO_TEMPORARIO_ATIVO=False
#NOME_ARQUIVO_TEMPORARIO=temp.txt
#ONLY_IMAGE_PATH=False
"""

##########################################################################################
MODULES_IMPORT_PY = '''"""[summary]
"""

import time
from pathlib import Path

import pyautogui
import pytesseract as ocr
from pywinauto import Desktop
from rpapy.activities import (click_coord, click_vision, contextlib, double_click_coord, 
                              double_click_vision, drag_to_vision, drag_vision, get_element_coord, 
                              get_element_vision, get_path_by_image_name, get_text_ocr_region, 
                              get_text_ocr_vision, get_windows_title, max_wait_attr, open_executable, 
                              prepare_text_to_pyautogui, registrar_credencial, toast_process_start_notifier, 
                              triple_click_coord, triple_click_vision, wait_element_vision, write_text_coord, 
                              write_text_vision)
from rpapy.core.localizador import (ImageNotFoundError, LocalizadorImagem,
                                    image_optmization, max_wait_attr)

#######################DEFINE#######################
toast_process_start_notifier()
get_coordenadas = LocalizadorImagem()
#######################DEFINE#######################


'''
##########################################################################################

MODULES_IMPORT_ROBOT = '''*** Settings ***
Documentation    Documentação da Suite de Tasks Robot Framework

Library     rpapy.activities
Resource    ../resources/keywords.robot
  
*** Variables ***
${VAR}=      Everybody


*** Tasks ***
Tarefa principal
    Keyword principal


*** Keywords ***
Keyword principal
    Primeira Keyword        ${VAR}
'''

##########################################################################################
MODULES_IMPORT_RESOURCE = '''*** Settings ***
Documentation    Documentacao das Keywords da Suite de Tasks
Library     rpapy.activities
  

*** Variables ***
${VAR}=      variables


*** Keywords ***
Primeira Keyword
    [Arguments]         ${arg}
    Log To Console      Hello ${arg}!
'''

##########################################################################################
MSG_OPCOES_IMG = """
***ATENÇÃO***
Insira os parâmetros na sequência de 1 a 5, conforme o necessário, 
deixando-os separados apenas por espaço. 

1. Insirá o nome da imagem separado com o padrão snake_case e sem
caracteres especiais.

2. Templates-> 0=localizador | 1=pywinauto | 2=pyautogui | 3=Activities  
             | 4=OCR -> (backend=ocr; lang=por|eng|...)

3. Backend:_________4. Método:______________5. Param:
uia | win32 | gui _______1_click________________(opcional)
uia | win32 | xxx _______2_click_input___________(opcional)
uia | win32 | gui _______3_double_click_________(opcional)
uia | win32 | xxx _______4_double_click_input____(opcional)
uia | win32 | gui _______5_select/get_element____(obrigatório)
uia | win32 | gui _______6_type_keys___________(obrigatório)
uia | win32 | gui _______7_wait_element_________(opcional)
ocr | xxxxx | xxx _______8_ocr_img_to_text_______(obrigatório)
"""
##########################################################################################
MSG_OPCOES_OCR_PY = """
***ATENÇÃO***
Insira os parâmetros na sequência de 1 a 3, deixando-os 
separados apenas por espaço.

1. Insirá o nome da variável que armazenará o texto 
   recuperado pelo OCR e o template a ser utilizado.

2. Templates ->  1 | 2 - arquivo.py

3. Idioma ->  por | eng | ...

"""

##########################################################################################
MSG_OPCOES_OCR_ROBOT = """
***ATENÇÃO***
Insira os parâmetros na sequência de 1 a 3, deixando-os 
separados apenas por espaço.

1. Insirá o nome da variável que armazenará o texto 
   recuperado pelo OCR e o template a ser utilizado.

2. Template ->  1 - arquivo.robot

3. Idioma ->  por | eng | ...
"""

##########################################################################################
CONTROL_RPA_0 = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    xy_{0} = get_coordenadas('{0}')
"""

##########################################################################################
CONTROL_RPA_1 = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    xy_{0} = get_coordenadas('{0}')
    {0} = Desktop(backend='{1}').from_point(*xy_{0})
    max_wait_attr({0}, '{2}', max_wait=5.0)
    {0}.{2}({3})
"""

##########################################################################################
CONTROL_RPA_2 = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    xy_{0} = get_coordenadas('{0}')
    pyautogui.moveTo(*xy_{0})
    pyautogui.{1}({2})
"""

##########################################################################################
CONTROL_RPA_OCR_PY = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    im_{0} = pyautogui.screenshot(region={1})
    str_{0} = ocr.image_to_string(im_{0}, lang='{2}')
    print('>>>>str_ocr>>>>', str_{0})
    # im_{0}.show()
"""

##########################################################################################
CONTROL_RPA_OCR_IMG_PY = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    get_text_ocr_vision('{0}', region={1}, lang='{2}', identifier_img=get_coordenadas, 
                        max_wait=30, wait_vanish=False, ignore_error=False)
"""

##########################################################################################
CLICK_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    Click Vision    {0}    backend={1}    max_wait=30.0
    ...    button=left    delay=0.0    before=0.0   after=0.0
"""

##########################################################################################
DOUBLE_CLICK_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    Double Click Vision    {0}    backend={1}    max_wait=30.0
    ...    button=left    delay=0.0    before=0.0   after=0.0
    ...    move_x=0    move_y=0    ignore_error=$^~False$~
"""

##########################################################################################
WRITE_TEXT_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    Write Text Vision    {0}    backend={1}
    ...    wait_attr=5.0,    text={2}
    ...    max_wait=30.0    delay=0.0    before=0.0   after=0.0
    ...    move_x=0    move_y=0    ignore_error=$^~False$~
"""

##########################################################################################
TRIPLE_CLICK_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    Triple Click Vision    {0}    backend={1}    max_wait=30.0
    ...    button=left    delay=0.0    before=0.0   after=0.0
    ...    move_x=0    move_y=0    ignore_error=$^~False$~
"""

##########################################################################################
GET_ELEMENT_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    Get Element Vision    {0}    backend={1}    max_wait=30.0
    ...    execute=$^~True$~    args=$^~^~ {2} $~$~    kwargs=$^~^~ ^~$~ $~$~
    ...    attr_name=select     wait_attr=5.0     vanish=$^~False$~
    ...    delay=0.0    before=0.0    after=0.0
    ...    move_x=0    move_y=0    ignore_error=$^~False$~
"""

##########################################################################################
WAIT_ELEMENT_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    Wait Element Vision    {0}    max_wait=30.0    wait_vanish=$^~False$~   ignore_error=$^~False$~
"""

##########################################################################################
GET_TEXT_OCR_VISION_ROBOT = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    $^~str_{0}$~    Get Text Ocr Vision    {0}    region=$^~^~{1}$~$~    lang=$^~{2}$~
    ...    max_wait=30.0    wait_vanish=$^~False$~    ignore_error=$^~False$~
    ...    Log To Console    $^~str_{0}$~

"""

##########################################################################################
GET_TEXT_OCR_REGION_ROBOT = """
    # [Contexto - Janela]: 
    # [Descricao]: {0}
    $^~str_{0}$~    Get Text Ocr Region    region=$^~^~{1}$~$~    lang=$^~{2}$~
    ...    Log To Console    $^~str_{0}$~
"""

##########################################################################################
class ActivityPy:    
    
    CLICK_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    click_vision('{0}', identifier_img=get_coordenadas, backend='{1}', button='left', 
                before=0.0, after=0.0, max_wait=30, move_x=0, move_y=0, ignore_error=False)
    """

    DOUBLE_CLICK_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    double_click_vision('{0}', identifier_img=get_coordenadas, backend='{1}', button='left', 
                        before=0.0, after=0.0, max_wait=30, move_x=0, move_y=0, ignore_error=False)
    """

    WRITE_TEXT_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]:
    {0} = '{2}' 
    write_text_vision('{0}', text={0}, identifier_img=get_coordenadas, backend='{1}', max_wait=30, 
                        wait_vanish=False, move_x=0, move_y=0, before=0.0, after=0.0, interval=None, 
                        confidence=None, wait_attr=5, ignore_error=False)
    """

    TRIPLE_CLICK_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    triple_click_vision('{0}', identifier_img=get_coordenadas, backend='{1}', button='left', 
                        before=0.0, after=0.0, max_wait=30, move_x=0, move_y=0, ignore_error=False)
    """

    GET_ELEMENT_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    {0} = get_element_vision('{0}', attr_name='{1}', identifier_img=get_coordenadas, backend='{2}',  
                            max_wait=30,  move_x=0, move_y=0, ignore_error=False, confidence=None, 
                            wait_vanish=False, interval=None, before=0.0, after=0.0, wait_attr=5.0, 
                            execute=False, arguments=(), kwarguments=^~$~)
    """

    WAIT_ELEMENT_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    wait_element_vision('{0}', identifier_img=get_coordenadas, backend='{1}',
                        max_wait=30, wait_vanish=False, ignore_error=False)
    """

    GET_TEXT_OCR_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    str_{0} = get_text_ocr_vision('{0}', backend={1}, region={2}, lang='{3}', identifier_img=get_coordenadas, 
                        max_wait=30, wait_vanish=False, ignore_error=False)
    print('>>>>str_ocr>>>>', str_{0})
    """

    GET_TEXT_OCR_REGION = """
    # [Contexto - Janela]: 
    # [Descricao]: {0}
    str_{0} = get_text_ocr_region(region={1}, lang='{2}')
    print('>>>>str_ocr>>>>', str_{0})
    """    
    

##########################################################################################
class ActivityRobot:
    
    CLICK_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    Click Vision    {0}    backend={1}    max_wait=30.0
    ...    button=left    delay=0.0    before=0.0   after=0.0
    """
    
    DOUBLE_CLICK_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    Double Click Vision    {0}    backend={1}    max_wait=30.0
    ...    button=left    delay=0.0    before=0.0   after=0.0
    ...    move_x=0    move_y=0    ignore_error=$^~False$~
    """

    WRITE_TEXT_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    Write Text Vision    {0}    backend={1}
    ...    wait_attr=5.0    text={2}
    ...    max_wait=30.0    delay=0.0    before=0.0   after=0.0
    ...    move_x=0    move_y=0    ignore_error=$^~False$~
    """
    TRIPLE_CLICK_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    Triple Click Vision    {0}    backend={1}    max_wait=30.0
    ...    button=left    delay=0.0    before=0.0   after=0.0
    ...    move_x=0    move_y=0    ignore_error=$^~False$~
    """

    GET_ELEMENT_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    Get Element Vision    {0}    backend={1}    max_wait=30.0
    ...    execute=$^~True$~    arguments=$^~^~ {2} $~$~    kwarguments=$^~^~ ^~$~ $~$~
    ...    attr_name=select     wait_attr=5.0     vanish=$^~False$~
    ...    delay=0.0    before=0.0    after=0.0
    ...    move_x=0    move_y=0    ignore_error=$^~False$~
    """

    WAIT_ELEMENT_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    Wait Element Vision    {0}    max_wait=30.0    wait_vanish=$^~False$~   ignore_error=$^~False$~
    """

    GET_TEXT_OCR_VISION = """
    # [Contexto - Janela]: 
    # [Descricao]: 
    $^~str_{0}$~    Get Text Ocr Vision    {0}    backend={1}    region={2}
    ...    lang={3}    max_wait=30.0    wait_vanish=$^~False$~    ignore_error=$^~False$~
    Log To Console     $^~str_{0}$~
    """

    GET_TEXT_OCR_REGION = """
    # [Contexto - Janela]: 
    # [Descricao]: {0}
    $^~str_{0}$~    Get Text Ocr Region    region=$^~^~{1}$~$~    lang={2}
    ...    Log To Console     $^~str_{0}$~
    """    
