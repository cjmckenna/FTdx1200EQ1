import serial
import sys
import glob
from PyQt5 import QtCore, QtGui, QtWidgets

ser = serial.Serial(timeout=.01)


class ftdxSerFuncs(object):


    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
                print(port)
                self.comPortInput.addItem(port)
            except (OSError, serial.SerialException):
                pass
        return result


    def open_serial(self):
        try:
            ser.open()
            print(ser.is_open)
            print("I am opening the port", ser.port)

            #########################################################################
            # now we have to actually test that we can talk to the radio
            ser.write('FA;'.encode())
            readret = (ser.read(1).decode('utf-8', 'ignore'))
            print("Return Value", readret)

            if readret != 'F':
                print("Oh Crap!")
                self.messageLabel.setText('Error opening connection to the radio.  Verify your comport and baud rate selections and try to connect again')
                ser.close()
            else:

                amiopen = str(ser.is_open)
                print(amiopen)
                if amiopen == "True":
                    print('Yep... its open')
                    self.messageLabel.setText(
                        'Successfully connected to the radio')
                    #radio_connect_button.config(highlightbackground='#4ca64c')
                    #radio_connect_button.config(text='Connected')
                    self.loadcurrents()
                else:
                    print('something went wrong')
        except:
            self.messageLabel.setText(
                'A problem occured connecting to the radio.  Please check that you have selected the proper com port and baud rate')

    def close_serial(self):
        try:
            ser.close()             # close port
            print(ser.is_open)
            self.messageLabel.setText(
                'Connection to radio has been closed')
        except:
            self.messageLabel.setText(
                'A problem occured disconnecting from the radio')

    def setComPort(self, portval):
        print('Selected Com Port: ', self.comPortInput.itemText(portval))
        ser.port = self.comPortInput.itemText(portval)
        print('This is the port variable: ', ser.port)

    def setBaudRate(self, baudval):
        print('Selected Com Port: ', self.baudRate.itemText(baudval))
        ser.baudrate = self.baudRate.itemText(baudval)
        print('This is the baud variable: ', ser.baudrate)