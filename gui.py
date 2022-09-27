#!/usr/bin/env python
import PySimpleGUI as sg
import cv2
import numpy as np
from collections import Counter

#https://github.com/PySimpleGUI/PySimpleGUI
#https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_OpenCV_Webcam.py

#Band order when converting between opencv/np and fastai is important

def main():

    sg.theme('Black')

    save_list = []

    layout = [[sg.Text('LiveMakroID', size=(20, 1), font='Helvetica 22')],
              [sg.Text('Click start to begin', font='Helvetica 16', key="image_text")],
              [sg.Image(filename='', key='image')],
              [sg.Button('Start', size=(10, 1), font='Helvetica 12'),
               sg.Button('Stop', size=(10, 1), font='Any 12'),
               sg.Button('Save', size=(10, 1), font='Helvetica 12'),
               sg.Button('Exit', size=(10, 1), font='Helvetica 12')],
              [sg.Table(values=save_list, headings=["Art", "Antal"], 
                        key="table", auto_size_columns=False, 
                        def_col_width=20, justification="left")],
              [sg.Text('', key="result_text")]]

    window = sg.Window('BugID Live DEMO', layout, location=(800, 400))

    model_path = "models/effnet_b0.onnx"
    model = cv2.dnn.readNetFromONNX(model_path)
    model_vocab = np.load("models/dk_vocab.npy")
    
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

            model_input = cv2.dnn.blobFromImage(
                image = frame,
                scalefactor = 1.0/255.0,
                size = (224, 224),
                swapRB=True,
                crop=True)
            
            model.setInput(model_input)
            out = model.forward().squeeze()
            idx_pred = np.argmax(out)
            class_pred = model_vocab[idx_pred]
            
            label = f'Art: {class_pred} ({int(out[idx_pred]*100)}%)'
            window["image_text"].update(label)

            if event == "Save":
                save_list.append(class_pred)
                save_list_count = Counter(save_list)
                save_list_table = [[k, v] for k, v in zip(save_list_count.keys(), save_list_count.values())]
                window["table"].update(values=save_list_table)
                window["result_text"].update('Antal arter: {} \nAntal individer: {}'.format(len(save_list_count.keys()), sum(save_list_count.values())))

            imgbytes = cv2.imencode('.png', frame)[1].tobytes()
            window['image'].update(data=imgbytes)

main()
