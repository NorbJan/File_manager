
from PyQt5 import QtWidgets

from Presenter import Presenter
from Model import Model
from View import View

class Setup(object):
    
    def __init__(self):
        # Creating Model and View
        self.__view = View()
        self.__model = Model()

        # Creating Presenter
        self.__presenter = Presenter(self.__model, self.__view)
    
    def show_window(self):
        self.__view.show()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    manager = Setup()
    manager.show_window()
    
    sys.exit(app.exec_())