import PySimpleGUI as sg
from lib.csv_reader import GraphCSV
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sg.theme('Topanga')

layout = [[sg.T('Choose CSV file')],
          [sg.In(key='-FB-', readonly=True, text_color='#282923'), sg.FileBrowse()],
          [sg.B('Select', key='-SELECT-')],
          [sg.Canvas(key='-CANVAS-', size=(650,480))],
          [sg.B('Function', key='-FUNCTION-'), sg.B('Integral', key='-INTEGRATE-'), sg.B('Compare', key='-COMPARE-')]]

window = sg.Window('Graph Integrator', layout, icon='./assets/graph.ico', element_justification='center')

def drawFigure(canvas, figure):
    fc = FigureCanvasTkAgg(figure, canvas)
    fc.draw()
    fc.get_tk_widget().pack(side='top', fill='both', expand=1)
    return fc

graphInfo = None
figureCanvas = None
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '-SELECT-':
        graphInfo = GraphCSV(values['-FB-'])
        graphInfo.buildFunctionGraph()
        graph = graphInfo.exportGraph()
        if(figureCanvas):
            figureCanvas.get_tk_widget().forget()
        figureCanvas = drawFigure(window['-CANVAS-'].TKCanvas, graph)

    if event == '-FUNCTION-':
        if graphInfo != None:
            graphInfo.buildFunctionGraph()
            graph = graphInfo.exportGraph()
            figureCanvas.get_tk_widget().forget()
            figureCanvas = drawFigure(window['-CANVAS-'].TKCanvas, graph)

    if event == '-INTEGRATE-':
        if graphInfo != None:
            graphInfo.buildIntegralGraph()
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