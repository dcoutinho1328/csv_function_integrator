import PySimpleGUI as sg
from lib.csv_reader import GraphCSV
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sg.theme('Topanga')

layout = [[sg.T('Choose CSV file')],
          [sg.In(key='-FB-', readonly=True, text_color='#282923'), sg.FileBrowse()],
          [sg.T('Insert Channel:'), sg.In(key='-CH-', text_color='#282923', background_color='#ffffff', size=(10,1)), sg.B('Choose', key='-CHOOSE-')],
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
channel = None
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '-CHOOSE-':
        try:
            channel = int(values['-CH-'])
            window['-CH-'].update(text_color='#282923')
        except:
            window['-CH-'].update(text_color='#c44d45')

    if event == '-SELECT-':
        if(channel == 1 or channel == 2):
            graphInfo = GraphCSV(values['-FB-'], channel)
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