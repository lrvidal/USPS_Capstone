import ModBus
import SPI
import I2C
import csv
import datetime
import RPi.GPIO as GPIO

ROGOWSKY_PHASE_1_CURRENT_REGISTER = 1000
ROGOWSKY_PHASE_2_CURRENT_REGISTER = 1002
ROGOWSKY_PHASE_3_CURRENT_REGISTER = 1004
ROGOWSKY_PHASE_1_VOLTAGE_REGISTER = 1010
ROGOWSKY_PHASE_2_VOLTAGE_REGISTER = 1012
ROGOWSKY_PHASE_3_VOLTAGE_REGISTER = 1014
ROGOWSKY_PHASE_SEQUENCE_REGISTER = 220

ERROR_MESSAGE = "error\nreading\ndata"

class DataProvider:
    _airPressureTrend = []
    _airHumidityTrend = []
    _airTemperatureTrend = []
    _phaseVoltageTrend = [[], [], []]
    _phaseCurrentTrend = [[], [], []]
    _firstOilTemperatureTrend = []
    _secondOilTemperatureTrend = []
    _measurementsTime = []


    def __init__(
             self, 
             rogowskyPort, rogowskyAdress, 
             loopBus, loopDevice, 
             tempHumBus, tempHumDevice, 
             thermo1Bus, thermo1Device,
             thermo2Bus, thermo2Device
             ):
        
        self.rogowskyCoil = ModBus.ModBus(port=rogowskyPort, address=rogowskyAdress)
        self.currentLoop = I2C.I2C(busNumber=loopBus, deviceAddress=loopDevice)
        self.tempHumSensor = I2C.I2C(busNumber=tempHumBus, deviceAddress=tempHumDevice)
        self.thermo1 = SPI.SPIDevice(bus=thermo1Bus, device=thermo1Device)
        self.thermo2 = SPI.SPIDevice(bus=thermo2Bus, device=thermo2Device)

    def cToF(self, celsius):
        if celsius == None:
            return -999

        return celsius * 9/5 + 32

    def updateData(self):
        # If the length of any array is equal to the number of minutes in a day, erase the oldest entry to be replaced
        if len(self._airPressureTrend) >= 1440:
            self._airPressureTrend.pop(0)
            self._airHumidityTrend.pop(0)
            self._airTemperatureTrend.pop(0)
            self._firstOilTemperatureTrend.pop(0)
            self._secondOilTemperatureTrend.pop(0)
            self._phaseVoltageTrend[0].pop(0)
            self._phaseCurrentTrend[0].pop(0)
            self._phaseVoltageTrend[1].pop(0)
            self._phaseCurrentTrend[1].pop(0)
            self._phaseVoltageTrend[2].pop(0)
            self._phaseCurrentTrend[2].pop(0)
            self._measurementsTime.pop(0)


        # Time Section #
        current_time = datetime.datetime.now()
        min = current_time.minute if current_time.minute >= 10 else "0" + str(current_time.minute)
        self._measurementsTime.append("{0}:{1}".format(current_time.hour, min))

        # Air Section #
        try:
            currentPressure = self.currentLoop.read_pressure()
            self._airPressureTrend.append(currentPressure)
        except:
            self._airPressureTrend.append(ERROR_MESSAGE)

        try :
            currentTemperature, currentHumidity = self.tempHumSensor.read_sht30()
        except:
            currentTemperature = -999
            currentHumidity = -999
        
        self._airHumidityTrend.append(currentHumidity)
        self._airTemperatureTrend.append(self.cToF(currentTemperature))

        # Electrical Section #

        currentPhaseVoltage1 = self.rogowskyCoil.read_modbus_float(ROGOWSKY_PHASE_1_VOLTAGE_REGISTER) or ERROR_MESSAGE
        currentPhaseVoltage2 = self.rogowskyCoil.read_modbus_float(ROGOWSKY_PHASE_2_VOLTAGE_REGISTER) or ERROR_MESSAGE
        currentPhaseVoltage3 = self.rogowskyCoil.read_modbus_float(ROGOWSKY_PHASE_3_VOLTAGE_REGISTER) or ERROR_MESSAGE

        currentPhaseCurrent1 = self.rogowskyCoil.read_modbus_float(ROGOWSKY_PHASE_1_CURRENT_REGISTER) or ERROR_MESSAGE
        currentPhaseCurrent2 = self.rogowskyCoil.read_modbus_float(ROGOWSKY_PHASE_2_CURRENT_REGISTER) or ERROR_MESSAGE
        currentPhaseCurrent3 = self.rogowskyCoil.read_modbus_float(ROGOWSKY_PHASE_3_CURRENT_REGISTER) or ERROR_MESSAGE

        print("PHASE 1 VOLTAGE ", currentPhaseVoltage1)

        self._phaseVoltageTrend[0].append(currentPhaseVoltage1)
        self._phaseCurrentTrend[0].append(currentPhaseCurrent1)
        self._phaseVoltageTrend[1].append(currentPhaseVoltage2)
        self._phaseCurrentTrend[1].append(currentPhaseCurrent2)
        self._phaseVoltageTrend[2].append(currentPhaseVoltage3)
        self._phaseCurrentTrend[2].append(currentPhaseCurrent3)

        # Oil Section #
        oilOneRead = self.thermo1.read_data(length=4)
        currentFirstOilTemperature = self.cToF(oilOneRead)
        self._firstOilTemperatureTrend.append(currentFirstOilTemperature)

        oilTwoRead = self.thermo2.read_data(length=4)
        currentSecondOilTemperature = self.cToF(oilTwoRead)
        self._secondOilTemperatureTrend.append(currentSecondOilTemperature)

    def updateDataCSV(self):
        self.updateData()
        csvHeaders = ["Time", "Air Pressure", "Air Humidity", "Air Temperature", "First Oil Temperature", "Second Oil Temperature", "Phase 1 Voltage", "Phase 1 Current", "Phase 2 Voltage", "Phase 2 Current", "Phase 3 Voltage", "Phase 3 Current"]
        # Open the CSV file in append mode
        with open('data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(csvHeaders)
            for i in range(len(self._measurementsTime)):
                data = [
                    self._measurementsTime[i],
                    self._airPressureTrend[i],
                    self._airHumidityTrend[i],
                    self._airTemperatureTrend[i],
                    self._firstOilTemperatureTrend[i],
                    self._secondOilTemperatureTrend[i],
                    self._phaseVoltageTrend[0][i],
                    self._phaseCurrentTrend[0][i],
                    self._phaseVoltageTrend[1][i],
                    self._phaseCurrentTrend[1][i],
                    self._phaseVoltageTrend[2][i],
                    self._phaseCurrentTrend[2][i],
                ]
                # Write the data to the CSV file
                writer.writerow(data)
        
    def getCurrentOilTemperatures(self):
        return self._firstOilTemperatureTrend[-1], self._secondOilTemperatureTrend[-1]

    def getOilTemperaturesTrends(self):
        return self._firstOilTemperatureTrend, self._secondOilTemperatureTrend
        
    def getCurrentAirPressure(self):
        return self._airPressureTrend[-1]
    
    def getAirPressureTrend(self):
        return self._airPressureTrend
    
    def getCurrentAirHumidity(self):
        return self._airHumidityTrend[-1]
    
    def getAirHumidityTrend(self):
        return self._airHumidityTrend
    
    def getCurrentAirTemperature(self):
        return self._airTemperatureTrend[-1]
    
    def getAirTemperatureTrend(self):
        return self._airTemperatureTrend
    
    def getPhaseTrends(self):
        return self._phaseVoltageTrend, self._phaseCurrentTrend
    
    def getPhaseStatus(self):
        phaseStatus = self.rogowskyCoil.read_modbus_float(ROGOWSKY_PHASE_SEQUENCE_REGISTER)
        return phaseStatus
    
    def getWaterLevelStatus(self):

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.IN)

        if GPIO.input(18) == GPIO.HIGH:
            return 1
        else:
            return 0

    def getTimeArray(self):
        return self._measurementsTime