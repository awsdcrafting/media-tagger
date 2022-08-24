import sys
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebChannel import QWebChannel


class HelloWorldHtmlApp(QObject):

    @pyqtSlot()
    def foo(self):
        print('bar')

    @pyqtSlot(str)
    def debug(self, string):
        print(string)


def run(args):
    app = QApplication(args)

    web = QWebEngineView()
    web.load(QUrl("file:///html/index.html"))
    #web.load(QUrl("file:///html/tree.html"))
    channel = QWebChannel()
    html_app = HelloWorldHtmlApp()
    channel.registerObject('backend', html_app)
    web.page().setWebChannel(channel)

    web.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run(sys.argv)
