from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout

from src.xlyy_window.gpt_mainWindow import PrivateEngineView


class test_Browser(QMainWindow):
    def __init__(self):
        super(test_Browser, self).__init__()
        self.browser = PrivateEngineView()
        self.url_bar = QLineEdit()
        self.go_button = QPushButton('go')
        self.back_button = QPushButton('<-')
        self.forward_button = QPushButton('->')
        self.init_ui()
        self.show()
    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.back_button)
        h_layout.addWidget(self.forward_button)
        h_layout.addWidget(self.url_bar)
        h_layout.addWidget(self.go_button)
        layout.addLayout(h_layout)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.go_button.clicked.connect(self.load_url)
        self.back_button.clicked.connect(self.browser.back)
        self.forward_button.clicked.connect(self.browser.forward)
        self.url_bar.returnPressed.connect(self.load_url)
    def load_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))