import minimalmodbus

class ModBus:
    def __init__(self, port, peripheral_address):
        self.instrument = minimalmodbus.Instrument(port, peripheral_address)
        self.instrument.serial.baudrate = 9600
        self.instrument.serial.timeout = 0.1

    def readData(self, register_address):
        try:
            data = self.instrument.read_register(register_address, functioncode=3)
            return data
        except Exception as e:
            print(f"Error reading data: {e}")
            return None
