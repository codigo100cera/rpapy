"""[summary]
"""

import time
import typing
from pathlib import Path

import pyautogui
import pytesseract as ocr
from pywinauto import Desktop
from pywinauto.backend import BackendsRegistry
from win10toast import ToastNotifier

from rpapy.core.activities import (click_coord, click_vision,
                                   double_click_coord, double_click_vision,
                                   get_element_vision, get_text_ocr_region,
                                   get_text_ocr_vision, open_executable,
                                   triple_click_coord, triple_click_vision,
                                   wait_element_vision, write_text_vision)
from rpapy.core.localizador import (ImageNotFoundError, LocalizadorImagem,
                                    image_optmization, max_wait_attr)
from rpapy.core.screenshots import get_screenshot_region

#######################DEFINE#######################
get_coordenadas = LocalizadorImagem()
LIMPAR_CAMPOS = '{HOME}{DEL 30}'
#######################DEFINE#######################

toaster = ToastNotifier()
toaster.show_toast('Robo.py iniciando processo', duration=5, threaded=True)
print('Robo.py iniciando processo...')


def desenhar():
    # [Contexto - Janela]: 
    # [Descricao]: 
    exec = open_executable('mspaint.exe', 'Sem título', work_dir='C:/Windows/System32', maximized=True)

    # [Contexto - Janela]: 
    # [Descricao]:
    wait_element_vision('verificar_icone_paint') 

    # Contexto - Janela: 
    # Descricao: 
    click_vision('btn_lapis', identifier_img=get_coordenadas, backend='uia')

    # Contexto - Janela: 
    # Descricao:
    click_vision('btn_reduzir_zoom', identifier_img=get_coordenadas, backend='uia', after=.5)
    
    definir_tamanho_imagem(6000, 3000)


def definir_tamanho_imagem(largura, altura):
    # Contexto - Janela: 
    # Descricao: 
    click_vision('btn_menu_arquivo', identifier_img=get_coordenadas, backend='uia')

    # Contexto - Janela: 
    # Descricao: 
    click_vision('btn_item_menu_propriedades', identifier_img=get_coordenadas, backend='uia')

    # Contexto - Janela: 
    # Descricao: 
    campo_largura_imagem = LIMPAR_CAMPOS + str(largura)
    write_text_vision('campo_largura_imagem',text=campo_largura_imagem, identifier_img=get_coordenadas, backend='uia', move_x=40)

    # Contexto - Janela: 
    # Descricao: 
    campo_altura_imagem = LIMPAR_CAMPOS + str(altura)
    write_text_vision('campo_altura_imagem',text=campo_altura_imagem, identifier_img=get_coordenadas, backend='uia', move_x=40)

    # Contexto - Janela: 
    # Descricao: 
    click_vision('btn_ok_propriedades_imagem', identifier_img=get_coordenadas, backend='uia', after=.5)


if __name__ == "__main__":
    desenhar()

    # Contexto - Janela: 
    # Descricao:
    click_vision('btn_editar_cores', identifier_img=get_coordenadas)

    # Contexto - Janela: 
    # Descricao: 
    click_vision('btn_ok_editar_cores', identifier_img=get_coordenadas, backend='uia')
    
    # [Contexto - Janela]: 
    # [Descricao]: 
    label_btn_tamanho = get_text_ocr_vision('label_btn_tamanho', backend=ocr, region=(716, 88, 771, 103), lang='por', identifier_img=get_coordenadas, 
                        max_wait=30, wait_vanish=False, ignore_error=False)

    
    print('>>>>>>>>>>>>>>>>>', label_btn_tamanho)
    
    # [Contexto - Janela]: 
    # [Descricao]: 
    im_label_cores = pyautogui.screenshot(region=get_screenshot_region(934, 121, 972, 137))
    str_label_cores = ocr.image_to_string(im_label_cores, lang='por')
    print('>>>>str_ocr>>>>', str_label_cores)
    # im_label_cores.show()
    
    # [Contexto - Janela]: 
    # [Descricao]: lb_icone_sefip
    lb_icone_sefip = get_text_ocr_region(region=(850, 765, 891, 783), lang='por')
    
    # [Contexto - Janela]: 
    # [Descricao]: 
    im_lb_icone_sefip = pyautogui.screenshot(region=get_screenshot_region(856, 764, 892, 782))
    str_lb_icone_sefip = ocr.image_to_string(im_lb_icone_sefip, lang='por')
    print('>>>>str_ocr>>>>', str_lb_icone_sefip)
    
    # im_lb_icone_sefip.show()
    # [Contexto - Janela]:
    # [Descricao]: lb_icone_sefip
    lb_icone_sefip = get_text_ocr_region(region=(844, 765, 894, 778), lang='eng')
    

    # [Contexto - Janela]: 
    # [Descricao]: 
    wait_element_vision('teste', identifier_img=get_coordenadas, backend=None,
                        max_wait=30, wait_vanish=False, ignore_error=False)
    