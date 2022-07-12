from typing import List
import PySimpleGUI as sg
from lib.csv_reader import GraphCSV
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from os import listdir

sg.theme('Topanga')

def getSamplesList():
    files = listdir('./scopes')
    def getScopes(file):
        return file.startswith('scope_') and file.endswith('.csv')
    return list(filter(getScopes, files))

layout = [[sg.T('Choose CSV file')],
          [sg.Combo(getSamplesList(),text_color='#E7C855', key='-DD-'), sg.B('Choose', key='-CHOOSE-')],
          [sg.T('F1 Max Value:', font=('Helvetica', 15), size=(12, 0)), sg.T('', justification='left', key='-F1MAX-', font=('Helvetica', 15)),
          sg.T('   |   ', font=('Helvetica', 15)),
          sg.T('F2 Value:', font=('Helvetica', 15), size=(8, 0)), sg.T('', key='-F2V-', font=('Helvetica', 15))],
          [sg.Canvas(key='-CANVAS-', size=(650,480))],
          [sg.B('Function 1', key='-FUNCTION1-'), sg.B('Function 2', key='-FUNCTION2-'), sg.B('Compare', key='-COMPARE-')]]

window = sg.Window('Graph Integrator', layout, icon='./assets/graph.ico', element_justification='center')

def drawFigure(canvas, figure):
    fc = FigureCanvasTkAgg(figure, canvas)
    fc.draw()
    fc.get_tk_widget().pack(side='top', fill='both', expand=1)
    return fc

graphInfo = None
figureCanvas = None
channel = None
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '-CHOOSE-':
        file = values['-DD-']
        path = f'./scopes/{file}'
        graphInfo = GraphCSV(path)
        graphInfo.buildFunction1Graph()
        graph = graphInfo.exportGraph()
        if(figureCanvas):
                figureCanvas.get_tk_widget().forget()
        figureCanvas = drawFigure(window['-CANVAS-'].TKCanvas, graph)
        peak = graphInfo.getF1PeakValue()
        unit1 = graphInfo.getAxisUnit('y1')
        unit2 = graphInfo.getAxisUnit('y2')
        f2Value = graphInfo.getF2ValueOnF1Peak()
        window['-F1MAX-'].update(f'{peak:.2f} {unit1}')
        window['-F2V-'].update(f'{f2Value:.2f} {unit2}')

    if event == '-FUNCTION1-':
        if graphInfo != None:
            graphInfo.buildFunction1Graph()
            graph = graphInfo.exportGraph()
            figureCanvas.get_tk_widget().forget()
            figureCanvas = drawFigure(window['-CANVAS-'].TKCanvas, graph)
    
    if event == '-FUNCTION2-':
        if graphInfo != None:
            graphInfo.buildFunction2Graph()
            graph = graphInfo.exportGraph()
            figureCanvas.get_tk_widget().forget()
            figureCanvas = drawFigure(window['-CANVAS-'].TKCanvas, graph)

    if event == '-COMPARE-':
        if graphInfo != None:
            graphInfo.buildComparationGraph()
            graph = graphInfo.exportGraph()
            figureCanvas.get_tk_widget().forget()
            figureCanvas = drawFigure(window['-CANVAS-'].TKCanvas, graph)

window.close()