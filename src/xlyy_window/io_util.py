import sys
import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QWidget
from PyQt5.QtCore import QRect

from str_util import String


def get_last_dir(count:int) -> str:
    if is_executable():
        current_path = os.path.dirname(sys.executable)
        print("current_path: ", current_path)
        return current_path
    else:
        # 获取当前脚本文件的路径
        current_path = os.path.abspath(__file__)
        # 逐级向上获取父目录路径
        for _ in range(count):
            current_path = os.path.dirname(current_path)
        return current_path

#当前文件是否是exe文件
def is_executable() -> bool:
    executable_path = sys.executable
    s = String(executable_path)
    return not s.end_with('python.exe')

def is_dir_exists(path: str) -> bool:
    return os.path.isdir(path)

def is_file_exists(path: str) -> bool:
    return os.path.isfile(path)

def get_center_screenGeometry(window:QWidget | QMainWindow,/, width:int = None, height:int = None) ->QtCore.QRect | None:
    screen = QDesktopWidget().screenGeometry()
    if window and not width and not height:
        rec: QRect = window.geometry()
        m_width = (screen.width() - rec.width()) / 2
        m_height = (screen.height() - rec.height()) / 2
        return QRect(int(m_width), int(m_height),rec.width(),rec.height())
    elif window and width and height:
        m_width = (screen.width() - width) / 2
        m_height = (screen.height() - height) / 2
        return QRect(int(m_width), int(m_height),width,height)

