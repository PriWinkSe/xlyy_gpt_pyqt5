from abc import ABCMeta, ABC, abstractmethod

from PyQt5.QtWidgets import QWidget


class windowMeta(ABCMeta, type(QWidget)):
    pass

class AbstractWindow(QWidget, ABC, metaclass=windowMeta):
    #初始化窗口
    @abstractmethod
    def InitWindow(self):
        ...

    @abstractmethod
    def setupWindowBasicAttributes(self):
        ...

    #添加组件,布局
    @abstractmethod
    def setupWidgets(self):
        ...
    #注册事件
    @abstractmethod
    def regEvents(self):
        ...
    #设置组件属性
    @abstractmethod
    def setWidgetFlags(self):
        ...