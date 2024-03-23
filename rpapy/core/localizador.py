import datetime
import os
import time
import warnings
from pathlib import Path
from typing import Dict, Tuple

import cv2
import numpy as np
import pyautogui
from PIL import Image

with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from pywinauto import Desktop

from rpapy.core.loads import create_python_default_dirs

from .config import Config
from .snipps import update_image
from .snipps.snippingtools import (ImageNotDisappearError, ImageNotFoundError,
                                   close_window_with_title)

MODO_MANUTENCAO = False
if Config.VERIFICAR_MODO:
    MODOS = {'SIM':True, 'NAO': False, None:'CANCEL'}
    MODO_MANUTENCAO = MODOS[pyautogui.confirm(title='RPAPY',text='Ativar o modo de manutenção?', buttons=['SIM', 'NAO'])]

if MODO_MANUTENCAO == 'CANCEL': 
    pyautogui.alert(title='RPAPY', text='O processo foi cancelado!')
    exit()

if MODO_MANUTENCAO is False:
    pyautogui.FAILSAFE = False

if Config.FAILSAFE_OFF:    
    pyautogui.FAILSAFE = False

path_base_dir = Path(Config.BASE_DIR)
path_dir_resources = Path(path_base_dir, Config.RESOURCES_DIR_NAME)
path_dir_images =  Path(path_dir_resources, Config.IMAGES_DIR_NAME)
path_dir_error_images = Path(path_dir_resources, Config.IMAGES_ERROR_DIR_NAME)


def localizar_na_tela(image, *args, **kwargs):
    try:
        img = Image.open(image)
        return pyautogui.locateOnScreen(img, *args, **kwargs)
    except ValueError:
        pass


