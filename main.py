import os
import sys
from io import BytesIO

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication

from ai_module import ali_nls
from core import wsa_server
from gui import flask_server
from gui.window import MainWindow
from utils import config_util
from scheduler.thread_manager import MyThread
from core.content_db import Content_Db
import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 5)

def __clear_samples():
    if not os.path.exists("./samples"):
        os.mkdir("./samples")
    for file_name in os.listdir('./samples'):
        if file_name.startswith('sample-'):
            os.remove('./samples/' + file_name)


def __clear_logs():
    if not os.path.exists("./logs"):
        os.mkdir("./logs")
    for file_name in os.listdir('./logs'):
        if file_name.endswith('.log'):
            os.remove('./logs/' + file_name)

def __clear_timer():
    if os.path.exists("./timer.db"):
        os.remove("./timer.db")
if __name__ == '__main__':
    __clear_samples()
    __clear_logs()
    __clear_timer()
    
    contentdb = Content_Db()
    contentdb.init_db()     
    ws_server = wsa_server.new_instance(port=10002)
    ws_server.start_server()
    web_ws_server = wsa_server.new_web_instance(port=10003)
    web_ws_server.start_server()
    if config_util.ASR_mode == "ali":
        ali_nls.start()
    flask_server.start()
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    win = MainWindow()
    win.show()
    app.exit(app.exec_())

    
