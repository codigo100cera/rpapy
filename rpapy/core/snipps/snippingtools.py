
import contextlib
from pathlib import Path
import time
from typing import List, Tuple

import cv2
import numpy as np
import PySimpleGUI as sg
from PIL.Image import Image
import pyautogui
from rpapy.core.utils.messages import confirm_ok_cancel, message_to_set_timeout

coordinates = None
anchor = None

class ScreenshotAreaError(Exception):
    pass


class ImageNotFoundError(Exception):
    """[summary]
    Arguments:
    |ValueError: Exception {[type]} -- [description]
    """


class ImageNotDisappearError(Exception):
    """[summary]
    Arguments:
        Exception {[type]} -- [description]
    """    


def get_images_path(img_name, dir_name_imgs):
    return list(Path(dir_name_imgs).glob(f'{img_name}-*.png'))


def remove_duplicate_images(img_name, dir_name_imgs):
    images_file_found_path: Path = get_images_path(img_name, dir_name_imgs)
    if len(images_file_found_path) > 0:
        msg = f'Foram encontrados {len(images_file_found_path)} imagem(s) com o nome "{img_name}", deseja substituir todos?'        
        if confirm_ok_cancel(msg):                
            for path_img in images_file_found_path:
                with contextlib.suppress(FileExistsError):
                    path_img.unlink()
            return True
    return False


def get_screenshot_region(left: int, top: int, right: int, bottom: int) -> Tuple[int]:
    screenshot_area = left, top, right - left, bottom - top
    if min(screenshot_area) < 0:
        raise ScreenshotAreaError('Um ou mais valores informados para a area do screenshot são negativos')
    return screenshot_area


def record_image(msg: str, choices: List[str]=None):
    
    sg.ChangeLookAndFeel("SystemDefault")

    # Prompt to instruct the user
    text = sg.Text(msg, background_color="#2196F3", text_color="white")

    choices = choices or ['IMG', 'IMG_ANCHOR', 'IMG_OCR', 'OCR', 'CANCEL']

    buttons = [
        sg.Button(choice, button_color=("white", "#0069C0")) for choice in choices
    ]

    layout = [[text], buttons]

    window2 = sg.Window(
        "",
        layout,
        # icon="icon.ico",
        no_titlebar=True,
        background_color="#2196F3",
        element_justification="center",
        use_default_focus=False,
        keep_on_top=True
    )

    choice, _ = window2.Read()  # Read button click from window
    window2.Close()
    del(window2)

    if choice == 'CANCEL':
        return choice, None
    elif 'IMG' not in choice:
        return 'OCR', None  

    msg = 'Clique em TIMEOUT e selecione o objeto, se deseja gravar mudanças de aspecto da imagem a ser salva.'
    message_to_set_timeout(msg)

    screenshot = capture_screen()

    target = anchor = None
    if 'ANCHOR' in choice:
        # Present the user with a selection window
        target, anchor_coord = select_rectangle_on_screen(screenshot, is_anchor=True)
    else:            
        # Present the user with a selection window
        target, anchor_coord = select_rectangle_on_screen(screenshot)
        
    im_crop = screenshot.crop(target)
    return im_crop, anchor_coord


def record_region(msg_timeout: str=None):

    sg.ChangeLookAndFeel("SystemDefault")

    message = 'Click em OK e selecione a região da tela onde deverá ser procurada a imagem ou aplicado o OCR.'
    
    text = sg.Text(message, background_color="#2196F3", text_color="white")

    choices = ['OK', 'CANCEL']

    buttons = [
        sg.Button(choice, button_color=("white", "#0069C0")) for choice in choices
    ]

    layout = [[text], buttons]

    window3 = sg.Window(
        "Select Anchor",
        layout,
        # icon="icon.ico",
        no_titlebar=True,
        background_color="#2196F3",
        element_justification="center",
        use_default_focus=False,
        keep_on_top=True
    )

    choice, _ = window3.Read()
    window3.Close()
    del(window3)

    region = None
    if choice == 'OK':
        if msg_timeout:
            message_to_set_timeout(msg_timeout)
        screenshot = capture_screen()
        retangle_on_screen, anchor_coord = select_rectangle_on_screen(screenshot)

        if retangle_on_screen is None:
            return
        
        region = get_screenshot_region(*retangle_on_screen)

    return region


def capture_screen():
    """
    Captures the screen to a Pillow Image object
    """
    import mss
    from PIL import Image

    monitor = None

    with mss.mss() as sct:

        # Find primary monitor
        for monitor in sct.monitors:
            if monitor["left"] == 0 and monitor["top"] == 0:
                break

        sct_img = sct.grab(monitor)

    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

    return img


def select_rectangle_on_screen(screenshot, info='', is_anchor=False):
    """
    Presents the user with a window which allows him/her to select
    a rectangle on the screen and returns the coordinates in the carthesian
    coordinate system
    """
    global coordinates
    global anchor

    try:
        if is_anchor:
            SnippingTool(screenshot, info=info, is_anchor=is_anchor)
        else:
            SnippingTool(screenshot, info=info)
    except KeyboardInterrupt:
        return

    return coordinates, anchor

