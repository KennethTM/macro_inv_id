#!/usr/bin/env python
import PySimpleGUI as sg
import cv2
import numpy as np
from collections import Counter

#https://github.com/PySimpleGUI/PySimpleGUI
#https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_OpenCV_Webcam.py

def read_vocab(path):
    model_vocab = []

    with open(path, 'r') as f:
        for i in f:
            x = i[:-1]
            model_vocab.append(x)

    return(model_vocab)

def main():

    sg.theme('Black')

    save_list = []

    layout = [[sg.Text('LiveMakroID', size=(20, 1), font='Helvetica 22')],
              [sg.Text('Click start to begin', font='Helvetica 16', key="image_text")],
              [sg.Image(filename='', key='image')],
              [sg.Button('Start', size=(10, 1), font='Helvetica 12'),
               sg.Button('Stop', size=(10, 1), font='Helvetica 12'),
               sg.Button('Save', size=(10, 1), font='Helvetica 12'),
               sg.Button('Exit', size=(10, 1), font='Helvetica 12')],
              [sg.Table(values=save_list, headings=["Art", "Antal"], 
                        key="table", auto_size_columns=False, 
                        def_col_width=20, justification="left")],
              [sg.Text('', key="result_text")]]

    window = sg.Window('BugID Live DEMO', layout, location=(600, 400))

    model_path = "models/effnet_b3.onnx"
    model = cv2.dnn.readNetFromONNX(model_path)
    model_vocab = read_vocab("models/dk_vocab.txt")

    scale = 1/255
    images_size = 300
    
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
            white_screen = np.full((images_size, images_size), 255)

            white_screen_bytes = cv2.imencode('.png', white_screen)[1].tobytes()
            window['image'].update(data=white_screen_bytes)
            window["image_text"].update('Click start to begin')
            save_list = []
            window["table"].update(values=save_list)
            window["result_text"].update()

        if recording:
            ret, frame = cap.read()

            model_input = cv2.dnn.blobFromImage(
                image = frame,
                scalefactor = scale,
                size = (images_size, images_size),
                swapRB=True,
                crop=True)
            
            model.setInput(model_input)
            output = model.forward().squeeze()
            idx_pred = np.argmax(output)
            class_pred = model_vocab[idx_pred]
            
            label = f'Art: {class_pred} ({int(output[idx_pred]*100)}%)'
            window["image_text"].update(label)

            if event == "Save":
                save_list.append(class_pred)
                save_list_count = Counter(save_list)
                save_list_table = [[k, v] for k, v in zip(save_list_count.keys(), save_list_count.values())]
                window["table"].update(values=save_list_table)
                window["result_text"].update('Antal arter: {} \nAntal individer: {}'.format(len(save_list_count.keys()), sum(save_list_count.values())))

            frame_output = cv2.cvtColor((np.transpose(model_input.squeeze(), (2, 1, 0))*255).astype(np.uint8), cv2.COLOR_RGB2BGR)

            frame_output_bytes = cv2.imencode('.png', frame_output)[1].tobytes()
            window['image'].update(data=frame_output_bytes)

main()