class LocalizadorImagem():

    def __init__(self):
        self._screenshots: Dict[str, Dict[str, Tuple[int]]] = mapear_imagens()
        self.wait_before = 0.0
        self.debug = False
        self._interval = 0.2
        self._max_wait = Config.MAX_WAIT_MANUTENCAO if MODO_MANUTENCAO else 30
        self._modo_manutencao = MODO_MANUTENCAO

    def modo_manutencao(self, opcao: bool):
        if isinstance(opcao, bool):
            if opcao:
                self._modo_manutencao = opcao
                self._max_wait = 10
            else:
                self._modo_manutencao = opcao
                self._max_wait = 30

    @property
    def max_wait(self):
        return self._max_wait

    @max_wait.setter
    def max_wait(self, _max_wait):
        max_wait = float(_max_wait)
        if max_wait >= 0:
            self._max_wait = max_wait
        else:
            self._max_wait = 30
    
    @property
    def interval(self):
        return self.interval

    @interval.setter
    def interval(self, interval):
        if interval >= 0:
            self._interval = interval

    def __call__(self, image_name: str, *, max_wait: float=None, confidence: float=None, wait_vanish=False,
                interval: float=None, deslocar_x:int=0, deslocar_y:int=0) -> Tuple[int]:
        """Busca a imagem na tela até o tempo máximo definido por parâmetro, e retorna 
        a coordenada da imagem se encontrada, senão lança uma excessão personalizada ImageNotFoundError.
        Arguments:
            image {str} -- nome da imagem a ser recuperada no dicionário
        Keyword Arguments:
            max_wait {float} -- [tempo máximo de espera para encontra a imagem] (default: {None})
            interval {float} -- [intervalo de parada para busca da imagem] (default: {None})
            deslocar_x {int} -- [desloca o centro da localização da imagem no eixo x] (default: {0})
            deslocar_y {int} -- [desloca o centro da localização da imagem no eixo] (default: {0})
        Raises:
            ImageNotFoundError: [Excessão lançada quando a imagem não for encontrada dentro do prazo máximo]
        Returns:
            Tuple[int] -- [tupla contendo os valores (x, y) do centro da imagem identificada]
        """
        # Se True efetua uma parada a cada execução. Utilizado para reduzir a velocidade do bot.
        if self.debug:
            input(f'Localizar "{image_name}" - Pressione enter para continuar...')

        # Atribui ao interval_local o intervalo passado por parâmetro, de diferente de None
        if interval is not None:
            if interval > 0:
                interval_local = interval
            else:
                interval_local = self._interval
        else:
            interval_local = self._interval

        # Atribui ao max_wait_local o tempo máximo passado por parâmetro, se diferente de None
        if max_wait is not None:
            max_wait = float(max_wait)
            if max_wait > 0 and max_wait > interval_local:
                max_wait_local = max_wait
            else:
                max_wait_local = self._max_wait
        else:
            max_wait_local = self._max_wait
        
        # Efetua uma pausa antes de tentar encontrar a localização da imagem
        time.sleep(self.wait_before)

        # Move o mouse para um ponto de descanso na tela para não interferir na busca da imagem
        pyautogui.moveTo(700,5,0)

        # Inicia a coordenada com o padrão flag None
        coordenada = None

        # Armazena o início da execução do método para ser verificado com o max_wait
        start_time = time.time()

        if not wait_vanish:
            # Repete o bloco de codigo, enquanto variável coordenada for igual a None
            while coordenada is None:
                try:
                    # recupera a imagem do mapa, passando o nome enviado por parâmetro
                    image_region = self._screenshots[image_name]                
                except KeyError:
                    # Cria um arquivo com image_name no diretório images se não existir
                    im = Image.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'utils/imagens/IMAGEM_NAO_ENCONTRADA.png'))
                    im.save(f'{path_dir_images}/{image_name}-(300, 50, 700, 200).png', 'PNG')
                    time.sleep(1)
                    # Atualiza o mapa com a imagem criada com o paramêtro image_name.
                    self._screenshots = mapear_imagens()
                    continue
                
                try:
                    # Executa o bloco else se a imagem for encontrada no mapa e efetua um continue para sair do loop
                    if confidence is None:
                        coordenada = localizar_na_tela(**image_region)
                    else:
                        coordenada = localizar_na_tela(**image_region, confidence=confidence)

                    if coordenada is not None:
                        continue
                except Exception:
                    coordenada = None
                    
                # Entra no bloco se o tempo de execução do loop exceder o max_wait.
                if time.time() - start_time > max_wait_local:
                    if self._modo_manutencao:
                        atualizou = update_image(image_region.get('image'))
                        if atualizou:
                            self._screenshots = mapear_imagens()
                            image_region = self._screenshots[image_name]
                        start_time = time.time()
                    else:
                        # Efetua um print da tela no momento em que ocorreu o erro
                        image_not_found_error = pyautogui.screenshot()
                        # Salva o print da tela com o nome da imagem que não foi encontrada, incluindo data e hora
                        salvar_img_error(image_name, image_not_found_error)
                        # Lança a exceção de imagem não encotrada.
                        raise ImageNotFoundError(f'A imagem "{image_name}", não foi encontrada!')

                # Efetua um intervalo de parada entre os loop de tentativa de encontrar a imagem
                time.sleep(interval_local)
            else:
                # Se o loop for encerrado na condicional do while, este bloco é executado.            
                # Recupera a coordenada x,y do centro da imagem encontrada.
                resultado = pyautogui.center(coordenada)
                # Retorna o resultado adionando os deslocamentos, se passados por parâmetro.
                return resultado[0] + int(deslocar_x), resultado[-1] + int(deslocar_y)
        
        else:
            # Armazena o início da execução do método para ser verificado com o max_wait
            start_time = time.time()

            # Define coordenada diferente de None para iniciar o loop while
            coordenada = True

            # Verifica se a imagem buscada na tela desapareceu            
            while coordenada is not None:
                try:
                    # recupera a imagem do mapa, passando o nome enviado por parâmetro
                    image_region = self._screenshots[image_name]                
                except KeyError as e:
                    # Se modo manutenção igual True, cria imagem provisória e atualiza a imagem recem criada no mapa
                    if self._modo_manutencao:
                        # Cria um arquivo com image_name no diretório images se não existir
                        im = pyautogui.screenshot(region=(1, 1, 300, 150))
                        im.save(f'{path_dir_images}/{image_name}-(300, 50, 350, 200).png', 'PNG')
                        time.sleep(1)
                        # Atualiza o mapa com a imagem criada com o paramêtro image_name.
                        self._screenshots = mapear_imagens()
                        # recupera a imagem do mapa, passando o nome enviado por parâmetro
                        image_region = self._screenshots[image_name]             
                    
                        atualizou = update_image(image_region.get('image'))
                        if atualizou:
                            self._screenshots = mapear_imagens()
                            image_region = self._screenshots[image_name]
                    else:
                        raise KeyError(e)     
                else:
                    # Executa o bloco else se a imagem for encontrada no mapa
                    coordenada = localizar_na_tela(**image_region)
                    # Efetua um break para sair do loop quando as coordenas da imagem não forem mais encontradas
                    if coordenada is None:
                        continue             
                
                if time.time() - start_time > max_wait_local:
                    if self._modo_manutencao:
                        # Abre a imagem a que não desapareceu no tempo de espera máxima
                        im = Image.open(image_region['image'])
                        im.show()
                        pyautogui.alert(title='RPAPY', text='A imagen {} não desapareceu em {:.0f} minutos! Feche-a para continuar a manutenção.'.format(image_region['image'], time.time() - start_time))
                        # Fecha janela do visualizador de imagem após confirmacao de troca
                        fechar_visualizador_fotos('fotos')
                        start_time = time.time()
                    else:
                        raise ImageNotDisappearError("A imagem não desapareceu em {} seconds".format(time.time() - start_time))

                # Efetua um intervalo parada entre os loop de tentativa de encontrar a imagem
                time.sleep(interval_local)


