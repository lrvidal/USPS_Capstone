import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.pyplot as plt
from DataProvider import DataProvider

dataProvider = DataProvider()

class GUI:
    def __init__(self, window, notebook):
        self.window = window
        self.notebook = notebook
        self.dataProvider = DataProvider()
        self.electrical_tab = ttk.Frame(notebook)
        self.air_tab = ttk.Frame(notebook)
        self.oil_tab = ttk.Frame(notebook)
        self.download_tab = ttk.Frame(notebook)

        notebook.add(self.electrical_tab, text="Electrical")
        notebook.add(self.oil_tab, text="Oil")
        notebook.add(self.air_tab, text="Air")
        notebook.add(self.download_tab, text="Download")

        self.electrical_fig, self.electrical_axs = plt.subplots(3, 2, figsize=(10, 10))
        self.electrical_canvas = FigureCanvasTkAgg(self.electrical_fig, master=self.electrical_tab)

        self.oil_fig, self.oil_axs = plt.subplots(1, 2, figsize=(10, 5))
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
        return

    def displayData(self):
        # TODO: Replace this with your own data retrieval logic

        lossOfPressure = [0.5, 0.3, 0.2, 0.4, 0.1]
        oilSystemConditions = ["Normal", "Normal", "Abnormal", "Normal", "Abnormal"]

        # Add the tabs to the notebook
        self.notebook.add(self.electrical_tab, text="Electrical")
        self.notebook.add(self.oil_tab, text="Oil")
        self.notebook.add(self.air_tab, text="Air")

        # Plot voltage in the electrical tab
        self.updateElectricalAttributes()
        self.updatePhaseTrends()
        # Adjust spacing between subplots in the electrical tab
        self.electrical_fig.tight_layout()

        self.electrical_canvas.draw()
        self.electrical_canvas.get_tk_widget().pack()

        # Plot loss of pressure over time in the oil tab
        self.oil_axs[0].plot(lossOfPressure)
        self.oil_axs[0].set_title("Loss of Pressure")

        # Plot oil system conditions in the oil tab
        self.oil_axs[1].plot(oilSystemConditions)
        self.oil_axs[1].set_title("Oil System Conditions")

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

        self.window.after(3000, self.updateData) #FIXME: time interval for updating data is hardcoded
        self.window.mainloop()

    def updateData(self):
        self.updateCurrentAirPressure()
        self.updateAirPressureTrend()
        self.updateCurrentAirHumidity()
        self.updateAirHumidityTrend()
        self.updateCurrentAirTemperature()
        self.updateAirTemperatureTrend()
        self.updateElectricalAttributes()
        self.updatePhaseTrends()

        self.window.after(3000, self.updateData) #FIXME: time interval for updating data is hardcoded

    def updateAirHumidityTrend(self):
        self.air_axs[1, 1].cla()
        self.air_axs[1, 1].plot(dataProvider.getAirHumidityTrend())
        self.air_axs[1, 1].set_title("Air Humidity Trend")
        self.air_canvas.draw()

    def updateCurrentAirHumidity(self):
        self.air_axs[1, 0].cla()
        self.air_axs[1, 0].set_title("Current Air Humidity")
        self.air_axs[1, 0].set_xticks([])
        self.air_axs[1, 0].set_yticks([])
        self.air_axs[1, 0].text(0.5, 0.5, str(dataProvider.getCurrentAirHumidity()) + " %RH", fontsize=35, ha='center')
        self.air_canvas.draw()

    def updateAirPressureTrend(self):
        self.air_axs[0, 1].cla()
        self.air_axs[0, 1].plot(dataProvider.getAirPressureTrend())
        self.air_axs[0, 1].set_title("Air Pressure Trend")
        self.air_canvas.draw()

    def updateCurrentAirPressure(self):
        self.air_axs[0, 0].cla()
        self.air_axs[0, 0].set_title("Current Air Pressure")
        self.air_axs[0, 0].set_xticks([])
        self.air_axs[0, 0].set_yticks([])
        self.air_axs[0, 0].text(0.5, 0.5, str(dataProvider.getCurrentAirPressure()) + " psi", fontsize=35, ha='center')
        self.air_canvas.draw()
    
    def updateAirTemperatureTrend(self):
        self.air_axs[2, 1].cla()
        self.air_axs[2, 1].plot(dataProvider.getAirTemperatureTrend())
        self.air_axs[2, 1].set_title("Air Temperature Trend")
        self.air_canvas.draw()

    def updateCurrentAirTemperature(self):
        self.air_axs[2, 0].cla()
        self.air_axs[2, 0].set_title("Current Air Temperature")
        self.air_axs[2, 0].set_xticks([])
        self.air_axs[2, 0].set_yticks([])
        self.air_axs[2, 0].text(0.5, 0.5, str(dataProvider.getCurrentAirTemperature()) + " °F", fontsize=35, ha='center')
        self.air_canvas.draw()

    def updateElectricalAttributes(self):
        voltage, current, power = dataProvider.getElectricalAttributes()

        self.electrical_axs[0, 0].cla()
        self.electrical_axs[0, 0].set_title("Current Voltage")
        self.electrical_axs[0, 0].set_xticks([])
        self.electrical_axs[0, 0].set_yticks([])
        self.electrical_axs[0, 0].text(0.5, 0.5, str(voltage) + " V", fontsize=35, ha='center')

        self.electrical_axs[0, 1].cla()
        self.electrical_axs[0, 1].set_title("Current Current")
        self.electrical_axs[0, 1].set_xticks([])
        self.electrical_axs[0, 1].set_yticks([])
        self.electrical_axs[0, 1].text(0.5, 0.5, str(current) + " A", fontsize=35, ha='center')

        self.electrical_axs[1, 0].cla()
        self.electrical_axs[1, 0].set_title("Current Power")
        self.electrical_axs[1, 0].set_xticks([])
        self.electrical_axs[1, 0].set_yticks([])
        self.electrical_axs[1, 0].text(0.5, 0.5, str(power) + " kW", fontsize=35, ha='center')

        self.electrical_canvas.draw()

    def updatePhaseTrends(self):
        self.electrical_axs[1, 1].cla()
        self.electrical_axs[2, 0].cla()
        phaseVoltage, phaseCurrent = dataProvider.getPhaseTrends()

        for i in range(3):
            self.electrical_axs[1, 1].plot(phaseVoltage[i], label=f"Phase {i+1}")
            self.electrical_axs[2, 0].plot(phaseCurrent[i], label=f"Phase {i+1}")

        self.electrical_axs[1, 1].set_title("Phase Voltage")
        self.electrical_axs[1, 1].legend()

        self.electrical_axs[2, 0].set_title("Phase Current")
        self.electrical_axs[2, 0].legend()

window = tk.Tk()
notebook = ttk.Notebook(window)
gui = GUI(window=window, notebook=notebook)

gui.displayData()