import pyvisa
import time

class Rigol:
    max_channels = {
        "831": 3,
        "832": 3,
        "821": 2,
        "811": 1
    }

    def __init__(self):
        '''
        Make sure that the instruments are powered on and discoverable before you run the script. 
        The init function will keep looping until it finds at least one instrument. 
        It will not look for more instruments after the funciton is called.      
        '''
        self.rm = pyvisa.ResourceManager()
        self.num = len(self.rm.list_resources())
        # print(self.rm.list_resources())
        # maybe loop until you find more than one device
        while self.num < 1:
            self.num = len(self.rm.list_resources())
            time.sleep(5)
        # should I continously look for more devices if someone plugs one in
        self.inst = []
        for i in range(self.num):
            self.inst.append(self.rm.open_resource(self.rm.list_resources()[i]))
            print(str(self.inst[i].query("*IDN?"))[:-1])
        self.types = []
        for i in self.inst:
            # assuming its a rigol machine with the normal idn format
            self.types.append(str(i.query("*IDN?"))[21:34])
            # print(str(i.query("*IDN?"))[21:24])
    
    def get_serial(self, index = 0):
        '''
        Function that returns the serial number of the instrument. 

        index is the location of the instrument in the instrument list. 
        The default is the first instrument in the list
        '''
        try:
            # assuming its the standard rigol format
            return str(self.rm.list_resources()[index][18:31])
        except IndexError:
            if self.num > 1:
                print("Index is out of range, valid indexes are: 0 -",self.num-1)
            else:
                print("Index is out of range, only valid index is 0")

    def get_num(self):
        '''
        Function that returns the number of connected instruments
        '''
        return self.num

    def get_voltage(self, index = 0, channel = 0):
        '''
        Function that returns the voltage of an instrument on a specific channel

        index is the index of the instrument in the instrument list. 
        The default is the first instrument in the list\n
        channel is the channel you would like to measure. 
        The default is the currently selected channel
        '''
        if channel == 0:
            return float(self.inst[index].query("MEAS:VOLT?"))
        return float(self.inst[index].query("MEAS:VOLT? CH"+str(channel)))
    
    def get_current(self, index = 0, channel = 0):
        '''
        Function that returns the current of an instrument on a specific channel

        index is the index of the instrument in the instrument list. 
        The default is the first instrument in the list\n
        channel is the channel you would like to measure. 
        The default is the currently selected channel
        '''
        if channel == 0:
            return float(self.inst[index].query("MEAS:CURR?"))
        return float(self.inst[index].query("MEAS:CURR? CH"+str(channel)))

    def get_power(self, index = 0, channel = 0):
        '''
        Function that returns the power of an instrument on a specific channel

        index is the index of the instrument in the instrument list. 
        The default is the first instrument in the list\n
        channel is the channel you would like to measure. 
        The default is the currently selected channel
        '''
        if channel == 0:
            return float(self.inst[index].query("MEAS:POWE?"))
        return float(self.inst[index].query("MEAS:POWE? CH"+str(channel)))

    def power_on(self, index = 0, channel = 0):
        '''
        Function that enables the output of a selected channel. 
        Make sure to set the output of the channel beforehand.

        index is the index of the instrument in the instrument list. 
        The default is the first instrument in the list\n
        channel is the channel you would like to turn on. 
        The default is the currently selected channel
        '''
        if channel == 0:
            self.inst[index].write(":OUTP ON")
            return
        self.inst[index].write(":OUTP CH"+str(channel)+",ON")
    
    def power_off(self, index = 0, channel = 0):
        '''
        Function that disables the output of a selected channel. 

        index is the index of the instrument in the instrument list. 
        The default is the first instrument in the list\n
        channel is the channel you would like to turn off. 
        The default is the currently selected channel
        '''
        if channel == 0:
            self.inst[index].write(":OUTP OFF")
            return
        self.inst[index].write(":OUTP CH"+str(channel)+",OFF")
    

    

    def set_voltage(self, volt, num = 0, channel = 1):
        if volt > 30.0:
            volt = 30.0
        if volt < 0:
            volt = 0
        self.inst[num].write(":APPL CH"+str(channel)+","+str(volt))