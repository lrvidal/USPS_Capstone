import minimalmodbus
import time

class ModBus:
    def __init__(self, port, address):
        # Initialize Modbus Reader
        self.instr = minimalmodbus.Instrument(port, address)
        self.instr.serial.baudrate = 9600
        self.instr.handle_local_echo = False

    def read_modbus_float(self, register):
        for i in range(10):
            try:
                time.sleep(0.5)  # Add a delay of 0.5 seconds
                value = self.instr.read_float(register)
                return round(value, 4)
            except Exception as e:
                value = None
                print(e)
        return value
