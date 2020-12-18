![](https://i.imgur.com/ClOul8Y.png)

# RPAPY - Open Source Tool for Robotic Process Automatition
[Medium](https://medium.com/@codigo100cera) | [Linkedin](https://www.linkedin.com/in/mcsilva-csc/) | [Youtube](https://www.youtube.com/channel/UCbrw7-reRWpQD1JBubCl4QQ?view_as=subscriber) | [Telegram](https://t.me/joinchat/C_ECNVWoSae_ebzcjfM33w)

__RPAPY__ is a open source easy tool for automating boring stuffs on any screen with robotframework, pyautogui, pywinauto and others.

_"Creating __automations__ for __GUI__ has never been more __fun__ than now."_


![RPAPY Example](https://i.imgur.com/9TaGCby.gif)

## Get started

### Windows

The easiest way to install RPAPY is by using __pip install__

- Download and install [Python 3.7](https://www.python.org)

- Install the latest version RPAPY on your machine:
```
pip install rpapy
```

However, it is advisable to use a virtual environment for an isolated installation of all requirements, this avoids conflicts with the python interpreter installed on the host machine:
```
pip install virtualenv
mkdir <your-project-name>
cd <your-project-name>
virtualenv  <your-venv-name>
activate <your-venv-name>
pip install rpapy
```

After installed, the construction of the project structure is accomplished by executing the following command in the terminal:
```
rpapy
```

The hotkeys menu to be used will be displayed after executing the above command.

```
***TURN ON AGENTPY***
        ****************HOTKEYS MENU****************
        <CTRL>+<ALT>+P: Capture image or ocr
        <CTRL>+<ALT>+R: Change file name
        <CTRL>+<ALT>+B: Switch between backends
        <CTRL>+I:       Inspect UI element
        <CTRL>+<CMD>+C: View current configuration
        <CTRL>+<CMD>+E: Load sample implementation
        <CTRL>+<CMD>+X: Turn off agent
        ********************************************
```

To run the sample implementation, perform the following steps:

- Activate the hotkey ```<CTRL>+<CMD>+E```.

- In the messagebox enter ```your-file-name.robot``` or keep the default name ```main.robot```.

- Configure the ```.env``` file in the root directory of the project.

```
###VARIAVEIS DE AMBIENTE PYTHON-DOTENV

#RESOURCES_DIR_NAME=resources
#RESOURCES_KEYWORDS_FILE_NAME=keywords.robot
#IMAGES_DIR_NAME=images
#IMAGES_ERROR_DIR_NAME=images_error
#TASKS_DIR_NAME=tasks
MAX_WAIT_MANUTENCAO=5
VERIFICAR_MODO=True
#ARQUIVO_TEMPORARIO_ATIVO=False
#NOME_ARQUIVO_TEMPORARIO=temp.txt
```

- Run the following command on the terminal:

```
robot -d log tasks
```

- In the dialog box, which will be displayed, choose the option YES and make changes to the images as required by RPAPY.

- After the update cycle of the UI images in which the actions will be performed by the robot, interrupt the execution.

- Repet the command on the terminal:

```
robot -d log tasks
```

- select the option no in the dialog box to choose the maintenance mode off.

## Credits

Under the hood, RPAPY is built on some of the greatest open source libraries. Within RPAPY, the following libraries are currently included:

- [Keyring](https://pypi.org/project/keyring/)
- [Mouse](https://github.com/boppreh/mouse)
- [Numpy](https://pypi.org/project/numpy/)
- [OpencvPython](https://pypi.org/project/opencv-python/)
- [Pillow](https://pillow.readthedocs.io/en/stable/)
- [PyAutoGUI](https://github.com/asweigart/pyautogui)
- [Pynput](https://pypi.org/project/pynput/)
- [Pyperclip](https://pypi.org/project/pyperclip/)
- [PySide2](https://pypi.org/project/PySide2/)
- [PySimpleGUI](https://pypi.org/project/PySimpleGUI/)
- [Pytesseract](https://pypi.org/project/pytesseract/)
- [PythonDotenv](https://pypi.org/project/python-dotenv/)
- [Pwinauto](https://pypi.org/project/pywinauto/)
- [RobotFramework](https://pypi.org/project/robotframework/)
- [Win10toast](https://pypi.org/project/win10toast/)

