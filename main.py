import sys
#3rd party
from PyQt5.QtWidgets import QApplication
import numpy as np

from mainwindow import MainWindow

def main():

    app = QApplication(sys.argv)
    root = MainWindow()

    root.show()
    app.exec_()

if __name__ == '__main__':
    
    main()
