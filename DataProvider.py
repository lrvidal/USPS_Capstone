class DataProvider:
    _airPressureTrend = [0]
    _airHumidityTrend = [0]
    _airTemperatureTrend = [0]
    _voltage = 0
    _current = 0
    _power = 0
    _phaseVoltageTrend = [[0], [0], [0]]
    _phaseCurrentTrend = [[0], [0], [0]]

    def getCurrentAirPressure(self):
        #TODO: implement SPI interfacing to acquire data
        currentPressure = self._airPressureTrend[-1] + 2 #FIXME: this is not real data

        self._airPressureTrend.append(currentPressure)
        return self._airPressureTrend[-1]
    
    def getAirPressureTrend(self):
        return self._airPressureTrend
    
    def getCurrentAirHumidity(self):
        #TODO: implement SPI interfacing to acquire data
        currentHumidity = self._airHumidityTrend[-1] + 5 #FIXME: this is not real data

        self._airHumidityTrend.append(currentHumidity)
        return self._airHumidityTrend[-1]
    
    def getAirHumidityTrend(self):
        return self._airHumidityTrend
    
    def getCurrentAirTemperature(self):
        #TODO: implement SPI interfacing to acquire data
        currentTemperature = self._airTemperatureTrend[-1] + 1.5 #FIXME: this is not real data

        self._airTemperatureTrend.append(currentTemperature)
        return self._airTemperatureTrend[-1]
    
    def getAirTemperatureTrend(self):
        return self._airTemperatureTrend
    
    def getElectricalAttributes(self):
        #TODO: implement SPI interfacing to acquire data
        self._voltage += 1
        self._current += 0.2
        self._power += 10

        currentPhaseVoltage1 = self._phaseVoltageTrend[0][-1] + 1
        currentPhaseCurrent1 = self._phaseCurrentTrend[0][-1] + 1
        currentPhaseVoltage2 = self._phaseVoltageTrend[1][-1] + 2
        currentPhaseCurrent2 = self._phaseCurrentTrend[1][-1] + 2
        currentPhaseVoltage3 = self._phaseVoltageTrend[2][-1] + 3
        currentPhaseCurrent3 = self._phaseCurrentTrend[2][-1] + 3

        self._phaseVoltageTrend[0].append(currentPhaseVoltage1)
        self._phaseCurrentTrend[0].append(currentPhaseCurrent1)
        self._phaseVoltageTrend[1].append(currentPhaseVoltage2)
        self._phaseCurrentTrend[1].append(currentPhaseCurrent2)
        self._phaseVoltageTrend[2].append(currentPhaseVoltage3)
        self._phaseCurrentTrend[2].append(currentPhaseCurrent3)

        return self._voltage, self._current, self._power
    
    def getPhaseTrends(self):
        return self._phaseVoltageTrend, self._phaseCurrentTrend