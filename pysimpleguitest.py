#!/usr/bin/env python
import PySimpleGUI as sg
import numpy as np
import cv2
import time
from fastai.vision.all import *
import pathlib
import collections

#https://github.com/PySimpleGUI/PySimpleGUI
#https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_OpenCV_Webcam.py

def main():

    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath

    sg.theme('Black')

    save_list = []

    layout = [[sg.Text('LiveMakroID', size=(20, 1), font='Helvetica 22')],
              [sg.Text('Click start to begin', font='Helvetica 16', key="image_text")],
              [sg.Image(filename='', key='image')],
              [sg.Button('Start', size=(10, 1), font='Helvetica 12'),
               sg.Button('Stop', size=(10, 1), font='Any 12'),
               sg.Button('Save', size=(10, 1), font='Helvetica 12'),
               sg.Button('Exit', size=(10, 1), font='Helvetica 12')],
              [sg.Table(values=save_list, headings=["Art", "Antal"], key="table", auto_size_columns=False, def_col_width=20, justification="left")],
              [sg.Text('', key="result_text")]]

    window = sg.Window('LiveMakroID DEMO', layout, location=(800, 400))

    weights_dir = Path("models")/"resnet34-fin-ept-dk.export"
    learn_inf = load_learner(weights_dir)

    cap = cv2.VideoCapture(0)

    recording = False

    while True:
        event, values = window.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            return

        elif event == 'Start':
            recording = True

        elif event == 'Stop':
            recording = False
            img = np.full((480, 640), 255)

            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['image'].update(data=imgbytes)
            window["image_text"].update('Click start to begin')
            save_list = []
            window["table"].update(values=save_list)
            window["result_text"].update()

        if recording:
            ret, frame = cap.read()

            img = PILImage.create(frame)
            pred, pred_idx, probs = learn_inf.predict(img)
            label = f'Art: {pred} ({int(probs[pred_idx]*100)} %)'
            window["image_text"].update(label)

            if event == "Save":
                save_list.append(pred)
                save_list_count = collections.Counter(save_list)
                save_list_table = [[k, v] for k, v in zip(save_list_count.keys(), save_list_count.values())]
                window["table"].update(values=save_list_table)
                window["result_text"].update('Antal arter: {} \nAntal individer: {}'.format(len(save_list_count.keys()), sum(save_list_count.values())))

            imgbytes = cv2.imencode('.png', frame)[1].tobytes()
            window['image'].update(data=imgbytes)

main()
