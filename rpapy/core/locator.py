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

from rpapy.core.utils.messages import confirm_ok_cancel, confirm_yes_no_cancel

with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from pywinauto import Desktop

from rpapy.core.image_mapper import map_images
from rpapy.core.snipps.loads import create_python_default_dirs

from .config import Config
from .snipps import update_image
from .snipps.snippingtools import (ImageNotDisappearError, ImageNotFoundError,
                                   close_window_with_title)

MAINTENANCE_MODE = False
if Config.CHECK_MODE:
    MAINTENANCE_MODE = confirm_yes_no_cancel(title='RPAPY',text='Ativar o modo de manutenção?')

if MAINTENANCE_MODE is None: 
    pyautogui.hotkey('ctrl', 'win', 'x')
    pyautogui.sleep(2)
    exit()

if MAINTENANCE_MODE is False:
    pyautogui.FAILSAFE = False

if Config.FAILSAFE_OFF:    
    pyautogui.FAILSAFE = False

images_dir_path =  Config.IMAGES_DIR_PATH
error_images_dir_path = Config.ERROR_IMAGES_DIR_PATH


def locate_on_screen(image, *args, **kwargs):
    try:
        img = Image.open(image)
        return pyautogui.locateOnScreen(img, *args, **kwargs)
    except ValueError:
        pass


class LocatorImage():

    def __init__(self):
        self._screenshots: Dict[str, Dict[str, Tuple[int]]] = map_images()
        self.wait_before = 0.0
        self.debug = False
        self._interval = 0.2
        self._max_wait = Config.MAX_WAIT_MAINTENANCE if MAINTENANCE_MODE else 30
        self._maintenance_mode = MAINTENANCE_MODE

    def modo_manutencao(self, option: bool):
        if isinstance(option, bool):
            if option:
                self._maintenance_mode = option
                self._max_wait = 10
            else:
                self._maintenance_mode = option
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

    def __call__(self,
                 image_name: str, 
                 *, 
                 max_wait: float=None, 
                 confidence: float=None, 
                 wait_vanish=False,
                 interval: float=None, 
                 deslocar_x:int=0, 
                 deslocar_y:int=0, 
                 ignore_error: bool=False) -> Tuple[int]:
        
        """Searches the image on the screen until the maximum time defined by parameter, and returns
        the image coordinate if found, otherwise it throws the custom exception ImageNotFoundError.
        Arguments:
            image {str} -- name of the image to be retrieved from the dictionary
        Keyword Arguments:
            max_wait {float} -- maximum waiting time to find the image (default: {None})
            interval {float} -- stop interval for image search (default: {None})
            deslocar_x {int} -- shifts the center of the image location on the x-axis (default: {0})
            deslocar_y {int} -- shifts the center of the image location on the y-axis (default: {0})
        Raises:
            ImageNotFoundError: Excess thrown when the image is not found within the maximum period
        Returns:
            Tuple[int] -- tuple containing the values ​​(x, y) of the center of the identified image
        """
        # If True performs a stop at each execution. Used to reduce the speed of the bot.
        if self.debug:
            input(f'Localizar "{image_name}" - Pressione enter para continuar...')

        # Assigns to interval_local the interval passed as a parameter, other than None.
        if interval is not None:
            if interval > 0:
                interval_local = interval
            else:
                interval_local = self._interval
        else:
            interval_local = self._interval

        # Assigns to max_wait_local the maximum time passed per parameter, if different from None.
        if max_wait is not None:
            max_wait = float(max_wait)
            if max_wait > 0 and max_wait > interval_local:
                max_wait_local = max_wait
            else:
                max_wait_local = self._max_wait
        else:
            max_wait_local = self._max_wait
        
        # Pauses before trying to find the image location.
        time.sleep(self.wait_before)

        # Moves the mouse to a resting point on the screen so as not to interfere with the image search.
        pyautogui.moveTo(700,5,0)

        # Starts the coordinate with the default flag None.
        coordenada = None

        # Registers the start of method execution to be checked with max_wait.
        start_time = time.time()

        if not wait_vanish:
            # Repeat the code block as long as the coordinate variable is equal to None.
            while coordenada is None:
                try:
                    # retrieves the map image, passing the name sent as a parameter.
                    image_region = {
                        'image': self._screenshots[image_name]['image'],
                        'region': self._screenshots[image_name]['region']
                    }
                except KeyError:
                    # Create a file with image_name in the images directory if it does not exist
                    im = Image.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'utils/imagens/IMAGEM_NAO_ENCONTRADA.png'))
                    im.save(f'{images_dir_path}/{image_name}-(300, 50, 700, 200).png', 'PNG')
                    time.sleep(1)
                    # Updates the map with the image created with the image_name parameter.
                    self._screenshots = map_images()
                    continue
                
                try:
                    # Executes the else block if the image is found on the map and continues to exit the loop.
                    if confidence is None:
                        coordenada = locate_on_screen(**image_region)
                    else:
                        coordenada = locate_on_screen(**image_region, confidence=confidence)

                    if coordenada is not None:
                        continue
                except Exception:
                    coordenada = None
                    
                # Enter block if loop execution time exceeds max_wait.
                if time.time() - start_time > max_wait_local:
                    if self._maintenance_mode:
                        atualizou = update_image(image_region.get('image'))
                        if atualizou:
                            self._screenshots = map_images()
                            image_region = {
                                'image': self._screenshots[image_name]['image'],
                                'region': self._screenshots[image_name]['region']
                            }
                        start_time = time.time()
                    elif not ignore_error:
                        # Take a screenshot of the screen at the time the error occurred.
                        image_not_found_error = pyautogui.screenshot()
                        # Saves the screenshot with the name of the image that was not found, including date and time.
                        salvar_img_error(image_name, image_not_found_error)
                        # Throws the image not found exception.
                        raise ImageNotFoundError(f'A imagem "{image_name}", não foi encontrada!')

                # Take a timeout between loops trying to find the image.
                time.sleep(interval_local)
            else:
                
                # If the loop is terminated in the while conditional, this block is executed.
                # Retrieves the x,y coordinate of the center of the found image.
                resultado = pyautogui.center(coordenada)

                # Retrieves the anchor coordinates to apply the displacement
                anchor_coord = self._screenshots[image_name]['anchor_coord']
                if anchor_coord is not None and deslocar_x + deslocar_y == 0:
                    deslocar_x, deslocar_y = anchor_coord

                # Returns the result adding the displacements, if passed by parameter.
                return resultado[0] + int(deslocar_x), resultado[-1] + int(deslocar_y)
        
        else:
            # Stores the start of method execution to be checked with max_wait.
            start_time = time.time()

            # Sets a coordinate other than None to start the while loop.
            coordenada = True

            # Checks whether the image searched for on the screen has disappeared.            
            while coordenada is not None:
                try:
                    # retrieves the map image, passing the name sent as a parameter.
                    image_region = {
                        'image': self._screenshots[image_name]['image'],
                        'region': self._screenshots[image_name]['region']
                    }                
                except KeyError as e:
                    # If maintenance mode equals True, creates a provisional image and updates the newly created image on the map.
                    if self._maintenance_mode:
                        # Create a file with image_name in the images directory if it does not exist.
                        im = pyautogui.screenshot(region=(1, 1, 300, 150))
                        im.save(f'{images_dir_path}/{image_name}-(300, 50, 350, 200).png', 'PNG')
                        time.sleep(1)
                        # Updates the map with the image created with the image_name parameter.
                        self._screenshots = map_images()
                        # Retrieves the map image, passing the name sent as a parameter.
                        image_region = {
                            'image': self._screenshots[image_name]['image'],
                            'region': self._screenshots[image_name]['region']
                        }             
                    
                        atualizou = update_image(image_region.get('image'))
                        if atualizou:
                            self._screenshots = map_images()
                            image_region = {
                                'image': self._screenshots[image_name]['image'],
                                'region': self._screenshots[image_name]['region']
                            }
                    else:
                        raise KeyError(e)     
                else:
                    # Execute the else block if the image is found on the map.
                    coordenada = locate_on_screen(**image_region)
                    # Performs a break to exit the loop when the image coordinates are no longer found.
                    if coordenada is None:
                        continue             
                
                if time.time() - start_time > max_wait_local:
                    if self._maintenance_mode:
                        # Open the image that did not disappear within the maximum waiting time.
                        im = Image.open(image_region['image'])
                        im.show()
                        pyautogui.alert(title='RPAPY', text='A imagen {} não desapareceu em {:.0f} minutos! Feche-a para continuar a manutenção.'.format(image_region['image'], time.time() - start_time))
                        # Closes image viewer window after switching confirmation.
                        close_image_viewer('fotos')
                        start_time = time.time()
                    else:
                        raise ImageNotDisappearError("A imagem não desapareceu em {} seconds".format(time.time() - start_time))

                # Performs a pause between loops trying to find the image
                time.sleep(interval_local)


