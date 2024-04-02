import contextlib
from pathlib import Path
from typing import Dict, List

import pyautogui
import pyperclip

from rpapy.core.config import Config
from rpapy.core.snipps import templates
from rpapy.core.snipps.loads import (create_default_script_file,
                                     create_robot_default_dirs)
from rpapy.core.snipps.snippingtools import record_region


class ParamNotFoundError(Exception):
    pass


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


def add_new_activity(file_name, snippet_type, region):
    default = image_name = ''
    while image_name.strip() == '':
        if snippet_type == 'OCR':
            msg_text = templates.MSG_OPCOES_OCR_PY if '.py' in file_name.lower() \
                                                    else templates.MSG_OPCOES_OCR_ROBOT            
            image_name = pyautogui.prompt(text=msg_text, title='RPA-PY', default=default)
        else:
            image_name = pyautogui.prompt(text=templates.MSG_OPCOES_IMG, title='RPA-PY', default=default)                
        
        if image_name is None:
            return
        
        if image_name.strip() == '':
            continue
        
        parametros = image_name.split()
        parametros[0] = parametros[0].replace('-','_').lower()        
        parametros = [file_name] + parametros

        region_ocr_img = None
        with contextlib.suppress(IndexError):
            if parametros[3] == 'ocr' and snippet_type != 'OCR':
                region_ocr_img = record_region(msg_timeout='Selecione a região da tela onde será aplicado o OCR.')
                if region_ocr_img is None:
                    return
        try:
            writing_code_snippet(*parametros, snippet_type=snippet_type, region=region, region_ocr_img=region_ocr_img)
            image_name = parametros[1]
        except ParamNotFoundError as error:
            pyautogui.alert(title='RPAPY', text=str(error))
            default = ''
            with contextlib.suppress(Exception) as target:
                default = ' '.join(parametros[1:])            
            image_name = ''
    else:
        return image_name


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

    create_default_script_file(file_name=nome_arquivo)
        
    # Decide qual arquivo será aberto para escrita do snippet de código
    if Config.ACTIVE_TEMPORARY_ARCHIVE:
        path_file = Path(Config.BASE_DIR, Config.TEMPORALY_FILE_NAME)
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
