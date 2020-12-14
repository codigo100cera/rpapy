"""Setup script for rpapy"""

import os.path
import rpapy
from setuptools import setup, find_packages

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="rpapy",
    version="1.0.1",
    description="RPAPY is a open source easy tool for automating boring stuffs on any screen with robotframework, pyautogui, pywinauto and others.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/codigo100cera",
    author="Codigo Sem Cera",
    author_email="codigo100cera@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    packages=find_packages(exclude=["resources", "log", "tasks", "tests"]),
    include_package_data=True,
    install_requires=[
        "pywinauto", "pyautogui", "pyperclip", "pynput", "PySide2",
        "win10toast", "python-dotenv", "PySimpleGUI", "pillow", "opencv-python",
        "numpy==1.19.3", "mss", "pytesseract", "mouse", "robotframework"
    ],
    entry_points={"console_scripts": ["rpapy=rpapy.__main__:main"]},
)
