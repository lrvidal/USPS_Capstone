import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from DataProvider import DataProvider
import socket


### I2C BUS NUMBERS ###
I2C_BUS = '/dev/i2c-0'

### Pressure Transducer Current Loop  I2C ###
LOOP_DEVICE_ADDRESS = 0x48
LOOP_REGISTER = 0x00
LOOP_DATA_LENGTH = 3

### Humidity Sensor I2C ###
AIR_TEMP_HUMIDITY_DEVICE_ADDRESS = 0x44
AIR_TEMP_HUMIDITY_REGISTER_ADDRESS = 0xE000
AIR_TEMP_HUMIDITY_DATA_LENGTH = 6

### Rogowsky Coil ModBus ###
ROGOWSKY_PORT = '/dev/serial0'
ROGOWSKY_PERIPHERAL_ADDRESS = 1
ROGOWSKY_PHASE_1_CURRENT_REGISTER = 0x3E8
ROGOWSKY_PHASE_2_CURRENT_REGISTER = 0x3EA
ROGOWSKY_PHASE_3_CURRENT_REGISTER = 0x3EC
ROGOWSKY_PHASE_1_VOLTAGE_REGISTER = 0x3F2
ROGOWSKY_PHASE_2_VOLTAGE_REGISTER = 0x3F4
ROGOWSKY_PHASE_3_VOLTAGE_REGISTER = 0x3F6
ROGOWSKY_PHASE_POWER_REGISTER = 0x40A
ROGOWSKY_PHASE_SEQUENCE_REGISTER = 0xDC

### SPI BUS NUMBER ###
SPI_BUS = 0

### Thermocouple SPIs ###
THERMO1_DEVICE = 0
THERMO2_DEVICE = 1

