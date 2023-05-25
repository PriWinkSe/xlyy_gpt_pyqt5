import sys

from PyQt5.QtWidgets import QApplication, QStyle

from src.xlyy_window.gpt_mainWindow import xlyy_GPT

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = xlyy_GPT()
    #w = test_Browser()
    sys.exit(app.exec_())