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
        data = self.bus.read_i2c_block_data(self.deviceAddress, 0)

        # Convert the data
        temp = data[0] * 256 + data[1]
        temp = -45 + (175 * temp / 65535.0)
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

        return temp, humidity

    def read_pressure(self):
        ADS1115_CONFIG_REGISTER = 0x01
        ADS1115_CHANNEL_0_CONFIG = [0x90, 0x83] # Gain of 2, 128 samples per sec
        WAIT_TIME = 8.1
        ADS1115_CONVERSION_REGISTER = 0x00
        # Set the ADS1115 to read from the appropriate channel
        # This depends on how the pressure transducer is connected to the ADS1115
        # For this example, I'll assume it's connected to channel 0
        self.bus.write_i2c_block_data(self.deviceAddress, ADS1115_CONFIG_REGISTER, ADS1115_CHANNEL_0_CONFIG)

        time.sleep(WAIT_TIME)  # Wait for the ADS1115 to complete the conversion

        # Read the conversion result
        data = self.bus.read_i2c_block_data(self.deviceAddress, ADS1115_CONVERSION_REGISTER)

        # Convert the raw data to voltage
        raw_adc = data[0] << 8 | data[1]

        # Calculate the slope and intercept of the line
        slope = (10000 - 15) / (32154 - 6430)
        intercept = 15 - slope * 6430


        # Convert the voltage to pressure
        pressure = slope * raw_adc + intercept

        return pressure

    def writeData(self, registerAddress, data):
        try:
            self.bus.write_i2c_block_data(self.deviceAddress, registerAddress, data)
        except IOError as e:
            print(f"Error writing I2C data: {e}")