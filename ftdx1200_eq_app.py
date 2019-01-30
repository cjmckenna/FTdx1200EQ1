from PyQt5 import QtCore, QtGui, QtWidgets
from ftdx1200_eq_ui import Ui_MainWindow
from ftdxserfuncs import ftdxSerFuncs

class mainApp(QtWidgets.QMainWindow, Ui_MainWindow, ftdxSerFuncs):
    def __init__(self, parent=None):
        super(mainApp, self).__init__(parent)
        self.setupUi(self)

        # read in the list of serial ports on the computer
        self.serial_ports()

        # link slider changes to associated LCD displays
        self.poffeq1Freq.valueChanged.connect(self.poffeq1FreqLcd.display)
        self.poffeq1Level.valueChanged.connect(self.poffeq1LevelLcd.display)
        self.poffeq1Bw.valueChanged.connect(self.poffeq1BwLcd.display)
        self.poffeq2Freq.valueChanged.connect(self.poffeq2FreqLcd.display)
        self.poffeq2Level.valueChanged.connect(self.poffeq2LevelLcd.display)
        self.poffeq2Bw.valueChanged.connect(self.poffeq2BwLcd.display)
        self.poffeq3Freq.valueChanged.connect(self.poffeq3FreqLcd.display)
        self.poffeq3Level.valueChanged.connect(self.poffeq3LevelLcd.display)
        self.poffeq3Bw.valueChanged.connect(self.poffeq3BwLcd.display)
        self.poneq1Freq.valueChanged.connect(self.poneq1FreqLcd.display)
        self.poneq1Level.valueChanged.connect(self.poneq1LevelLcd.display)
        self.poneq1Bw.valueChanged.connect(self.poneq1BwLcd.display)
        self.poneq2Freq.valueChanged.connect(self.poneq2FreqLcd.display)
        self.poneq2Level.valueChanged.connect(self.poneq2LevelLcd.display)
        self.poneq2Bw.valueChanged.connect(self.poneq2BwLcd.display)
        self.poneq3Freq.valueChanged.connect(self.poneq3FreqLcd.display)
        self.poneq3Level.valueChanged.connect(self.poneq3LevelLcd.display)
        self.poneq3Bw.valueChanged.connect(self.poneq3BwLcd.display)

        # Connections to functions from ftdxserfuncs for setting up the com port settings and opening the connection
        self.comPortInput.currentIndexChanged.connect(self.setComPort)
        self.baudRate.currentIndexChanged.connect(self.setBaudRate)
        self.radioConnect.clicked.connect(self.open_serial)
        self.radioDisconnect.clicked.connect(self.close_serial)






if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv)
    ftdxGui = mainApp()
    ftdxGui.show()
    sys.exit(app.exec())