dataProvider = DataProvider(thermo1Bus=SPI_BUS, thermo1Device=THERMO1_DEVICE, thermo2Bus=SPI_BUS, thermo2Device=THERMO2_DEVICE)
UPDATE_DATA_TIME = 60000 # Time for updating data in milliseconds
class GUI:
    def __init__(self, window, notebook):
        self.window = window
        self.notebook = notebook
        self.air_tab = ttk.Frame(notebook)
        self.oil_tab = ttk.Frame(notebook)
        self.download_tab = ttk.Frame(notebook)
        self.phase_tab = ttk.Frame(notebook)

        notebook.add(self.phase_tab, text="Phase Electrical")
        notebook.add(self.oil_tab, text="Oil")
        notebook.add(self.air_tab, text="Air")
        notebook.add(self.download_tab, text="Download")

        self.phase_fig, self.phase_axs = plt.subplots(2, 2, figsize=(10, 10))
        self.phase_canvas = FigureCanvasTkAgg(self.phase_fig, master=self.phase_tab)

        self.oil_fig, self.oil_axs = plt.subplots(2, 2, figsize=(10, 10))
        self.oil_canvas = FigureCanvasTkAgg(self.oil_fig, master=self.oil_tab)

        self.air_fig, self.air_axs = plt.subplots(3, 2, figsize=(10, 10))
        self.air_canvas = FigureCanvasTkAgg(self.air_fig, master=self.air_tab)


        self.toottip = ttk.Label(self.download_tab, text="Enter IP Address of the computer to download the data to")
        self.toottip.pack()
        self.ip_entry = tk.Entry(self.download_tab)
        self.ip_entry.pack()
        self.button = tk.Button(self.download_tab, text="Download Trends as CSV", command=self.fileDownload)
        self.button.pack()


    def fileDownload(self):
        ip = self.ip_entry.get()
        PORT_NUMBER = 5000
        try:
            # Create a socket
            s = socket.socket()

            # Connect to the receiver
            s.connect((ip, PORT_NUMBER))

            # Open the file in binary mode
            with open("data.csv", "rb") as f:
                # Read the file and send it over the socket
                while (data := f.read(1024)):
                    s.send(data)

            # Close the socket
            s.close()
        except Exception as e:
            print("Connection Failed: ", e)

    def displayData(self):

        # Add the tabs to the notebook
        self.notebook.add(self.phase_tab, text="Phase Electrical")
        self.notebook.add(self.oil_tab, text="Oil")
        self.notebook.add(self.air_tab, text="Air")

        # Plot phase trends in the phase tab
        self.updatePhaseTrends()
        self.phase_fig.tight_layout()
        self.phase_canvas.draw()
        self.phase_canvas.get_tk_widget().pack()

        # Plot oil temperature trends in the oil tab
        self.updateOilTemperatures()

        # Plot water level sensor status in the oil tab
        self.updateWaterLevelStatus()

        # Adjust spacing between subplots in the oil tab
        self.oil_fig.tight_layout()

        # Create a label to display the oil figure in the oil tab
        self.oil_canvas.draw()
        self.oil_canvas.get_tk_widget().pack()

        # Plot current air pressure in the air tab
        self.updateCurrentAirPressure()

        # Plot air pressure trend in the air tab
        self.updateAirPressureTrend()

        # Plot current air humidity in the air tab
        self.updateCurrentAirHumidity()

        # Plot air humidity trend in the air tab
        self.updateAirHumidityTrend()

        # Plot current air temperature in the air tab
        self.updateCurrentAirTemperature()

        # Plot air temperature trend in the air tab
        self.updateAirTemperatureTrend()

        # Adjust spacing between subplots in the air tab
        self.air_fig.tight_layout()


        self.air_canvas.draw()
        self.air_canvas.get_tk_widget().pack()

        # Pack the notebook widget
        self.notebook.pack()
        # Run the GUI event loop

        self.window.after(UPDATE_DATA_TIME, self.updateData)
        self.window.mainloop()

    def updateData(self):
        dataProvider.updateDataCSV()

        self.updateCurrentAirPressure()
        self.updateAirPressureTrend()
        self.updateCurrentAirHumidity()
        self.updateAirHumidityTrend()
        self.updateCurrentAirTemperature()
        self.updateAirTemperatureTrend()
        self.updateOilTemperatures()
        self.updateWaterLevelStatus()
        self.updatePhaseTrends()

        self.window.after(UPDATE_DATA_TIME, self.updateData)

    def updateAirHumidityTrend(self):
        self.air_axs[1, 1].cla()
        self.air_axs[1, 1].plot(dataProvider.getTimeArray(), dataProvider.getAirHumidityTrend())
        self.air_axs[1, 1].set_title("Air Humidity Trend")
        self.air_axs[1, 1].xaxis.set_major_locator(MaxNLocator(nbins=6))
        self.air_canvas.draw()

    def updateCurrentAirHumidity(self):
        airHumidityColor = "red" if isMeasurementConcerning("Air Humidity", dataProvider.getCurrentAirHumidity()) else "black"
        self.air_axs[1, 0].cla()
        self.air_axs[1, 0].set_title("Current Air Humidity")
        self.air_axs[1, 0].set_xticks([])
        self.air_axs[1, 0].set_yticks([])
        self.air_axs[1, 0].text(0.5, 0.5, str(dataProvider.getCurrentAirHumidity()) + " %RH", fontsize=35, ha='center', color=airHumidityColor)
        self.air_canvas.draw()

    def updateAirPressureTrend(self):
        self.air_axs[0, 1].cla()
        self.air_axs[0, 1].plot(dataProvider.getTimeArray(), dataProvider.getAirPressureTrend())
        self.air_axs[0, 1].set_title("Air Pressure Trend")
        self.air_axs[0, 1].xaxis.set_major_locator(MaxNLocator(nbins=6))
        self.air_canvas.draw()

    def updateCurrentAirPressure(self):
        airPressureColor = "red" if isMeasurementConcerning("Air Pressure", dataProvider.getCurrentAirPressure()) else "black"
        self.air_axs[0, 0].cla()
        self.air_axs[0, 0].set_title("Current Air Pressure")
        self.air_axs[0, 0].set_xticks([])
        self.air_axs[0, 0].set_yticks([])
        self.air_axs[0, 0].text(0.5, 0.5, str(dataProvider.getCurrentAirPressure()) + " psi", fontsize=35, ha='center', color=airPressureColor)
        self.air_canvas.draw()
    
    def updateAirTemperatureTrend(self):
        self.air_axs[2, 1].cla()
        self.air_axs[2, 1].plot(dataProvider.getTimeArray(), dataProvider.getAirTemperatureTrend())
        self.air_axs[2, 1].set_title("Air Temperature Trend")
        self.air_axs[2, 1].xaxis.set_major_locator(MaxNLocator(nbins=6))
        self.air_canvas.draw()

    def updateCurrentAirTemperature(self):
        airTempColor = "red" if isMeasurementConcerning("Air Temperature", dataProvider.getCurrentAirTemperature()) else "black"
        self.air_axs[2, 0].cla()
        self.air_axs[2, 0].set_title("Current Air Temperature")
        self.air_axs[2, 0].set_xticks([])
        self.air_axs[2, 0].set_yticks([])
        self.air_axs[2, 0].text(0.5, 0.5, str(dataProvider.getCurrentAirTemperature()) + " °F", fontsize=35, ha='center', color=airTempColor)
        self.air_canvas.draw()

    def updatePhaseTrends(self):
        self.phase_axs[0, 0].cla()
        self.phase_axs[1, 1].cla()
        self.phase_axs[1, 0].cla()
        phaseVoltage, phaseCurrent = dataProvider.getPhaseTrends()

        phaseStatus = dataProvider.getPhaseStatus()
        phaseStatusColor = "black" if phaseStatus == 0 else "red"
        phaseStatusMessages = {
            0: "All Clear",
            1: "Voltage Sequence wrong, Current Sequence normal",
            2: "Voltage Sequence norman, Current Sequence wrong",
            3: "Voltage Sequence wrong, Current Sequence wrong"
        }

        self.phase_axs[0, 0].cla()
        self.phase_axs[0, 0].set_title("Current Status")
        self.phase_axs[0, 0].set_xticks([])
        self.phase_axs[0, 0].set_yticks([])
        self.phase_axs[0, 0].text(0.5, 0.5, phaseStatusMessages[phaseStatus], fontsize=35, ha='center', color=phaseStatusColor)
        self.phase_canvas.draw()

        for i in range(3):
            self.phase_axs[1, 1].plot(dataProvider.getTimeArray(), phaseVoltage[i], label=f"Phase {i+1}")
            self.phase_axs[1, 0].plot(dataProvider.getTimeArray(), phaseCurrent[i], label=f"Phase {i+1}")

        self.phase_axs[1, 1].set_title("Phase Voltage")
        self.phase_axs[1, 1].legend()
        self.phase_axs[1, 1].xaxis.set_major_locator(MaxNLocator(nbins=6))

        self.phase_axs[1, 0].set_title("Phase Current")
        self.phase_axs[1, 0].legend()
        self.phase_axs[1, 0].xaxis.set_major_locator(MaxNLocator(nbins=6))
        self.phase_canvas.draw()

    def updateOilTemperatures(self):
        self.oil_axs[1, 0].cla()
        firstTempTrend, secondTempTrend = dataProvider.getOilTemperaturesTrends()
        self.oil_axs[1, 0].set_title("Oil Temperature Trend")
        self.oil_axs[1, 0].plot(dataProvider.getTimeArray(), firstTempTrend, label="First Oil Temperature")
        self.oil_axs[1, 0].plot(dataProvider.getTimeArray(), secondTempTrend, label="Second Oil Temperature")
        self.oil_axs[1, 0].legend()
        self.oil_axs[1, 0].xaxis.set_major_locator(MaxNLocator(nbins=6))

        firstOilColor = "red" if isMeasurementConcerning("Oil Temperature", firstTempTrend[-1]) else "black"
        self.oil_axs[0, 0].cla()
        self.oil_axs[0, 0].set_title("Current First Oil Temperature")
        self.oil_axs[0, 0].set_xticks([])
        self.oil_axs[0, 0].set_yticks([])
        self.oil_axs[0, 0].text(0.5, 0.5, str(firstTempTrend[-1]) + " °F", fontsize=35, ha='center', color=firstOilColor)

        secondOilColor = "red" if isMeasurementConcerning("Oil Temperature", secondTempTrend[-1]) else "black"
        self.oil_axs[0, 1].cla()
        self.oil_axs[0, 1].set_title("Current Second Oil Temperature")
        self.oil_axs[0, 1].set_xticks([])
        self.oil_axs[0, 1].set_yticks([])
        self.oil_axs[0, 1].text(0.5, 0.5, str(secondTempTrend[-1]) + " °F", fontsize=35, ha='center', color=secondOilColor)
        self.oil_canvas.draw()

    def updateWaterLevelStatus(self):
        waterLevelStatus = dataProvider.getWaterLevelStatus()
        waterLevelColor = "black" if waterLevelStatus == 0 else "red"
        waterLevelMessages = {
            0: "Normal",
            1: "Check Water Tank"
        }
        self.oil_axs[1, 1].cla()
        self.oil_axs[1, 1].set_title("Water Level Sensor Status")
        self.oil_axs[1, 1].set_xticks([])
        self.oil_axs[1, 1].set_yticks([])
        self.oil_axs[1, 1].text(0.5, 0.5, waterLevelMessages, fontsize=35, ha='center', color=waterLevelColor)
        self.oil_canvas.draw()
## CONSTANTS ZONE ##
# these constants are used to determine if a measurement is concerning, making the text red on the GUI 
OIL_TEMP_CONCERNING = 300
AIR_PRESSURE_CONCERNING = 132
AIR_HUMIDITY_CONCERNING = 50
AIR_TEMP_CONCERNING = 212
CONCERNING_PARAMS = {
    "Oil Temperature": OIL_TEMP_CONCERNING,
    "Air Pressure": AIR_PRESSURE_CONCERNING,
    "Air Humidity": AIR_HUMIDITY_CONCERNING,
    "Air Temperature": AIR_TEMP_CONCERNING
}
def isMeasurementConcerning(type, value):
    return value > CONCERNING_PARAMS[type]

window = tk.Tk()
window.title("DUS Monitoring System")
#window.iconbitmap('./USPS.ico')
notebook = ttk.Notebook(window)
gui = GUI(window=window, notebook=notebook)

dataProvider.updateDataCSV()
gui.displayData()