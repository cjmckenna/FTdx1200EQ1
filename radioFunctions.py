from ftdxserfuncs import ser


class radioFunctions(object):
    def loadcurrents(self):
        print("I am running loadcurrents")
        # Proc Off EQ1 Frequency
        ser.write('EX159;'.encode())
        self.pofffeq1ret = (ser.read_until(';').decode('utf-8', 'ignore').strip('EX159').rstrip(';'))
        print("POFF EQ1 Frequency Return Value", self.pofffeq1ret)
        print("This is from the dictionary: ", reverse_eq1_frequency_cat_values[self.pofffeq1ret])
        self.poffeq1Freq.setValue(int(self.pofffeq1ret))
        self.poffeq1Freq.repaint()
        ser.flushInput()
        ser.flushOutput()
