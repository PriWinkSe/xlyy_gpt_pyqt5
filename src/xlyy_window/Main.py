import os
import sys
from PyQt5.QtWidgets import QApplication, QStyle
from gpt_mainWindow import xlyy_GPT
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


#基本目录
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = xlyy_GPT()
    #w = test_Browser()
    sys.exit(app.exec_())