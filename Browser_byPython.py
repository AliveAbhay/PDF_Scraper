from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLineEdit
import sys
from PyQt5.QtWebEngineWidgets import QWebEngineView

class BrowserWindow(QMainWindow):
    def __init__(self):
        super(BrowserWindow, self).__init__()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        self.setCentralWidget(self.browser)
        self.showMaximized()

        # Navigation Bar
        navbar = self.createNavbar()
        self.addToolBar(navbar)

    def createNavbar(self):
        navbar = self.addToolBar("Navigation")

        # Back button
        back_btn = QAction('Back', self)
        back_btn.setStatusTip('Back to previous page')
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        # Forward button
        forward_btn = QAction('Forward', self)
        forward_btn.setStatusTip('Forward to next page')
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        # Reload button
        reload_btn = QAction('Reload', self)
        reload_btn.setStatusTip('Reload page')
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        navbar.addWidget(self.url_bar)

        # Home button
        home_btn = QAction('Home', self)
        home_btn.setStatusTip('Go home')
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # Stop button
        stop_btn = QAction('Stop', self)
        stop_btn.setStatusTip('Stop loading current page')
        stop_btn.triggered.connect(self.browser.stop)
        navbar.addAction(stop_btn)

        return navbar

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.browser.setUrl(q)

app = QApplication(sys.argv)
QApplication.setApplicationName("Simple Browser")
window = BrowserWindow()
app.exec_()