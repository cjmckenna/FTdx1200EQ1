from PyQt5 import QtCore, QtGui, QtWidgets
from ftdx1200_eq_ui import Ui_MainWindow
from ftdxserfuncs import ftdxSerFuncs

class mainApp(QtWidgets.QMainWindow, Ui_MainWindow, ftdxSerFuncs):
    def __init__(self, parent=None):
        super(mainApp, self).__init__(parent)
        self.setupUi(self)
        self.serial_ports()
        #self.comPortInput.setCurrentIndex(-1)
#        self.comPortInput.addItem('Select Port')
        #self.comPortInput.setItemText('Select Port')
        self.comPortInput.currentIndexChanged.connect(self.setComPort)
        #self.comPortInput.currentText.connect(self.setComPort)
        self.radioConnect.clicked.connect(self.open_serial)


if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv)
    ftdxGui = mainApp()
    ftdxGui.show()
    sys.exit(app.exec())