from PyQt5 import QtWidgets
from ftdx1200_eq_ui import Ui_MainWindow
from ftdxserfuncs import ftdxSerFuncs, radioFunctions
import traceback


class mainApp(QtWidgets.QMainWindow, Ui_MainWindow, ftdxSerFuncs, radioFunctions):
    def __init__(self, parent=None):
        super(mainApp, self).__init__(parent)
        self.setupUi(self)

        # read in the list of serial ports on the computer
        self.serial_ports()

        # link slider changes to associated LCD displays
        self.poffeq1Freq.valueChanged[int].connect(self.poffeq1FreqSet)
        self.poffeq1Level.valueChanged[int].connect(self.poffeq1LevelSet)
        self.poffeq1Bw.valueChanged[int].connect(self.poffeq1BwSet)
        self.poffeq2Freq.valueChanged[int].connect(self.poffeq2FreqSet)
        self.poffeq2Level.valueChanged[int].connect(self.poffeq2LevelSet)
        self.poffeq2Bw.valueChanged[int].connect(self.poffeq2BwSet)
        self.poffeq3Freq.valueChanged[int].connect(self.poffeq3FreqSet)
        self.poffeq3Level.valueChanged[int].connect(self.poffeq3LevelSet)
        self.poffeq3Bw.valueChanged[int].connect(self.poffeq3BwSet)
        self.poneq1Freq.valueChanged[int].connect(self.poneq1FreqSet)
        self.poneq1Level.valueChanged[int].connect(self.poneq1LevelSet)
        self.poneq1Bw.valueChanged[int].connect(self.poneq1BwSet)
        self.poneq2Freq.valueChanged[int].connect(self.poneq2FreqSet)
        self.poneq2Level.valueChanged[int].connect(self.poneq2LevelSet)
        self.poneq2Bw.valueChanged[int].connect(self.poneq2BwSet)
        self.poneq3Freq.valueChanged[int].connect(self.poneq3FreqSet)
        self.poneq3Level.valueChanged[int].connect(self.poneq3LevelSet)
        self.poneq3Bw.valueChanged[int].connect(self.poneq3BwSet)
        self.poffeq1Control.currentIndexChanged[int].connect(self.poffeq1controlSet)
        self.poffeq2Control.currentIndexChanged[int].connect(self.poffeq2controlSet)
        self.poffeq3Control.currentIndexChanged[int].connect(self.poffeq3controlSet)
        self.poneq1Control.currentIndexChanged[int].connect(self.poneq1controlSet)
        self.poneq2Control.currentIndexChanged[int].connect(self.poneq2controlSet)
        self.poneq3Control.currentIndexChanged[int].connect(self.poneq3controlSet)
        self.voiceprocControl.currentIndexChanged[int].connect(self.vocalProcControler)
        self.micEqControl.currentIndexChanged[int].connect(self.micEqControler)



        # Connections to functions from ftdxserfuncs for setting up the com port settings and opening the connection
        self.comPortInput.currentIndexChanged[int].connect(self.setComPort)
        self.baudRate.currentIndexChanged[int].connect(self.setBaudRate)
        self.radioConnect.clicked.connect(self.open_serial)
        self.radioDisconnect.clicked.connect(self.close_serial)


if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv)
    ftdxGui = mainApp()
    ftdxGui.show()
    sys.exit(app.exec())