def close_image_viewer(title: str):
    """Closes the Windows Image Viewer window
    
    Arguments:
        title {str} -- Name or part of the name of the title of the image viewer window.
    """
    image_viewer = pyautogui.getWindowsWithTitle(title)
    for v in image_viewer:
        v.close()
    

def salvar_img_error(image_name:str, im:Image) ->None:
    """Saves a screenshot of the moment the error occurred with information
    date and time and name of the image where the error was thrown.
    
    Arguments:
        image_name {str} -- name of the image that was not found by the search method.
        im {Image} -- image that was captured at the time of the error.
    """    
    create_python_default_dirs()    
    nome_arquivo = datetime.datetime.now().strftime('%Y.%m.%d-%Hh%Mm%Ss')+'_'+image_name
    im.save(f'{error_images_dir_path}/{nome_arquivo}.png', 'PNG')


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

    # Typing the reading for RGB order channels.
    imagem = im.convert('RGB')

    # Converting to an editable array of numpy[x, y, CANALS]
    npimagem = np.asarray(imagem).astype(np.uint8)  

    # Noise reduction before binarization.
    npimagem[:, :, 0] = 0       # canal R (RED).
    npimagem[:, :, 2] = 0       # canal B (BLUE).

    # Grayscale Attribution
    im = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY) 

    # Application of binary truncation for intensity
    # Color intensity pixels below 127 will be converted to 0 (BLACK).
    # Color intensity pixels above 127 will be converted to 255 (WHITE).
    # The THRESH_OTSU attribute increases intelligent level analysis truncation.
    ret, thresh = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) 

    # Reconverting the threshold return into an object of type PIL.Image
    binimagem = Image.fromarray(thresh) 

    # Call to tesseract OCR through its wrapper
    # phrase = ocr.image_to_string(binimagem, lang='por')

    # printout of result
    # print(phrase)

    return binimagem

if '__main__' == __name__:
    map_images()