class SnippingTool():
    def __init__(self, image, info='', is_anchor=False):
        """
        Starts a full screen snipping tool for selecting coordinates
        """
        import tkinter as tk
        from tkinter.font import Font

        from PIL import ImageTk

        self.root = tk.Tk()
        self.is_anchor = is_anchor

        self.root.bind("<Escape>", self._quit)

        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()

        # Change window to size of full screen
        self.root.geometry("{}x{}".format(w, h))

        # Bring window to full screen and top most level
        self.root.attributes('-fullscreen', True)
        self.root.attributes("-topmost", True)

        # Keep reference of some things
        self.x = self.y = 0
        self.rect = None
        self.line = None
        self.start_x = None
        self.start_y = None
        self.deloc_x = None
        self.deloc_y = None

        # Create the canvas
        self.canvas = tk.Canvas(
            self.root,
            width=w,
            height=h,
            cursor="crosshair")

        self.canvas.pack()

        # Add the screenshot
        img = ImageTk.PhotoImage(image, master=self.root)

        self.canvas.create_image(
            (0, 0), image=img, anchor="nw")

        # Connect the event handlers
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        if info:
            font = Font(family='Helvetica', size=30)

            self.canvas.create_text(
                int(w/2), int(h*2/3), text=info, fill='#1B97F3', font=font
            )

        self.root.mainloop()

    def _quit(self, event=None):
        self.root.destroy()

    def on_button_press(self, event):
        # Update coordinates
        self.start_x = event.x
        self.start_y = event.y

        # If no rectangle is drawn yet, draw one
        if not self.rect:
            self.rect = self.canvas.create_rectangle(
                self.x, self.y, 1, 1, outline="#ff0000",
                fill="#1B97F3", stipple="gray12")

    def on_move_press(self, event):        
        # Update coordinates
        self.end_x, self.end_y = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x,
                           self.start_y, self.end_x, self.end_y)
    
    def on_move_anchor(self, event):
        # Update coordinates
        self.click_x, self.click_y = event.x, event.y        
        
        # Desenhe uma linha reta do centro até a posição atual do mouse
        self.canvas.coords(self.line, self.centro_x, self.centro_y, self.click_x, self.click_y)

        
    def on_button_press_anchor(self, event):
        # Calcule a distância até o centro do retângulo
        # Calcule a posição relativa ao centro do retângulo
        self.deloc_x = self.click_x - self.centro_x
        self.deloc_y = self.click_y - self.centro_y

    def on_button_release_anchor(self, event):
        # Update global variable
        global anchor

        if hasattr(self, 'deloc_x'):
            anchor = (self.deloc_x, self.deloc_y) 

            # Close the window
            self.root.quit()
            self.root.destroy()
    
    def on_button_release(self, event):
        # Update global variable
        global coordinates

        if hasattr(self, 'end_x'):
            coordinates = (
                min(self.start_x, self.end_x),
                min(self.start_y, self.end_y),
                max(self.start_x, self.end_x),
                max(self.start_y, self.end_y)
            )

            if self.is_anchor:

                # Calcular o centro do retângulo
                self.centro_x = (self.start_x + self.end_x) // 2
                self.centro_y = (self.start_y + self.end_y) // 2

                # Disconnect the event handlers
                self.canvas.unbind_all(["<ButtonPress-1>", "<B1-Motion>", "<ButtonRelease-1>"])

                # Connect the new event handlers to anchor coord
                self.canvas.bind("<ButtonPress-1>", self.on_button_press_anchor)
                self.canvas.bind("<Motion>", self.on_move_anchor)
                self.canvas.bind("<ButtonRelease-1>", self.on_button_release_anchor)
                
                if not self.line:
                    # Update coordinates
                    start_x = event.x
                    start_y = event.y
                    # Criar uma linha de feedback (inicialmente invisível)
                    self.line = self.canvas.create_line(self.line, self.centro_x, 
                                                        self.centro_y,  start_x, start_y, 
                                                        fill='red', width=2)

            else:
                # Close the window
                self.root.quit()
                self.root.destroy()



def show_image_crop(im_crop: Image, timeout:int=0) -> cv2:
    img = cv2.cvtColor(np.array(im_crop), cv2.COLOR_BGR2RGB)
    cv2.imshow('Captured Image', img)
    if timeout:
        cv2.waitKey(timeout)
        cv2.destroyAllWindows()
    else:
        return cv2


def close_window_with_title(title: str):
    """Fecha a janela do visualizador de imagem do windows
    
    Arguments:
        title {str} -- Nome ou parte do nome do titulo da janela do visualizador de imagens
    """
    visualizadores_fotos = pyautogui.getWindowsWithTitle(title)
    time.sleep(.5)
    for v in visualizadores_fotos:
        v.close()
