"""Normaliza o texto para execucao de teclas especiais no pyautogui no mesmo padrão do pywinauto
"""

def prepare_text_for_pyautogui(text):
    result = []
    keys_press = ''
    flag_key = False
    for l in text:

        if l in '{[':
            flag_key = True
            continue          

        if l in '}]':
            keys_qtde = keys_press.split()
            try:
                if len(keys_qtde) == 2:
                    result += [keys_qtde[0].lower()] * int(keys_qtde[1])
                else:
                    result += [keys_qtde[0].lower()]
            except:
                raise Exception('As teclas especiais')
            keys_press = ''
            flag_key = False
            continue

        if flag_key is True:
            keys_press += l
            
        if flag_key is False:
            result.append(l)
    
    return result


if __name__ == "__main__":
    print(prepare_text_for_pyautogui(r'{ESC 5}ocorrência{TAB 3}trabalhador{ENTER 2}'))
