import PySimpleGUI as sg
from lib.csv_reader import GraphCSV

sg.theme('Topanga')

layout = [[sg.T('Choose CSV file')],
          [sg.In(key='-FB-', readonly=True, text_color='#282923'), sg.FileBrowse()],
          [sg.B('Select', key='-SELECT-')],
          [sg.T('Peak value:', font=('Helvetica', 15), size=(10, 0)), sg.T('', justification='right', key='-PEAK-', font=('Helvetica', 15))]]

window = sg.Window('Peak Value', layout, icon='./assets/mountain.ico', element_justification='center')

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '-SELECT-':
        graphInfo = GraphCSV(values['-FB-'])
        peak = graphInfo.getPeakValue()
        unit = graphInfo.getAxisUnit('y')
        window['-PEAK-'].update(f'{peak:.2f} {unit}')

window.close()