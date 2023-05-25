import sys
import os
import threading

from PyQt5 import QtCore
from PyQt5.QtCore import QRect, QDir, QStringListModel, QSize, QPoint, QModelIndex, QTimer, QDateTime, QEventLoop, \
    QThread
from PyQt5.QtGui import QIcon, QFont, QPalette, QPixmap, QIntValidator, QDoubleValidator, QRegExpValidator, QImage, \
    QPainter, QColor, QFont, QFontMetrics, QPen, QStandardItemModel, QStandardItem,QBrush
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QPushButton, QHBoxLayout, QWidget, QToolTip, \
    QLabel, QLineEdit, QGridLayout, QFormLayout, QTextEdit, QVBoxLayout, QDialog, QRadioButton, QCheckBox, \
    QComboBox,QSlider, QSpinBox, QMessageBox, QInputDialog, QFontDialog, QFileDialog, QTableView, QListView, \
    QTableWidget,QTableWidgetItem,QAbstractItemView,QListWidget,QListWidgetItem,QMenu,QTreeWidget,QTreeWidgetItem,\
    QDirModel,QTreeView,QHeaderView,QTabWidget,QStackedWidget,QDockWidget,QMdiArea,QAction,QMdiSubWindow,QScrollBar
from PyQt5.QtCore import QObject,QRect,Qt,QRegExp


class _QT_util:
    def __init__(self):
        ...
    def do_afterSecond(self,method, mill_seconds: int):
        timer = QTimer()
        timer.start(mill_seconds)
        def timeoutEvent():
            timer.stop()
            method()
        timer.timeout.connect(timeoutEvent)

    def do_repeat_periodTime(self,method, mill_seconds: int, /, *args) -> QTimer | None:
        timer = QTimer()
        def repeat_operation():
            r: str = method(*args)
            if r and r == 'stop':
                timer.stop()
                return None
            timer.start(mill_seconds)
        timer.timeout.connect(repeat_operation)
        timer.start(mill_seconds)
        return timer

def qt_sleep(mill_seconds: int):
    # 创建一个临时的QEventLoop对象
    loop = QEventLoop()
    # 创建一个定时器
    timer = QTimer()
    timer.timeout.connect(loop.quit)
    # 启动定时器，设置间隔为指定的毫秒数
    timer.start(mill_seconds)
    # 进入事件循环，等待定时器超时
    loop.exec_()


def spe_remainContainsData(wid: QComboBox | QListView, reserv_data: str):
    if wid is None:
        return
    elif isinstance(wid, QComboBox):
        for index in range(wid.count() - 1, -1, -1):
            item_text = wid.itemText(index)
            if reserv_data not in item_text:
                wid.removeItem(index)
    elif isinstance(wid, QListView):
        model: QStringListModel = wid.model()
        if model is None:
            return
        row_count = model.rowCount()
        for row in range(row_count - 1, -1, -1):
            item_text = model.stringList()[row]
            if reserv_data not in item_text:
                model.removeRow(row)

def spe_remainData(wid: QComboBox | QListView, reserv_data: str):
    if wid is None or reserv_data is None or reserv_data.strip() == '':
        return
    elif isinstance(wid, QComboBox):
        for index in range(wid.count() - 1, -1, -1):
            item_text = wid.itemText(index)
            if item_text != reserv_data:
                wid.removeItem(index)
    elif isinstance(wid, QListView):
        model: QStringListModel = wid.model()
        if model is None:
            return
        row_count = model.rowCount()
        for row in range(row_count - 1, -1, -1):
            item_text = model.stringList()[row]
            if item_text != reserv_data:
                model.removeRow(row)

def spe_getStringList(wid: QComboBox | QListView) -> list[str, ...]:
    if wid is None:
        return list()
    if isinstance(wid, QComboBox):
        l = list()
        for index in range(wid.count()):
            item_text = wid.itemText(index)
            l.append(item_text)
        return l
    elif isinstance(wid,QListView):
        m: QStringListModel = wid.model()
        if not m:
            return list()
        return m.stringList()
#不重复的添加数据
def spe_addString(wid: QComboBox | QListView, arg: str):
    if wid is None:
        return
    elif isinstance(wid, QComboBox):
        if arg not in [wid.itemText(index) for index in range(wid.count())]:
            wid.addItem(arg)
    elif isinstance(wid, QListView):
        model: QStringListModel = wid.model()
        if model is None:
            model = QStringListModel()
            wid.setModel(model)
        if arg not in model.stringList():
            model.insertRow(model.rowCount())
            model.setData(model.index(model.rowCount() - 1), arg)
def spe_containsString(wid: QComboBox | QListView, arg: str) -> bool:
    if arg in spe_getStringList(wid):
        return True
    else:
        return False
def spe_removeString(wid: QComboBox | QListView, arg: str):
    if wid is None or arg is None:
        return
    if isinstance(wid, QComboBox):
        index = wid.findText(arg)
        if index != -1:
            wid.removeItem(index)
    elif isinstance(wid, QListView):
        string_list = spe_getStringList(wid)
        if arg in string_list:
            string_list.remove(arg)
            model: QStringListModel = wid.model()
            if model is not None:
                model.setStringList(string_list)
def spe_resetStringList(wid: QComboBox | QListView):
    if wid is None:
        return
    if isinstance(wid, QComboBox):
        wid.clear()
    elif isinstance(wid, QListView):
        model: QStringListModel = wid.model()
        if model is not None:
            model.setStringList([])

def spe_setStringList(wid: QComboBox | QListView, strlist: list[str, ...]):
    if wid is None:
        return
    elif isinstance(wid, QComboBox):
        wid.clear()
        wid.addItems(strlist)
    elif isinstance(wid, QListView):
        model = QStringListModel(strlist)
        wid.setModel(model)


class xm_QThread(threading.Thread):
    def __init__(self, method,repeat_delay:int |None = None, *args):
        super(xm_QThread,self).__init__()
        self.method = method
        self.repeat_delay = repeat_delay
        self.args = args
        self.daemon = True
        #print(f"method = {method} RepeatDelay: {repeat_delay} args{args}")


    def run(self):
        if self.repeat_delay is None:
            self.method(*self.args)
        else:
            while True:
                r = self.method(*self.args)
                if r == 'stop':
                    return
                qt_sleep(self.repeat_delay)