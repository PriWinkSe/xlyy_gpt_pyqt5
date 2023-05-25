import json

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QMouseEvent, QPainter, QPainterPath, QCursor
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QToolBar, QSizePolicy, QAction
from abstract_window import AbstractWindow
from io_util import get_last_dir,get_center_screenGeometry
from str_util import String
from sys_util import xmprint
from xlyyEngineView import PrivateEngineView


class xlyy_GPT(QMainWindow, AbstractWindow):
    def InitWindow(self):
        self.readConfigFile()
        self.setupWindowBasicAttributes()
        self.setupWidgets()
        self.regEvents()
        self.setWidgetFlags()

    def readConfigFile(self):
        # 获取 JSON 文件的绝对路径
        json_path = get_last_dir(3) + '\Configs\window_settings.json'
        # 读取 JSON 文件
        with open(json_path, 'r') as f:
            json_data = json.load(f)
        # 访问 JSON 数据
        self.first_Page:str = json_data['openUrl']  # 输出 https://poe.com/
        self.isStoreCache:bool = json_data['isStoreCache']  # 输出 1
        self.defaultHeight = json_data['defaultHeight']
        self.defaultWidth = json_data['defaultWidth']
        s = String(json_data['WindowIcon'])
        s.replaceAll('/','\\')
        self.windowIconPath = s.string
        xmprint(get_last_dir(3) + self.windowIconPath)
        self.setWindowIcon(QIcon(get_last_dir(3) + self.windowIconPath))

    def setupWindowBasicAttributes(self):
        self.setWindowTitle("Qt5_GPT")
        #self.setGeometry(100, 100, 1200, 800)
        self.setGeometry(get_center_screenGeometry(self,self.defaultHeight,self.defaultWidth))

    def setupWidgets(self):
        self.toolbar = QToolBar()
        # 设置工具栏样式

        actionStyle = '''
                    QToolBar {
                        border-top-left-radius: 15px;
                        border-top-right-radius: 15px;
                        border: 0;
                        background-color: deepskyblue;
                        background-clip: padding-box;
                    }
                    
                    QToolBar > * {
                        border-top-left-radius: 15px;
                        border-top-right-radius: 15px;
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
                        padding: 10px 20px;
                        background-clip: padding-box;
                   }
                   
                   QToolButton:first {
                    }
                    
                    QToolButton:last {
                    }
                   
                   QToolButton:disabled {
                        background-color: #CCCCCC;
                        font-family: monospace;
                        text-align: center;
                        font-size: 0.9em;
                        color: #fff;
                        outline: none;
                        border: none;
                        padding: 10px 20px;
                    }

                   QToolButton:hover {
                        background: dodgerblue;
                        color: #ffffff;
                   }         
               '''
        self.toolbar.setMovable(False)
        self.toolbar.setCursor(QCursor(Qt.ArrowCursor))
        self.toolbar.setContextMenuPolicy(Qt.CustomContextMenu)
        self.toolbar.mouseDoubleClickEvent = self.toggleMaximizeWindow
        self.toolbar.setMaximumHeight(38)
        self.addToolBar(self.toolbar)

        self.back_action = QAction("后退", self)
        self.back_action.setEnabled(True)
        self.toolbar.addAction(self.back_action)

        self.forward_action = QAction("前进", self)
        self.forward_action.setEnabled(False)
        self.toolbar.addAction(self.forward_action)

        self.refresh_action = QAction("刷新", self)

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
        self.web_view = PrivateEngineView(self.isStoreCache)
        self.toolbar.setStyleSheet(actionStyle)
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
        xmprint('当前加载的主页: ' + self.first_Page)
        self.web_view.load(QUrl(self.first_Page))
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            QMainWindow {
                font-family: monospace;
                text-align: center;
                font-size: 0.9em;
                color: #fff;
                background: #F5F5F5;
                outline: none;
                border: none;
                padding: 10px 20px;
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
