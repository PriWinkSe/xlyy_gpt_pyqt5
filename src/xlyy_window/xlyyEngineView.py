import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QToolBar, QPushButton, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage, QWebEngineSettings, \
    QWebEngineHistoryItem
from src.common_utils.io_util import get_last_dir, is_executable
from src.common_utils.sys_util import xmprint


class PrivateEngineView(QWebEngineView):
    def __init__(self):
        super(PrivateEngineView, self).__init__()
        self.load_privateCache()
        #self.Traceless_load()
        #self.page().urlChanged.connect(self.url_changed)

    #无痕模式
    def Traceless_load(self):
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.setHttpCacheType(QWebEngineProfile.NoCache)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
        self.setUrl(QUrl("about:blank"))

    #保存缓存
    def load_privateCache(self):
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.setCachePath(get_last_dir(5)+'\Cache\CachePath')
        self.profile.setPersistentStoragePath(get_last_dir(3)+'\Cache\PersistentPath')
        self.profile.setDownloadPath(get_last_dir(3)+'\Cache\DownloadPath')
        self.profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)
        cache_path = QWebEngineProfile.defaultProfile().cachePath()
        xmprint('[PrivateEngineView]当前浏览器缓存路径: '+ cache_path)
        self.setUrl(QUrl("about:blank"))
        xmprint("[PrivateEngineView]加载缓存成功")

    def createWindow(self, _type: QWebEnginePage.WebWindowType) -> 'QWebEngineView':
        if _type == QWebEnginePage.WebBrowserTab:
            return self
        elif _type == QWebEnginePage.WebBrowserBackgroundTab:
            # 在后台打开新标签页（可根据需求进行处理）
            pass
        elif _type == QWebEnginePage.WebBrowserWindow:
            # 在新窗口中打开链接（可根据需求进行处理）
            pass
        return super(PrivateEngineView, self).createWindow(_type)

    def url_changed(self, url: QUrl):
        ...




