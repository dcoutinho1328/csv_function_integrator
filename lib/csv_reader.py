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
        print(file)
        #try:
        self.__name = file.split('/')[-1].replace('.csv', '')
        csvFile = open(file, 'r')
        self.__reader = []
        for line in csv.reader(csvFile, dialect='excel'):
            self.__reader.append(line)
        csvFile.close()
        #except:
        #raise self.__readingError
        self.__populateFields()

    def __populateFields(self):

        #Gets graph x unit
        try:
            self.__xUnit = self.__reader[1][0]
        except:
            raise self.__getInfoError('a unidade do eixo x')

        #Gets graph y1 unit
        try:
            self.__y1Unit = self.__reader[1][1]
        except:
            raise self.__getInfoError('a unidade do eixo y1')

        #Gets graph y2 unit
        try:
            self.__y2Unit = self.__reader[1][2]
        except:
            raise self.__getInfoError('a unidade do eixo y2')

        #Get points
        try:
            self.__points = []
            self.__xValues = []
            self.__y1Values = []
            self.__y2Values = []
            xOffset = float(self.__reader[2][0])
            length = int(len(self.__reader[2:]))
            for line in self.__reader[16:length]:
                x = float(line[0]) - xOffset               
                y1 = float(line[1])
                y2 = float(line[2])
                self.__xValues.append(x)
                self.__y1Values.append(y1)
                self.__y2Values.append(y2)
                self.__points.append((x,y1,y2))
        except:
            raise self.__getInfoError('os pontos')

        #GetMaxValues
        try:
            self.__max1value = max(self.__y1Values)
            self.__max2value = max(self.__y2Values)
        except:
            raise self.__getInfoError('os máximos')

    def getGraphName(self):
        return self.__name

    def getAxisUnit(self, axis='x'):
        if str(axis.lower()) == 'x':
            return self.__xUnit
        elif str(axis.lower()) == 'y1':
            return self.__y1Unit
        elif str(axis.lower()) == 'y2':
            return self.__y2Unit
        else:
            raise self.__invalidAxis

    def getPoints(self):
        return self.__points

    def buildFunction1Graph(self):
        try:
            self.__graph.clf()
            self.__graph.plot(self.__xValues, self.__y1Values, '-r', label='Samples')
            self.__graph.title(self.__name)
            self.__graph.xlabel(f'[{self.__xUnit}]')
            self.__graph.ylabel(f'[{self.__y1Unit}]')
        except:
            raise self.__graphError('construir')
    
    def buildFunction2Graph(self):
        try:
            self.__graph.clf()
            self.__graph.plot(self.__xValues, self.__y2Values, '-r', label='Samples')
            self.__graph.title(self.__name)
            self.__graph.xlabel(f'[{self.__xUnit}]')
            self.__graph.ylabel(f'[{self.__y2Unit}]')
        except:
            raise self.__graphError('construir')
    
    def buildComparationGraph(self):
        try:
            self.__graph.clf()
            fig, ax = self.__graph.subplots()
            ax.plot(self.__xValues, self.__y1Values, '-r', label='F1')
            ax.set_ylabel(f'Function 1 [{self.__y1Unit}]', color='red')
            ax2 = ax.twinx()
            ax2.plot(self.__xValues, self.__y2Values, '-b', label='F2')
            ax2.set_ylabel(f'Function 2 [{self.__y2Unit}]', color='blue')
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

    def getF1PeakValue(self):
        return self.__max1value

    def getF2ValueOnF1Peak(self):
        for point in self.__points:
            if point[1] == self.__max1value:
                return point[2]
        return 0