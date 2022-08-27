import sys
from pathlib import Path

from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebChannel import QWebChannel

from data.media import Media


class HelloWorldHtmlApp(QObject):

    @pyqtSlot()
    def foo(self):
        print('bar')

    @pyqtSlot(str)
    def debug(self, string):
        print(string)

    def test(self, string):
        Media.from_json(string)
        pass


def started():
    print("Loading started")


def progress(i):
    print(f"Loading {i}")


def finished(ok):
    print(f"finished {ok}")


def run(args, cwd):
    app = QApplication(args)
    web = QWebEngineView()

    web.loadStarted.connect(started)
    web.loadProgress.connect(progress)
    web.loadFinished.connect(finished)
    qurl = QUrl((cwd / "frontend" / "html" / "index.html").as_uri())
    #print(qurl.path())
    web.load(qurl)
    channel = QWebChannel()
    html_app = HelloWorldHtmlApp()
    channel.registerObject('backend', html_app)
    web.page().setWebChannel(channel)

    web.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    cwd = Path(__file__).parent
    #print(cwd)
    run(sys.argv, cwd)
