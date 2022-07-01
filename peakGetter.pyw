import PySimpleGUI as sg
from lib.csv_reader import GraphCSV

sg.theme('Topanga')

layout = [[sg.T('Choose CSV file')],
          [sg.In(key='-FB-', readonly=True, text_color='#282923'), sg.FileBrowse()],
          [sg.T('Insert Channel:'), sg.In(key='-CH-', text_color='#282923', background_color='#ffffff', size=(10,1)), sg.B('Choose', key='-CHOOSE-')],
          [sg.B('Select', key='-SELECT-')],
          [sg.T('Peak value:', font=('Helvetica', 15), size=(10, 0)), sg.T('', justification='right', key='-PEAK-', font=('Helvetica', 15))]]

window = sg.Window('Peak Value', layout, icon='./assets/mountain.ico', element_justification='center')

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
            peak = graphInfo.getPeakValue()
            unit = graphInfo.getAxisUnit('y')
            window['-PEAK-'].update(f'{peak:.2f} {unit}')

window.close()