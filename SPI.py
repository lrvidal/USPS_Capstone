import spidev

class SPIDevice:
    def __init__(self, bus, device):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1000000  # Set SPI clock speed (1 MHz)

    def transfer(self, data):
        return self.spi.xfer2(data)

    def read_data(self, length):
        return self.spi.readbytes(length)

    def close(self):
        self.spi.close()