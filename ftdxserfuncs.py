import serial
import sys
import glob
from yaesuDict import reverse_eq1_frequency_cat_values
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
            print(ports)
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
                self.messageLabel.repaint()
                ser.flushInput()
                ser.flushOutput()
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
                    ser.flushInput()
                    ser.flushOutput()
                    self.loadCurrents()
                else:
                    print('something went wrong')
        except Exception as e:
            self.messageLabel.setText(
                'A problem occured connecting to the radio.  Please check that you have selected the proper com port and baud rate')
            self.messageLabel.repaint()
            print(str(e))

    def close_serial(self):
        try:
            ser.close()             # close port
            print(ser.is_open)
            self.messageLabel.setText(
                'Connection to radio has been closed')
            self.messageLabel.repaint()
        except:
            self.messageLabel.setText(
                'A problem occured disconnecting from the radio')
            self.messageLabel.repaint()

    def setComPort(self, portval):
        try:
            print('Selected Com Port: ', self.comPortInput.itemText(portval))
            ser.port = self.comPortInput.itemText(portval)
            print('This is the port variable: ', ser.port)
        except Exception as e:
            print(str(e))

    def setBaudRate(self, baudval):
        try:
            print('Selected Com Port: ', self.baudRate.itemText(baudval))
            ser.baudrate = self.baudRate.itemText(baudval)
            print('This is the baud variable: ', ser.baudrate)
        except Exception as e:
            print(str(e))

class radioFunctions(object):

    # This function will fetch the current settings for all of the EQs and update the UI to reflect current state
    def loadCurrents(self):
        try:
            print("I am running loadcurrents")

            # PROC OFF CURRENT SETTINGS READ

            # Proc Off EQ1 Frequency CAT item EX159
            ser.write('EX159;'.encode())
            self.pofffeq1ret = (ser.read_until(';').decode('UTF-8', 'ignore').strip('EX159').rstrip(';'))
            print("POFF EQ1 Frequency Return Value", self.pofffeq1ret)
            print("This is from the dictionary: ", reverse_eq1_frequency_cat_values[self.pofffeq1ret])
            self.poffeq1Freq.setValue(int(self.pofffeq1ret))
            self.poffeq1Freq.repaint()
            ser.flushInput()
            ser.flushOutput()

            # Proc Off EQ1 Level CAT item 160
            ser.write('EX160;'.encode())
            poffeq1Levelret = (ser.read_until(';').decode('utf-8', 'ignore').strip('EX160').rstrip(';'))
            print("POFF EQ1 Level Return Value", poffeq1Levelret)
            print("This is from the dictionary for EQ1 Level:", reverse_eq_level_cat_values[poffeq1levelret])
            self.poffeq1Level.setValue(int(self.poffeq1Levelret))
            self.poffeq1Level.repaint()
            ser.flushInput()
            ser.flushOutput()

            # Proc Off EQ1 Bandwidth CAT item 161
            ser.write('EX161;'.encode())
            poffeq1Bwret = int((ser.read_until(';').decode('utf-8', 'ignore').strip('EX161').rstrip(';')))
            print("POFF EQ1 Bandwidth Return Value", poffeq1Bwret)
            self.poffeq1Bw.setValue(int(self.poffeq1Bwret))
            self.poffeq1Bw.repaint()
            ser.flushInput()
            ser.flushOutput()

            '''


            # Proc Off EQ2 Frequency
            ser.write('EX162;'.encode())
            poffeq2Freqret = (ser.read_until(';').decode('utf-8', 'ignore').strip('EX162').rstrip(';'))
            # print("POFF EQ2 Frequency Return Value", poffeq2Freqret)
            # print("This is from the dictionary: ", reverse_eq2_frequency_cat_values[poffeq2Freqret])
            poff_eq2_frequency.set(reverse_eq2_frequency_cat_values[poffeq2Freqret])
            ser.flushInput()
            ser.flushOutput()
            elapsed_time = time.time() - start_time
            print("Proc Off EQ2 Frequency END Elapsed Time", elapsed_time)

            # Proc Off EQ2 Level CAT item 163
            ser.write('EX163;'.encode())
            poffeq2Levelret = (ser.read_until(';').decode('utf-8', 'ignore').strip('EX160').rstrip(';'))
            print("POFF EQ1 Level Return Value", poffeq2Levelret)
            print("This is from the dictionary for EQ1 Level:", reverse_eq_level_cat_values[poffeq2Levelret])
            self.poffeq1Level.setValue(int(self.poffeq2Levelret))
            self.poffeq1Level.repaint()
            ser.flushInput()
            ser.flushOutput()

            # Proc Off EQ1 Bandwidth CAT item 161
            ser.write('EX161;'.encode())
            poffeq1Bwret = int((ser.read_until(';').decode('utf-8', 'ignore').strip('EX161').rstrip(';')))
            print("POFF EQ1 Bandwidth Return Value", poffeq1Bwret)
            poff_eq1_bandw.set(poffeq1Bwret)
            ser.flushInput()
            ser.flushOutput()
'''



        except Exception as e:
            print(str(e))

    def poffeq1FreqSet(self, poffeq1FreqValue):
        try:
            print('Updating Proc Off EQ 1 Frequency to value: ', poffeq1FreqValue)
            self.poffeq1FreqLcd.display(poffeq1FreqValue * 100)
            # We would send the functions to update the radio from here
        except Exception as e:
            self.messageLabel.setText(
                'A problem occurred setting the radio')
            self.messageLabel.repaint()
            print(str(e))

    def poffeq1LevelSet(self, poffeq1LevelValue):
        try:
            print('Updating Proc Off EQ 1 Level to value: ', poffeq1LevelValue)
            self.poffeq1LevelLcd.display(poffeq1LevelValue)
            # We would send the functions to update the radio from here
        except Exception as e:
            self.messageLabel.setText(
                'A problem occurred setting the radio')
            self.messageLabel.repaint()
            print(str(e))

    def poffeq1BwSet(self, poffeq1BwValue):
        try:
            print('Updating Proc Off EQ 1 BW to value: ', poffeq1BwValue)
            self.poffeq1BwLcd.display(poffeq1BwValue)
            # We would send the functions to update the radio from here
        except Exception as e:
            self.messageLabel.setText(
                'A problem occurred setting the radio')
            self.messageLabel.repaint()
            print(str(e))

    def poffeq2FreqSet(self, poffeq2FreqValue):
        try:
            print('Updating Proc Off EQ 2 Frequency to value: ', poffeq2FreqValue)
            self.poffeq2FreqLcd.display(poffeq2FreqValue * 100)
            # We would send the functions to update the radio from here
        except Exception as e:
            self.messageLabel.setText(
                'A problem occurred setting the radio')
            self.messageLabel.repaint()
            print(str(e))

    def poffeq2LevelSet(self):
        pass

    def poffeq2BwSet(self):
        pass

    def poffeq3FreqSet(self):
        pass

    def poffeq3LevelSet(self):
        pass

    def poffeq3BwSet(self):
        pass

    def poneq1FreqSet(self):
        pass

    def poneq1LevelSet(self):
        pass

    def poneq1BwSet(self):
        pass

    def poneq2FreqSet(self):
        pass

    def poneq2LevelSet(self):
        pass

    def poneq2BwSet(self):
        pass

    def poneq3FreqSet(self):
        pass

    def poneq3LevelSet(self):
        pass

    def poneq3BwSet(self):
        pass