def fechar_visualizador_fotos(title: str):
    """Fecha a janela do visualizador de imagem do windows
    
    Arguments:
        title {str} -- Nome ou parte do nome do titulo da janela do visualizador de imagens
    """
    visualizadores_fotos = pyautogui.getWindowsWithTitle(title)
    for v in visualizadores_fotos:
        v.close()
    

def salvar_img_error(image_name:str, im:Image) ->None:
    """Salva um print da tela no momento em que ocorreu o erro com informações 
    de data e hora e nome da imagem em que foi lançado o erro.
    
    Arguments:
        image_name {str} -- nome da imagem que não foi encotrado pelo metodo de busca
        im {Image} -- imagem que capiturada no momento do erro.
    """    
    create_python_default_dirs()    
    nome_arquivo = datetime.datetime.now().strftime('%Y.%m.%d-%Hh%Mm%Ss')+'_'+image_name
    im.save(f'{path_dir_error_images}/{nome_arquivo}.png', 'PNG')


def mapear_imagens():
    """Efetua o mapeamento das imagens capituradas pelo agente.py
    e salvas no diretorio images. Utiliza o nome da imagem para 
    recuperar a região onde a imagem deverá ser procurada.
    
    Returns:
        [dict] -- [dicionário contendo os dados da imagem]
    """
    create_python_default_dirs()

    # recupera o diretório onde estão as imagens    
    try: 
        path_dir_images.mkdir()
    except FileExistsError:
        pass

    resultado: Dict[str, Dict[str, Tuple[int]]] = {}

    # Recupera todos os arquivos de imagem no formato nome+região
    images_path = path_dir_images.glob('*).png')

    # Itera por todas as imagens encontradas no diretório
    # recupera do nome e a tupla que indica a região da imagem
    # adiciona os dados em um dict litera e adiona ao dict resultado pelo método default.
    for p in images_path:
        p: Path = p     
        nome, restante = p.name.split('-')
        region_tuple = tuple(int(i) for i in restante.split('.')[0][1:-1].split(','))
        resultado.setdefault(nome, {'image': p.as_posix(), 'region': region_tuple, })
    return resultado


def max_wait_attr(desktop: Desktop, attr_name: str, max_wait: float=5.0) -> AttributeError:
    start_time = time.time()
    while True:
        if hasattr(desktop, attr_name):
            break
        elif time.time() - start_time > max_wait:
            raise AttributeError(f'O atributo "{attr_name}" não foi encontrado!')
        time.sleep(.1)


def image_optmization(im: Image) -> Image:
    """Fonte: https://blog.codeexpertslearning.com.br/lendo-imagens-uma-abordagem-%C3%A0-ocr-com-google-tesseract-e-python-ee8e8009f2ab
    Pesquisado em: 02/01/2020
    """
    from PIL import Image

    # tipando a leitura para os canais de ordem RGB
    imagem = im.convert('RGB')

    # convertendo em um array editável de numpy[x, y, CANALS]
    npimagem = np.asarray(imagem).astype(np.uint8)  

    # diminuição dos ruidos antes da binarização
    npimagem[:, :, 0] = 0 # zerando o canal R (RED)
    npimagem[:, :, 2] = 0 # zerando o canal B (BLUE)

    # atribuição em escala de cinza
    im = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY) 

    # aplicação da truncagem binária para a intensidade
    # pixels de intensidade de cor abaixo de 127 serão convertidos para 0 (PRETO)
    # pixels de intensidade de cor acima de 127 serão convertidos para 255 (BRANCO)
    # A atrubição do THRESH_OTSU incrementa uma análise inteligente dos nivels 
    # de truncagem
    ret, thresh = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) 

    # reconvertendo o retorno do threshold em um objeto do tipo PIL.Image
    binimagem = Image.fromarray(thresh) 

    # # chamada ao tesseract OCR por meio de seu wrapper
    # phrase = ocr.image_to_string(binimagem, lang='por')

    # # impressão do resultado
    # print(phrase)

    return binimagem
