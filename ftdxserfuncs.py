import serial
import sys
import glob
from yaesuDict import *
import traceback

ser = serial.Serial(timeout=.02)


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
            ###print(ser.read_until(';').decode('UTF-8', 'ignore'))
            ###print(int(ser.read_until(';').decode('UTF-8', 'ignore').strip('EX159').rstrip(';')))
            self.pofffeq1Freqret = int((ser.read_until(';').decode('UTF-8', 'ignore').replace('EX159', '').rstrip(';')))
            print("POFF EQ1 Frequency Return Value", self.pofffeq1Freqret)
            print('Current Slider EQ1 POFF Frequency Value: ', self.poffeq1Freq.value())
            print('POFF EQ1 multiplied value: ', self.pofffeq1Freqret *100)
            if self.pofffeq1Freqret == 0:
                print('EQ is OFF')
                self.poffeq1Control.setCurrentIndex(0)
                self.poffeq1Control.repaint()
            elif self.pofffeq1Freqret == self.poffeq1Freq.value():
                print('Slider matches value')
                self.poffeq1Control.setCurrentIndex(1)
                self.poffeq1Control.repaint()
                self.poffeq1FreqLcd.display(self.pofffeq1Freqret *100)
                self.poffeq1FreqLcd.repaint()
            else:
                self.poffeq1Control.setCurrentIndex(1)
                self.poffeq1Control.repaint()
                self.poffeq1Freq.setValue(self.pofffeq1Freqret)

            # Proc Off EQ1 Level CAT item 160
            ser.write('EX160;'.encode())
            ###print(ser.read_until(';').decode('utf-8', 'ignore'))
            self.poffeq1Levelret = int((ser.read_until(';').decode('utf-8', 'ignore').replace('EX160', '').rstrip(';')))
            print("POFF EQ1 Level Return Value", self.poffeq1Levelret)
            if self.poffeq1Levelret == self.poffeq1Level.value():
                print('Level slider matches value')
                self.poffeq1LevelLcd.display(self.poffeq1Levelret)
                self.poffeq1LevelLcd.repaint()
            else:
                self.poffeq1Level.setValue(int(self.poffeq1Levelret))

            # Proc Off EQ1 Bandwidth CAT item 161
            ser.write('EX161;'.encode())
            self.poffeq1Bwret = int((ser.read_until(';').decode('utf-8', 'ignore').replace('EX161', '').rstrip(';')))
            print("POFF EQ1 Bandwidth Return Value", self.poffeq1Bwret)
            if self.poffeq1Bwret == self.poffeq1Bw.value():
                print('Level slider matches value')
                self.poffeq1BwLcd.display(self.poffeq1Bwret)
                self.poffeq1BwLcd.repaint()
            else:
                self.poffeq1Bw.setValue(int(self.poffeq1Bwret))

            # Proc Off EQ2 Frequency CAT item EX162
            ser.write('EX162;'.encode())
            self.pofffeq2Freqret = int((ser.read_until(';').decode('UTF-8', 'ignore').replace('EX162', '').rstrip(';')))
            print("POFF EQ2 Frequency Return Value", self.pofffeq2Freqret)
            print('Current Slider EQ2 POFF Frequency Value: ', self.poffeq2Freq.value())
            print('POFF EQ2 multiplied value: ', self.pofffeq2Freqret *100)
            self.pofffeq2FreqretConverted = int(reverse_eq2_frequency_cat_values[self.pofffeq2Freqret])
            print('Converted value for POFF EQ2 Freq: ', self.pofffeq2FreqretConverted)
            if self.pofffeq2Freqret == 0:
                print('EQ is OFF')
                self.poffeq2Control.setCurrentIndex(0)
                self.poffeq2Control.repaint()
            elif self.pofffeq2FreqretConverted == self.poffeq2Freq.value():
                print('Slider matches value')
                self.poffeq2Control.setCurrentIndex(1)
                self.poffeq2Control.repaint()
                self.poffeq2FreqLcd.display(self.pofffeq2FreqretConverted *100)
                self.poffeq2FreqLcd.repaint()
            else:
                self.poffeq2Freq.setValue(self.pofffeq2FreqretConverted)
                self.poffeq2Control.setCurrentIndex(1)
                self.poffeq2Control.repaint()

            # Proc Off EQ2 Level CAT item 163
            ser.write('EX163;'.encode())
            self.poffeq2Levelret = int((ser.read_until(';').decode('utf-8', 'ignore').replace('EX163', '').rstrip(';')))
            print("POFF EQ2 Level Return Value", self.poffeq2Levelret)
            if self.poffeq2Levelret == self.poffeq2Level.value():
                print('Level slider matches value')
                self.poffeq2LevelLcd.display(self.poffeq2Levelret)
                self.poffeq2LevelLcd.repaint()
            else:
                self.poffeq2Level.setValue(int(self.poffeq2Levelret))

            # Proc Off EQ2 Bandwidth CAT item 164
            ser.write('EX164;'.encode())
            self.poffeq2Bwret = int((ser.read_until(';').decode('utf-8', 'ignore').replace('EX164', '').rstrip(';')))
            print("POFF EQ2 Bandwidth Return Value", self.poffeq2Bwret)
            if self.poffeq2Bwret == self.poffeq2Bw.value():
                print('Level slider matches value')
                self.poffeq2BwLcd.display(self.poffeq2Bwret)
                self.poffeq2BwLcd.repaint()
            else:
                self.poffeq2Bw.setValue(int(self.poffeq2Bwret))

            # Proc Off EQ3 Frequency CAT item EX165
            ser.write('EX165;'.encode())
            self.pofffeq3Freqret = int((ser.read_until(';').decode('UTF-8', 'ignore').replace('EX165', '').rstrip(';')))
            print("POFF EQ3 Frequency Return Value", self.pofffeq3Freqret)
            print('Current Slider EQ3 POFF Frequency Value: ', self.poffeq3Freq.value())
            print('POFF EQ3 multiplied value: ', self.pofffeq3Freqret *100)
            self.pofffeq3FreqretConverted = int(reverse_eq3_frequency_cat_values[self.pofffeq3Freqret])
            print('Converted value for POFF EQ3 Freq: ', self.pofffeq3FreqretConverted)
            if self.pofffeq2Freqret == 0:
                print('EQ is OFF')
                self.poffeq2Control.setCurrentIndex(0)
                self.poffeq2Control.repaint()
            elif self.pofffeq3FreqretConverted == self.poffeq3Freq.value():
                print('Slider matches value')
                self.poffeq3Control.setCurrentIndex(1)
                self.poffeq3Control.repaint()
                self.poffeq3FreqLcd.display(self.pofffeq3FreqretConverted *100)
                self.poffeq3FreqLcd.repaint()
            else:
                self.poffeq3Freq.setValue(self.pofffeq3FreqretConverted)
                self.poffeq3Control.setCurrentIndex(1)
                self.poffeq3Control.repaint()

            # Proc Off EQ3 Level CAT item 166
            ser.write('EX166;'.encode())
            self.poffeq3Levelret = int((ser.read_until(';').decode('utf-8', 'ignore').replace('EX166', '').rstrip(';')))
            print("POFF EQ3 Level Return Value", self.poffeq3Levelret)
            if self.poffeq3Levelret == self.poffeq3Level.value():
                print('Level slider matches value')
                self.poffeq3LevelLcd.display(self.poffeq3Levelret)
                self.poffeq3LevelLcd.repaint()
            else:
                self.poffeq3Level.setValue(int(self.poffeq3Levelret))

            # Proc Off EQ3 Bandwidth CAT item 167
            ser.write('EX167;'.encode())
            self.poffeq3Bwret = int((ser.read_until(';').decode('utf-8', 'ignore').replace('EX167', '').rstrip(';')))
            print("POFF EQ3 Bandwidth Return Value", self.poffeq3Bwret)
            if self.poffeq3Bwret == self.poffeq3Bw.value():
                print('Level slider matches value')
                self.poffeq3BwLcd.display(self.poffeq3Bwret)
                self.poffeq3BwLcd.repaint()
            else:
                self.poffeq3Bw.setValue(int(self.poffeq3Bwret))

            # Proc On EQ1 Frequency CAT item EX168
            ser.write('EX168;'.encode())
            self.ponfeq1Freqret = int((ser.read_until(';').decode('UTF-8', 'ignore').replace('EX168', '').rstrip(';')))
            print("PON EQ1 Frequency Return Value", self.ponfeq1Freqret)
            print('Current Slider EQ1 PON Frequency Value: ', self.poneq1Freq.value())
            print('PON EQ1 multiplied value: ', self.ponfeq1Freqret *100)
            if self.ponfeq1Freqret == 0:
                print('EQ is OFF')
                self.poneq1Control.setCurrentIndex(0)
                self.poneq1Control.repaint()
            elif self.ponfeq1Freqret == self.poneq1Freq.value():
                self.poneq1Control.setCurrentIndex(1)
                self.poneq1Control.repaint()
                print('Slider matches value')
                self.poneq1FreqLcd.display(self.ponfeq1Freqret *100)
                self.poneq1FreqLcd.repaint()
            else:
                self.poneq1Freq.setValue(self.ponfeq1Freqret)
                self.poneq1Control.setCurrentIndex(1)
                self.poneq1Control.repaint()

            # Proc On EQ1 Level CAT item 169
            ser.write('EX169;'.encode())
            self.poneq1Levelret = int((ser.read_until(';').decode('utf-8', 'ignore').replace('EX169', '').rstrip(';')))
            print("PON EQ1 Level Return Value", self.poneq1Levelret)
            if self.poneq1Levelret == self.poneq1Level.value():
                print('Level slider matches value')
                self.poneq1LevelLcd.display(self.poneq1Levelret)
                self.poneq1LevelLcd.repaint()
            else:
                self.poneq1Level.setValue(int(self.poneq1Levelret))

            # Proc On EQ1 Bandwidth CAT item 170
            ser.write('EX170;'.encode())
            #print((ser.read_until(';').decode('utf-8', 'ignore')))
            self.poneq1Bwret = int((ser.read_until(';').decode('utf-8', 'ignore').replace('EX170', '').rstrip(';')))
            print("PON EQ1 Bandwidth Return Value", self.poneq1Bwret)
            if self.poneq1Bwret == self.poneq1Bw.value():
                print('Level slider matches value')
                self.poneq1BwLcd.display(self.poneq1Bwret)
                self.poneq1BwLcd.repaint()
            else:
                self.poneq1Bw.setValue(int(self.poneq1Bwret))

            # Proc On EQ2 Frequency CAT item EX171
            ser.write('EX171;'.encode())
            self.ponfeq2Freqret = int((ser.read_until(';').decode('UTF-8', 'ignore').replace('EX171', '').rstrip(';')))
            print("PON EQ2 Frequency Return Value", self.ponfeq2Freqret)
            print('Current Slider EQ2 PON Frequency Value: ', self.poneq2Freq.value())
            print('PON EQ2 multiplied value: ', self.ponfeq2Freqret *100)
            self.ponfeq2FreqretConverted = int(reverse_eq2_frequency_cat_values[self.ponfeq2Freqret])
            print('Converted value for PON EQ2 Freq: ', self.ponfeq2FreqretConverted)
            if self.ponfeq1Freqret == 0:
                print('EQ is OFF')
                self.poneq2Control.setCurrentIndex(0)
                self.poneq2Control.repaint()
            elif self.ponfeq2FreqretConverted == self.poneq2Freq.value():
                print('Slider matches value')
                self.poneq2Control.setCurrentIndex(1)
                self.poneq2Control.repaint()
                self.poneq2FreqLcd.display(self.ponfeq2FreqretConverted *100)
                self.poneq2FreqLcd.repaint()
            else:
                self.poneq2Freq.setValue(self.ponfeq2FreqretConverted)
                self.poneq2Control.setCurrentIndex(1)
                self.poneq2Control.repaint()

            # Proc On EQ2 Level CAT item 172
            ser.write('EX172;'.encode())
            self.poneq2Levelret = int((ser.read_until(';').decode('utf-8', 'ignore').replace('EX172', '').rstrip(';')))
            print("PON EQ2 Level Return Value", self.poneq2Levelret)
            if self.poneq2Levelret == self.poneq2Level.value():
                print('Level slider matches value')
                self.poneq2LevelLcd.display(self.poneq2Levelret)
                self.poneq2LevelLcd.repaint()
            else:
                self.poneq2Level.setValue(int(self.poneq2Levelret))

            # Proc On EQ2 Bandwidth CAT item 173
            ser.write('EX173;'.encode())
            self.poneq2Bwret = int((ser.read_until(';').decode('utf-8', 'ignore').replace('EX173', '').rstrip(';')))
            print("PON EQ2 Bandwidth Return Value", self.poneq2Bwret)
            if self.poneq2Bwret == self.poneq2Bw.value():
                print('Level slider matches value')
                self.poneq2BwLcd.display(self.poneq2Bwret)
                self.poneq2BwLcd.repaint()
            else:
                self.poneq2Bw.setValue(int(self.poneq2Bwret))

            # Proc On EQ3 Frequency CAT item EX174
            ser.write('EX174;'.encode())
            self.ponfeq3Freqret = int((ser.read_until(';').decode('UTF-8', 'ignore').replace('EX174', '').rstrip(';')))
            print("PON EQ3 Frequency Return Value", self.ponfeq3Freqret)
            print('Current Slider EQ3 PON Frequency Value: ', self.poneq3Freq.value())
            print('PON EQ3 multiplied value: ', self.ponfeq3Freqret *100)
            self.ponfeq3FreqretConverted = int(reverse_eq3_frequency_cat_values[self.ponfeq3Freqret])
            print('Converted value for PON EQ3 Freq: ', self.ponfeq3FreqretConverted)
            if self.ponfeq1Freqret == 0:
                print('EQ is OFF')
                self.poneq3Control.setCurrentIndex(0)
                self.poneq3Control.repaint()
            elif self.ponfeq3FreqretConverted == self.poneq3Freq.value():
                print('Slider matches value')
                self.poneq3Control.setCurrentIndex(1)
                self.poneq3Control.repaint()
                self.poneq3FreqLcd.display(self.ponfeq3FreqretConverted *100)
                self.poneq3FreqLcd.repaint()
            else:
                self.poneq3Freq.setValue(self.ponfeq3FreqretConverted)
                self.poneq3Control.setCurrentIndex(1)
                self.poneq3Control.repaint()

            # Proc On EQ3 Level CAT item 175
            ser.write('EX175;'.encode())
            self.poneq3Levelret = int((ser.read_until(';').decode('utf-8', 'ignore').replace('EX175', '').rstrip(';')))
            print("PON EQ3 Level Return Value", self.poneq3Levelret)
            if self.poneq3Levelret == self.poneq3Level.value():
                print('Level slider matches value')
                self.poneq3LevelLcd.display(self.poneq3Levelret)
                self.poneq3LevelLcd.repaint()
            else:
                self.poneq3Level.setValue(int(self.poneq3Levelret))

            # Proc On EQ3 Bandwidth CAT item 176
            ser.write('EX176;'.encode())
            self.poneq3Bwret = int((ser.read_until(';').decode('utf-8', 'ignore').replace('EX176', '').rstrip(';')))
            print("PON EQ3 Bandwidth Return Value", self.poneq3Bwret)
            if self.poneq3Bwret == self.poneq3Bw.value():
                print('Level slider matches value')
                self.poneq3BwLcd.display(self.poneq3Bwret)
                self.poneq3BwLcd.repaint()
            else:
                self.poneq3Bw.setValue(int(self.poneq3Bwret))

            self.messageLabel.setText(
                'Current settings read successfully')
            self.messageLabel.repaint()

            # Get the settings of the PROC and MIC EQ to see if on or off

            # Read Proc Setting
            ser.write('PR0;'.encode())
            self.vocalProcret = int((ser.read_until(';').decode('utf-8', 'ignore').replace('PR0', '').rstrip(';')))
            print("Voice Processor Return Value", self.vocalProcret)
            self.voiceprocControl.setCurrentIndex(self.vocalProcret)
            self.voiceprocControl.repaint()

            # Read EQ Setting
            ser.write('PR1;'.encode())
            self.micEqret = int((ser.read_until(';').decode('utf-8', 'ignore').replace('PR1', '').rstrip(';')))
            print("Voice Processor Return Value", self.micEqret)
            self.micEqControl.setCurrentIndex(self.micEqret)
            self.micEqControl.repaint()


        except Exception as e:
            print(str(e))
            traceback.print_exc()

    def poffeq1FreqSet(self, poffeq1FreqValue):
        try:
            print('Updating Proc Off EQ 1 Frequency to value: ', poffeq1FreqValue)
            self.poffeq1FreqLcd.display(poffeq1FreqValue * 100)
            self.poffeq1FreqLcd.repaint()
            self.poffeq1Control.setCurrentIndex(1)
            self.poffeq1Control.repaint()
            #self.newval = self.poffeq1Freq.value()
            # We would send the functions to update the radio from here
            poffeq1FreqSet = 'EX159' + eq1_frequency_cat_values[self.poffeq1Freq.value()] + ';'
            print('This is the value for the radio: ', poffeq1FreqSet)
            ser.write(poffeq1FreqSet.encode())
            ser.flushInput()
            #ser.flushOutput()
            print('Done writing')
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def poffeq1LevelSet(self, poffeq1LevelValue):
        try:
            print('Updating Proc Off EQ 1 Level to value: ', poffeq1LevelValue)
            self.poffeq1LevelLcd.display(poffeq1LevelValue)
            self.poffeq1LevelLcd.repaint()
            # We would send the functions to update the radio from here
            poffeq1LevelSet = 'EX160' + eq_level_cat_values[str(self.poffeq1Level.value())] + ';'
            print('This is the value for the radio: ', poffeq1LevelSet)
            ser.write(poffeq1LevelSet.encode())
            ser.flushInput()
            #ser.flushOutput()
            print('Done writing')
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def poffeq1BwSet(self, poffeq1BwValue):
        try:
            print('Updating Proc Off EQ 1 BW to value: ', poffeq1BwValue)
            self.poffeq1BwLcd.display(poffeq1BwValue)
            self.poffeq1BwLcd.repaint()
            # We would send the functions to update the radio from here
            poffeq1BwSet = 'EX161' + str(self.poffeq1Bw.value()).zfill(2) + ';'
            print('This is the value for the radio: ', poffeq1BwSet)
            ser.write(poffeq1BwSet.encode())
            ser.flushInput()
            #ser.flushOutput()
            print('Done writing')
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def poffeq2FreqSet(self, poffeq2FreqValue):
        try:
            print('Updating Proc Off EQ 2 Frequency to value: ', poffeq2FreqValue)
            self.poffeq2FreqLcd.display(poffeq2FreqValue * 100)
            self.poffeq2FreqLcd.repaint()
            self.poffeq2Control.setCurrentIndex(1)
            self.poffeq2Control.repaint()
            # We would send the functions to update the radio from here
            poffeq2FreqSet = 'EX162' + eq2_frequency_cat_values[self.poffeq2Freq.value()] + ';'
            print('This is the value for the radio: ', poffeq2FreqSet)
            ser.write(poffeq2FreqSet.encode())
            ser.flushInput()
            #ser.flushOutput()
            print('Done writing')
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False


    def poffeq2LevelSet(self, poffeq2LevelValue):
        try:
            print('Updating Proc Off EQ 2 Level to value: ', poffeq2LevelValue)
            self.poffeq2LevelLcd.display(poffeq2LevelValue)
            self.poffeq2LevelLcd.repaint()
            # We would send the functions to update the radio from here
            poffeq2LevelSet = 'EX163' + eq_level_cat_values[str(self.poffeq2Level.value())] + ';'
            print('This is the value for the radio: ', poffeq2LevelSet)
            ser.write(poffeq2LevelSet.encode())
            ser.flushInput()
            #ser.flushOutput()
            print('Done writing')
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def poffeq2BwSet(self, poffeq2BwValue):
        try:
            print('Updating Proc Off EQ 2 BW to value: ', poffeq2BwValue)
            self.poffeq2BwLcd.display(poffeq2BwValue)
            self.poffeq2BwLcd.repaint()
            # We would send the functions to update the radio from here
            poffeq2BwSet = 'EX164' + str(self.poffeq2Bw.value()).zfill(2) + ';'
            print('This is the value for the radio: ', poffeq2BwSet)
            ser.write(poffeq2BwSet.encode())
            ser.flushInput()
            #ser.flushOutput()
            print('Done writing')
        except Exception as e:
            print(str(e))
        return False

    def poffeq3FreqSet(self, poffeq3FreqValue):
        try:
            print('Updating Proc Off EQ 3 Frequency to value: ', poffeq3FreqValue)
            self.poffeq3FreqLcd.display(poffeq3FreqValue * 100)
            self.poffeq3FreqLcd.repaint()
            self.poffeq3Control.setCurrentIndex(1)
            self.poffeq3Control.repaint()
            # We would send the functions to update the radio from here
            poffeq3FreqSet = 'EX165' + eq3_frequency_cat_values[self.poffeq3Freq.value()] + ';'
            print('This is the value for the radio: ', poffeq3FreqSet)
            ser.write(poffeq3FreqSet.encode())
            ser.flushInput()
            #ser.flushOutput()
            print('Done writing')
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def poffeq3LevelSet(self, poffeq3LevelValue):
        try:
            print('Updating Proc Off EQ 3 Level to value: ', poffeq3LevelValue)
            self.poffeq3LevelLcd.display(poffeq3LevelValue)
            self.poffeq3LevelLcd.repaint()
            # We would send the functions to update the radio from here
            poffeq3LevelSet = 'EX166' + eq_level_cat_values[str(self.poffeq3Level.value())] + ';'
            print('This is the value for the radio: ', poffeq3LevelSet)
            ser.write(poffeq3LevelSet.encode())
            ser.flushInput()
            #ser.flushOutput()
            print('Done writing')
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def poffeq3BwSet(self, poffeq3BwValue):
        try:
            print('Updating Proc Off EQ 3 BW to value: ', poffeq3BwValue)
            self.poffeq3BwLcd.display(poffeq3BwValue)
            self.poffeq3BwLcd.repaint()
            # We would send the functions to update the radio from here
            poffeq3BwSet = 'EX167' + str(self.poffeq3Bw.value()).zfill(2) + ';'
            print('This is the value for the radio: ', poffeq3BwSet)
            ser.write(poffeq3BwSet.encode())
            ser.flushInput()
            #ser.flushOutput()
            print('Done writing')
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def poneq1FreqSet(self, poneq1FreqValue):
        try:
            print('Updating Proc On EQ 1 Frequency to value: ', poneq1FreqValue)
            self.poneq1FreqLcd.display(poneq1FreqValue * 100)
            self.poneq1FreqLcd.repaint()
            #self.newval = self.poneq1Freq.value()
            # We would send the functions to update the radio from here
            poneq1FreqSet = 'EX168' + eq1_frequency_cat_values[self.poneq1Freq.value()] + ';'
            print('This is the value for the radio: ', poneq1FreqSet)
            ser.write(poneq1FreqSet.encode())
            ser.flushInput()
            print('Done writing')
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def poneq1LevelSet(self, poneq1LevelValue):
        try:
            print('Updating Proc On EQ 1 Level to value: ', poneq1LevelValue)
            self.poneq1LevelLcd.display(poneq1LevelValue)
            self.poneq1LevelLcd.repaint()
            # We would send the functions to update the radio from here
            poneq1LevelSet = 'EX169' + eq_level_cat_values[str(self.poneq1Level.value())] + ';'
            print('This is the value for the radio: ', poneq1LevelSet)
            ser.write(poneq1LevelSet.encode())
            ser.flushInput()
            print('Done writing')
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def poneq1BwSet(self, poneq1BwValue):
        try:
            print('Updating Proc On EQ 1 BW to value: ', poneq1BwValue)
            self.poneq1BwLcd.display(poneq1BwValue)
            self.poneq1BwLcd.repaint()
            # We would send the functions to update the radio from here
            poneq1BwSet = 'EX170' + str(self.poneq1Bw.value()).zfill(2) + ';'
            print('This is the value for the radio: ', poneq1BwSet)
            ser.write(poneq1BwSet.encode())
            ser.flushInput()
            #ser.flushOutput()
            print('Done writing')
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def poneq2FreqSet(self, poneq2FreqValue):
        try:
            print('Updating Proc On EQ 2 Frequency to value: ', poneq2FreqValue)
            self.poneq2FreqLcd.display(poneq2FreqValue * 100)
            self.poneq2FreqLcd.repaint()
            # We would send the functions to update the radio from here
            poneq2FreqSet = 'EX171' + eq2_frequency_cat_values[self.poneq2Freq.value()] + ';'
            print('This is the value for the radio: ', poneq2FreqSet)
            ser.write(poneq2FreqSet.encode())
            ser.flushInput()
            #ser.flushOutput()
            print('Done writing')
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False


    def poneq2LevelSet(self, poneq2LevelValue):
        try:
            print('Updating Proc On EQ 2 Level to value: ', poneq2LevelValue)
            self.poneq2LevelLcd.display(poneq2LevelValue)
            self.poneq2LevelLcd.repaint()
            # We would send the functions to update the radio from here
            poneq2LevelSet = 'EX172' + eq_level_cat_values[str(self.poneq2Level.value())] + ';'
            print('This is the value for the radio: ', poneq2LevelSet)
            ser.write(poneq2LevelSet.encode())
            ser.flushInput()
            #ser.flushOutput()
            print('Done writing')
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def poneq2BwSet(self, poneq2BwValue):
        try:
            print('Updating Proc On EQ 2 BW to value: ', poneq2BwValue)
            self.poneq2BwLcd.display(poneq2BwValue)
            self.poneq2BwLcd.repaint()
            # We would send the functions to update the radio from here
            poneq2BwSet = 'EX173' + str(self.poneq2Bw.value()).zfill(2) + ';'
            print('This is the value for the radio: ', poneq2BwSet)
            ser.write(poneq2BwSet.encode())
            ser.flushInput()
            #ser.flushOutput()
            print('Done writing')
        except Exception as e:
            print(str(e))
        return False

    def poneq3FreqSet(self, poneq3FreqValue):
        try:
            print('Updating Proc On EQ 3 Frequency to value: ', poneq3FreqValue)
            self.poneq3FreqLcd.display(poneq3FreqValue * 100)
            self.poneq3FreqLcd.repaint()
            # We would send the functions to update the radio from here
            poneq3FreqSet = 'EX174' + eq3_frequency_cat_values[self.poneq3Freq.value()] + ';'
            print('This is the value for the radio: ', poneq3FreqSet)
            ser.write(poneq3FreqSet.encode())
            ser.flushInput()
            #ser.flushOutput()
            print('Done writing')
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def poneq3LevelSet(self, poneq3LevelValue):
        try:
            print('Updating Proc On EQ 3 Level to value: ', poneq3LevelValue)
            self.poneq3LevelLcd.display(poneq3LevelValue)
            self.poneq3LevelLcd.repaint()
            # We would send the functions to update the radio from here
            poneq3LevelSet = 'EX175' + eq_level_cat_values[str(self.poneq3Level.value())] + ';'
            print('This is the value for the radio: ', poneq3LevelSet)
            ser.write(poneq3LevelSet.encode())
            ser.flushInput()
            #ser.flushOutput()
            print('Done writing')
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def poneq3BwSet(self, poneq3BwValue):
        try:
            print('Updating Proc On EQ 3 BW to value: ', poneq3BwValue)
            self.poneq3BwLcd.display(poneq3BwValue)
            self.poneq3BwLcd.repaint()
            # We would send the functions to update the radio from here
            poneq3BwSet = 'EX176' + str(self.poneq3Bw.value()).zfill(2) + ';'
            print('This is the value for the radio: ', poneq3BwSet)
            ser.write(poneq3BwSet.encode())
            ser.flushInput()
            #ser.flushOutput()
            print('Done writing')
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def poffeq1controlSet(self):
        try:
            print('Changing POFF EQ1 On or Off')
            print(self.poffeq1Control.currentIndex())
            if self.poffeq1Control.currentIndex() == 0:
                ser.write('EX15900;'.encode())
            elif self.poffeq1Control.currentIndex() == 1:
                poffeq1FreqSet = 'EX159' + eq1_frequency_cat_values[self.poffeq1Freq.value()] + ';'
                print('This is the value for the radio: ', poffeq1FreqSet)
                ser.write(poffeq1FreqSet.encode())
                ser.flushInput()
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def poffeq2controlSet(self):
        try:
            print('Changing POFF EQ2 On or Off')
            print(self.poffeq2Control.currentIndex())
            if self.poffeq2Control.currentIndex() == 0:
                ser.write('EX16200;'.encode())
            elif self.poffeq2Control.currentIndex() == 1:
                poffeq2FreqSet = 'EX162' + eq2_frequency_cat_values[self.poffeq2Freq.value()] + ';'
                print('This is the value for the radio: ', poffeq2FreqSet)
                ser.write(poffeq2FreqSet.encode())
                ser.flushInput()
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def poffeq3controlSet(self):
        try:
            print('Changing POFF EQ3 On or Off')
            print(self.poffeq3Control.currentIndex())
            if self.poffeq3Control.currentIndex() == 0:
                ser.write('EX16500;'.encode())
            elif self.poffeq3Control.currentIndex() == 1:
                poffeq3FreqSet = 'EX165' + eq3_frequency_cat_values[self.poffeq3Freq.value()] + ';'
                print('This is the value for the radio: ', poffeq3FreqSet)
                ser.write(poffeq3FreqSet.encode())
                ser.flushInput()
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def poneq1controlSet(self):
        try:
            print('Changing PON EQ1 On or Off')
            print(self.poneq1Control.currentIndex())
            if self.poneq1Control.currentIndex() == 0:
                ser.write('EX16800;'.encode())
            elif self.poneq1Control.currentIndex() == 1:
                poneq1FreqSet = 'EX168' + eq1_frequency_cat_values[self.poneq1Freq.value()] + ';'
                print('This is the value for the radio: ', poneq1FreqSet)
                ser.write(poneq1FreqSet.encode())
                ser.flushInput()
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def poneq2controlSet(self):
        try:
            print('Changing PON EQ2 On or Off')
            print(self.poneq2Control.currentIndex())
            if self.poneq2Control.currentIndex() == 0:
                ser.write('EX17100;'.encode())
            elif self.poneq2Control.currentIndex() == 1:
                poneq2FreqSet = 'EX171' + eq2_frequency_cat_values[self.poneq2Freq.value()] + ';'
                print('This is the value for the radio: ', poneq2FreqSet)
                ser.write(poneq2FreqSet.encode())
                ser.flushInput()
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def poneq3controlSet(self):
        try:
            print('Changing PON EQ3 On or Off')
            print(self.poneq3Control.currentIndex())
            if self.poneq3Control.currentIndex() == 0:
                ser.write('EX17400;'.encode())
            elif self.poneq3Control.currentIndex() == 1:
                poneq3FreqSet = 'EX174' + eq3_frequency_cat_values[self.poneq3Freq.value()] + ';'
                print('This is the value for the radio: ', poneq3FreqSet)
                ser.write(poneq3FreqSet.encode())
                ser.flushInput()
        except Exception as e:
            print(str(e))
            traceback.print_exc()
        return False

    def vocalProcControler(self, procControlVal):
        print('Changing vocal proc setting', procControlVal)
        vocalProcValue = 'PR0' + str(procControlVal) + ';'
        ser.write(vocalProcValue.encode())

    def micEqControler(self, micEqControlerVal):
        print('Changing vocal proc setting', micEqControlerVal)
        vmicEqValue = 'PR1' + str(micEqControlerVal) + ';'
        ser.write(vmicEqValue.encode())