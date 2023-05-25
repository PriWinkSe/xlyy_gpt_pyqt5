import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QMouseEvent, QFont, QPainter, QPainterPath, QCursor
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QToolBar, QPushButton, QLineEdit, \
     QSizePolicy, QAction
from abstract_window import AbstractWindow
from src.common_utils.io_util import get_last_dir
from src.xlyy_window.xlyyEngineView import PrivateEngineView


class xlyy_GPT(QMainWindow, AbstractWindow):
    def InitWindow(self):
        self.setupWindowBasicAttributes()
        self.setupWidgets()
        self.regEvents()
        self.setWidgetFlags()

    def setupWindowBasicAttributes(self):
        self.windowlogo = QIcon(get_last_dir(3) + '\images\logo.ico')
        self.setWindowTitle("Qt5_GPT")
        self.setWindowIcon(self.windowlogo)
        self.setGeometry(100, 100, 1200, 800)

    def setupWidgets(self):
        self.toolbar = QToolBar()
        # 设置工具栏样式

        actionStyle = '''
                    QToolBar {
                        border: 0;
                        background-color: deepskyblue;
                        background-clip: padding-box;
                    }
                    
                    QToolBar > * {
                        background-color: deepskyblue;
                        background-clip: padding-box;
                    }
                    
                   QToolButton {
                        font-family: monospace;
                        text-align: center;
                        font-size: 0.9em;
                        color: #fff;
                        background: deepskyblue;
                        outline: none;
                        border: none;
                        cursor: pointer;
                        padding: 10px 20px;
                        -webkit-appearance: none;
                   }
                   
                   QToolButton:disabled {
                        background-color: #CCCCCC;
                        font-family: monospace;
                        text-align: center;
                        font-size: 0.9em;
                        color: #fff;
                        outline: none;
                        border: none;
                        cursor: pointer;
                        padding: 10px 20px;
                        -webkit-appearance: none;
                    }

                   QToolButton:hover {
                        background: dodgerblue;
                        color: #ffffff;
                        transition: 0.5s all ease;
                        -webkit-transition: 0.5s all ease;
                        -moz-transition: 0.5s all ease;
                        -o-transition: 0.5s all ease;
                        -ms-transition: 0.5s all ease;
                   }         
               '''
        self.toolbar.setMovable(False)
        self.toolbar.setCursor(QCursor(Qt.ArrowCursor))
        self.toolbar.setStyleSheet(actionStyle)
        self.toolbar.setContextMenuPolicy(Qt.CustomContextMenu)
        self.toolbar.mouseDoubleClickEvent = self.toggleMaximizeWindow
        self.toolbar.setMaximumHeight(38)
        self.addToolBar(self.toolbar)
        #font = QFont('微软雅黑',8)
        self.back_action = QAction("后退", self)
        self.back_action.setEnabled(False)
        #self.back_action.setFont(font)
        self.toolbar.addAction(self.back_action)

        self.forward_action = QAction("前进", self)
        self.forward_action.setEnabled(False)
        #self.forward_action.setFont(font)
        self.toolbar.addAction(self.forward_action)

        self.refresh_action = QAction("刷新", self)
        #self.refresh_action.setFont(font)

        self.toolbar.addAction(self.refresh_action)

        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar.addWidget(spacer)

        min_action = QAction('-',self)
        min_action.triggered.connect(self.on_minimizeaction_clicked)
        self.toolbar.addAction(min_action)

        max_action = QAction('🗗', self)
        max_action.triggered.connect(self.on_maximizelabel_clicked)
        self.toolbar.addAction(max_action)

        # 添加关闭按钮
        close_action = QAction('🗙', self)
        close_action.triggered.connect(self.on_closeeaction_clicked)
        self.toolbar.addAction(close_action)

        #安装浏览器窗口
        self.container = QWidget()
        self.layout = QVBoxLayout()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        self.web_view = PrivateEngineView()
        self.layout.addWidget(self.web_view)

    def on_minimizeaction_clicked(self, event:QMouseEvent):
        self.setWindowState(Qt.WindowMinimized)

    def on_maximizelabel_clicked(self, event:QMouseEvent):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def toggleMaximizeWindow(self, event):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def on_closeeaction_clicked(self, event:QMouseEvent):
        self.close()

    def regEvents(self):
        self.web_view.urlChanged.connect(self.update_back_button)
        self.web_view.urlChanged.connect(self.update_forward_button)
        self.back_action.triggered.connect(self.web_view.back)
        self.forward_action.triggered.connect(self.web_view.forward)
        self.refresh_action.triggered.connect(self.web_view.reload)


    def setWidgetFlags(self):
        self.web_view.load(QUrl("https://www.baidu.com/"))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint)
        self.setStyleSheet("""
        
            QMainWindow {
                font-family: monospace;
                text-align: center;
                font-size: 0.9em;
                color: #fff;
                background: #F5F5F5;
                outline: none;
                border: none;
                cursor: pointer;
                padding: 10px 20px;
                -webkit-appearance: none;
            }
            
        """)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.white)

        path = QPainterPath()
        w, h = self.width(), self.height()
        radius = 20  # 圆角半径
        path.addRoundedRect(0, 0, w, h, radius, radius)
        painter.drawPath(path)


    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()


    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)

    def __init__(self):
        super().__init__()
        self.InitWindow()
        self.show()

    #back事件
    def update_back_button(self):
        self.back_action.setEnabled(self.web_view.history().canGoBack())
    #forward事件
    def update_forward_button(self):
        self.forward_action.setEnabled(self.web_view.history().canGoForward())

    def handle_link_clicked(self, url):
        # 将链接的 URL 转换为字符串
        url_string = url.toString()
        # 使用当前窗口加载链接
        self.web_view.page().load(QUrl(url_string))
