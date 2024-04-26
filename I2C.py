import smbus
import time

class I2C:
    def __init__(self, busNumber, deviceAddress):
        self.bus = smbus.SMBus(busNumber)
        self.deviceAddress = deviceAddress

    def read_sht30(self):
        # Send the command to read temperature and humidity
        self.bus.write_i2c_block_data(self.deviceAddress, 0x24, [0x00])
        time.sleep(0.015)  # Wait for the sensor to process the command

        # Read the 6 bytes of data
        data = self.bus.read_i2c_block_data(self.deviceAddress, 0x00, 6)

        # Convert the data
        temp = data[0] * 256 + data[1]
        temp = -45 + (175 * temp / 65535.0)
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

        return temp, humidity

    def writeData(self, registerAddress, data):
        try:
            self.bus.write_i2c_block_data(self.deviceAddress, registerAddress, data)
        except IOError as e:
            print(f"Error writing I2C data: {e}")