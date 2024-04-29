import minimalmodbus

class ModBus:
    def __init__(self, port, address) :
    # Initialize Modbus Reader
        self.instr = minimalmodbus.Instrument(port,address)
        self.instr.serial.baudrate = 9600
        self.instr.handle_local_echo = True

    def read_modbus_float(self, register):
        for i in range(10):
            try:
                value = self.instr.read_float(register)
                return round(value,4)
            except:
                value = None
        return value

