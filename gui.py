import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.pyplot as plt

def displayData():
    # TODO: Replace this with your own data retrieval logic
    lossOfPressure = [0.5, 0.3, 0.2, 0.4, 0.1]
    timeToReachPressure = [10, 15, 20, 25, 30]
    airQuality = ["Good", "Good", "Poor", "Good", "Poor"]
    oilSystemConditions = ["Normal", "Normal", "Abnormal", "Normal", "Abnormal"]

    voltage = [[220, 225, 230, 235, 240], [200, 220, 225, 230, 235], [190, 215, 220, 225, 230]]
    current = [[1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [1, 5, 1, 5, 1]]
    power = [[2200, 2205, 2300, 2305, 2400], [2000, 2200, 2025, 2300, 2305], [1900, 2150, 2200, 2025, 2300]]
    phaseVoltage = [[220, 225, 230, 235, 240], [200, 220, 225, 230, 235], [190, 215, 220, 225, 230]]
    phaseCurrent = [[1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [1, 5, 1, 5, 1]]

    # Create a new window
    window = tk.Tk()

    # Create a notebook widget to hold the tabs
    notebook = ttk.Notebook(window)

    # Create tabs for electrical, oil, and air
    electrical_tab = ttk.Frame(notebook)
    oil_tab = ttk.Frame(notebook)
    air_tab = ttk.Frame(notebook)

    # Add the tabs to the notebook
    notebook.add(electrical_tab, text="Electrical")
    notebook.add(oil_tab, text="Oil")
    notebook.add(air_tab, text="Air")

    # Create a figure and subplots for each data in the electrical tab
    electrical_fig, electrical_axs = plt.subplots(3, 2, figsize=(10, 10))

    # Plot voltage in the electrical tab
    for i in range(3):
        electrical_axs[0, 0].plot(voltage[i], label=f"Phase {i+1}")
        electrical_axs[0, 1].plot(current[i], label=f"Phase {i+1}")
        electrical_axs[1, 0].plot(power[i], label=f"Phase {i+1}")
        electrical_axs[1, 1].plot(phaseVoltage[i], label=f"Phase {i+1}")
        electrical_axs[2, 0].plot(phaseCurrent[i], label=f"Phase {i+1}")

    electrical_axs[0, 0].set_title("Voltage")
    electrical_axs[0, 0].legend()

    electrical_axs[0, 1].set_title("Current")
    electrical_axs[0, 1].legend()

    electrical_axs[1, 0].set_title("Power")
    electrical_axs[1, 0].legend()

    electrical_axs[1, 1].set_title("Phase Voltage")
    electrical_axs[1, 1].legend()

    electrical_axs[2, 0].set_title("Phase Current")
    electrical_axs[2, 0].legend()

    # Adjust spacing between subplots in the electrical tab
    electrical_fig.tight_layout()

    # Create a label to display the electrical figure in the electrical tab
    electrical_canvas = FigureCanvasTkAgg(electrical_fig, master=electrical_tab)
    electrical_canvas.draw()
    electrical_canvas.get_tk_widget().pack()

    # Create a figure and subplots for each data in the oil tab
    oil_fig, oil_axs = plt.subplots(1, 2, figsize=(10, 5))

    # Plot loss of pressure over time in the oil tab
    oil_axs[0].plot(lossOfPressure)
    oil_axs[0].set_title("Loss of Pressure")

    # Plot oil system conditions in the oil tab
    oil_axs[1].plot(oilSystemConditions)
    oil_axs[1].set_title("Oil System Conditions")

    # Adjust spacing between subplots in the oil tab
    oil_fig.tight_layout()

    # Create a label to display the oil figure in the oil tab
    oil_canvas = FigureCanvasTkAgg(oil_fig, master=oil_tab)
    oil_canvas.draw()
    oil_canvas.get_tk_widget().pack()

    # Create a figure and subplots for each data in the air tab
    air_fig, air_axs = plt.subplots(2, 1, figsize=(5, 10))

    # Plot time to reach operating pressure in the air tab
    air_axs[0].plot(timeToReachPressure)
    air_axs[0].set_title("Time to Reach Operating Pressure")

    # Plot air quality conditions in the air tab
    air_axs[1].plot(airQuality)
    air_axs[1].set_title("Air Quality")

    # Adjust spacing between subplots in the air tab
    air_fig.tight_layout()

    # Create a label to display the air figure in the air tab
    air_canvas = FigureCanvasTkAgg(air_fig, master=air_tab)
    air_canvas.draw()
    air_canvas.get_tk_widget().pack()

    # Pack the notebook widget
    notebook.pack()

    # Run the GUI event loop
    window.mainloop()

# Call the function to display the data
displayData()
