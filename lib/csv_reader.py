import csv
import matplotlib.pyplot as plt
from scipy import integrate

class GraphCSV():

    __graph = plt
    __integral = []

    __readingError = Exception('Arquivo inexistente ou não é csv\n')
    __getInfoError = lambda self, info: Exception(f'Não foi possível obter {info} do gráfico\nVerifique o conteúdo do seu arquivo CSV')
    __invalidAxis = Exception('Valor inválido para o eixo')
    __graphError = lambda self, operation: Exception(f'Não foi possível {operation} o gráfico')
    __integrationError = Exception('Não foi possível calcular a integral')

    def __init__(self, file):
        try:
            csvFile = open(file, 'r')
            self.__reader = []
            for line in csv.reader(csvFile, dialect='excel'):
                self.__reader.append(line)
            csvFile.close()
        except:
            raise self.__readingError
        self.__populateFields()

    def __populateFields(self):
        #Gets graph name
        try:
            self.__name = self.__reader[6][1]
        except:
            raise self.__getInfoError('o nome')

        #Gets graph x unit
        try:
            self.__xUnit = self.__reader[10][1]
        except:
            raise self.__getInfoError('a unidade do eixo x')

        #Gets graph y unit
        try:
            self.__yUnit = self.__reader[7][1]
        except:
            raise self.__getInfoError('a unidade do eixo y')

        #Gets graph y offset
        try:
            self.__yOffset = float(self.__reader[9][1])
        except:
            raise self.__getInfoError('a unidade do eixo y')

        #Get points
        try:
          self.__points = []
          self.__xValues = []
          self.__yValues = []
          xOffset = float(self.__reader[19][3])
          for line in self.__reader[19:-1]:
              x = float(line[3]) - xOffset
              y = float(line[4]) - self.__yOffset
              self.__xValues.append(x)
              self.__yValues.append(y)
              self.__points.append((x,y))
        except:
            raise self.__getInfoError('os pontos')

    def getGraphName(self):
        return self.__name

    def getAxisUnit(self, axis='x'):
        if str(axis.lower()) == 'x':
            return self.__xUnit
        elif str(axis.lower()) == 'y':
            return self.__yUnit
        else:
            raise self.__invalidAxis

    def getPoints(self):
        return self.__points

    def buildFunctionGraph(self):
        try:
            self.__graph.clf()
            self.__graph.plot(self.__xValues, self.__yValues, '-r', label='Samples')
            self.__graph.title(self.__name)
            self.__graph.xlabel(f'[{self.__xUnit}]')
            self.__graph.ylabel(f'[{self.__yUnit}]')
        except:
            raise self.__graphError('construir')

    def buildIntegralGraph(self):
        if len(self.__integral) == 0:
            self.__integrate()
        try:
            self.__graph.clf()
            self.__graph.plot(self.__xValues, self.__integral, '-b', label='Integral')
            self.__graph.title(f'Integral {self.__name}')
            self.__graph.xlabel(f'[{self.__xUnit}]')
        except:
            raise self.__graphError('construir')
    
    def buildComparationGraph(self):
        if len(self.__integral) == 0:
            self.__integrate()
        try:
            self.__graph.clf()
            fig, ax = self.__graph.subplots()
            ax.plot(self.__xValues, self.__yValues, '-r', label='Samples')
            ax.set_ylabel(f'Function [{self.__yUnit}]', color='red')
            ax2 = ax.twinx()
            ax2.plot(self.__xValues, self.__integral, '-b', label='Integral')
            ax2.set_ylabel('Integral', color='blue')
            self.__graph.title(f'Comparation {self.__name}')
            self.__graph.xlabel(f'[{self.__xUnit}]')
        except:
            raise self.__graphError('construir')


    def showGraph(self):
        try:
            self.__graph.show()
        except:
            raise self.__graphError('exibir')
    
    def exportGraph(self):
        try:
            return self.__graph.gcf()
        except:
            raise self.__graphError('exportar')

    def __integrate(self):
        try:
            self.__integral = integrate.cumulative_trapezoid(self.__yValues, self.__xValues, initial=0)
        except:
            raise self.__integrationError

    def getPeakValue(self):
        return max(self.__yValues)