import os
from pathlib import Path

import mouse
import pyautogui


def desenhar(nome_imagem: str):
        
    # The directory containing this file
    HERE = os.path.abspath(os.path.dirname(__file__))

    # The text of the README file
    with open(os.path.join(HERE, F"desenhos/{nome_imagem}.txt")) as fid:
        DESENHO = fid.read()


    flag_levantado = True
    for line in DESENHO.splitlines():
        
        partes_line = line.split()
        if len(partes_line) < 2:
            continue        

        if 'Z5' in partes_line[1]:
            flag_levantado = True
        
        elif 'Z-' in partes_line[1]:
            flag_levantado = False
        
        if 'X' in partes_line[1]:
            x, y = [int(float(coord.replace('X', '').replace('Y', ''))) for coord in partes_line[1:3]]
            
            if flag_levantado:
                pyautogui.moveTo(x+100, y+100, .2)
                
            else:
                start_x, start_y = mouse.get_position()
                mouse.drag(start_x, start_y, x+100, y+100, absolute=True, duration=float(1*10**-250))

def get_dados_cores(nome_imagem: str):        
    return {
        'robotframework':{
            'preenchimento': {
                'param_cor': (0, 0, 0),
                'coordenadas': [(331, 309),(341, 213),(540, 229),(616, 248),(683, 233),(690, 266),
                                (766, 249),(608, 332),(687, 358),(615, 450),(687, 427),(538, 523),
                                (613, 528),(687, 550),(764, 529)]
            },
            'iniciais_azul': {
                'param_cor': (0, 192, 182, 118, 240, 90),
                'coordenadas': [(538, 244),(519, 344),(538, 471)]
            },
            'amarelo': {
                'param_cor': (255, 201, 14, 31, 240, 127),
                'coordenadas': [(537, 537),(596, 547),(686, 519),(743, 544),(832, 540)]
            },
            'vermelho': {
                'param_cor': (255, 0, 0, 0, 240, 120),
                'coordenadas': [(930, 384),(1082, 308)]
            }
        },
        'borboleta':{
            'contorno': {
                'param_cor': (0, 0, 0),                         # Cor preto
                'coordenadas': [(419, 459)]
            },
            'asas': {
                'param_cor': (255, 0, 128, 220, 240, 120),      # Cor rosa
                'coordenadas': [(203, 247),(242, 233),(303, 252),(224, 277),(273, 280),(326, 277),(358, 297),
                                (350, 309),(302, 316),(228, 319),(336, 321),(351, 345),(395, 345),(442, 387),(246, 348),(233, 376),
                                (251, 400),(282, 359),(309, 347),(299, 382),(326, 376),(283, 402),(360, 385),(396, 409),(428, 429),
                                (394, 430),(328, 430),(333, 439),(411, 450),(272, 442),(252, 457),(259, 484),(291, 475),(337, 449),
                                (304, 489),(432, 464),(265, 507),(262, 528),(285, 520),(311, 526),(359, 491),(359, 522),(380, 538),
                                (420, 496),(252, 546),(297, 552),(318, 555),(348, 563)] + [(666, 232),(714, 249),(609, 248),
                                (550, 299),(582, 274),(633, 283),(673, 276),(626, 309),(559, 306),(574, 316),(675, 322),(521, 336),
                                (475, 386),(559, 347),(587, 354),(651, 353),(631, 360),(542, 388),(583, 372),(610, 377),(678, 372),
                                (637, 395),(660, 397),(528, 413),(481, 424),(513, 434),(578, 431),(499, 450),(581, 438),(627, 441),
                                (574, 449),(607, 469),(650, 453),(657, 456),(656, 483),(647, 500),(617, 490),(475, 461),(489, 488),
                                (518, 514),(546, 514),(557, 502),(589, 521),(623, 514),(646, 525),(557, 563),(592, 557),(618, 558),(642, 551)]
            },
            'corpo': {
                'param_cor': (251, 251, 0, 40, 240, 118),       # Cor amarelo
                'coordenadas': [(455, 371),(458, 414),(456, 464)]
            }
        }
    }.get(nome_imagem)