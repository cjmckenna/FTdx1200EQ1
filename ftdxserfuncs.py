import serial
import sys
import glob

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

    def com_on_select(event=None):

        # get selection from event
        print("event.widget:", event.widget.get())

        # or get selection directly from combobox
        print("comboboxes: ", event.widget.get())
        ser.port = event.widget.get()
        print("What I set as a var: ", ser.port)

    def open_serial(self):
        ser.open()
        print(ser.is_open)
        print("I am opening the port")

        #########################################################################
        # now we have to actually test that we can talk to the radio
        ser.write('FA;'.encode())
        readret = (ser.read(1).decode('utf-8', 'ignore'))
        print("Return Value", readret)

        if readret != 'F':
            print("Oh Crap!")
            ser.close()
        else:

            amiopen = str(ser.is_open)
            print(amiopen)
            if amiopen == "True":
                print('Yep... its open')
                #radio_connect_button.config(highlightbackground='#4ca64c')
                #radio_connect_button.config(text='Connected')
                self.loadcurrents()
            else:
                print('something went wrong')

    def close_serial(self):
        ser.close()             # close port
        print(ser.is_open)
        radio_connect_button.config(highlightbackground='#db3328')
        radio_connect_button.config(text='Connect')

    def setComPort(self, portval):
        print('Selected Com Port: ', self.comPortInput.itemText(portval))
        ser.port = self.comPortInput.itemText(portval)
        print('This is the port variable: ', ser.port)