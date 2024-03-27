import smbus

class I2C:
    def __init__(self, busNumber, deviceAddress):
        self.bus = smbus.SMBus(busNumber)
        self.deviceAddress = deviceAddress

    def readData(self, registerAddress, numBytes):
        try:
            data = self.bus.read_i2c_block_data(self.deviceAddress, registerAddress, numBytes)
            return data
        except IOError as e:
            print(f"Error reading I2C data: {e}")
            return None

    def writeData(self, registerAddress, data):
        try:
            self.bus.write_i2c_block_data(self.deviceAddress, registerAddress, data)
        except IOError as e:
            print(f"Error writing I2C data: {e}")
