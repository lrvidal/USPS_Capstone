import spidev

class SPIDevice:
    def __init__(self, bus, device):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1000000  # Set SPI clock speed (1 MHz)
        self.slope = (100 - 0) / (86.75 - 3)  # Calculate the slope
        self.intercept = 0 - self.slope * 3  # Calculate the intercept

    def transfer(self, data):
        return self.spi.xfer2(data)

    def read_data(self, length):
        # Send a dummy byte to read 32-bit data from TC1
        response = self.spi.xfer2([0x00, 0x00, 0x00, 0x00])
        # Combine the response bytes into one 32-bit value
        raw_data = response[0] << 24 | response[1] << 16 | response[2] << 8 | response[3]
        
        # Check if there are any errors
        if (raw_data & 0x7):
            print("Error reading thermocouple {} data.".format(self.device + 1))
            return None
        
        # Extract the temperature data (first 14 bits of the second word)
        value = raw_data >> 18
        if value & 0x2000:  # Check if negative
            value -= 0x4000
        
        # Convert to Celsius
        temp_celsius = value * 0.25

        # Normalize the temperature
        temp_celsius = self.slope * temp_celsius + self.intercept

        return temp_celsius

    def close(self):
        self.spi.close()