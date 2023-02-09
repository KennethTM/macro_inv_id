#!/usr/bin/env python
import PySimpleGUI as sg
import cv2
import numpy as np
from collections import Counter
from os import path
import random 

#https://github.com/PySimpleGUI/PySimpleGUI
#https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_OpenCV_Webcam.py

def read_vocab(path):
    model_vocab = []

    with open(path, 'r') as f:
        for i in f:
            x = i[:-1]
            model_vocab.append(x)

    return(model_vocab)

def update_table(window, spec_list):
    spec_count = Counter(spec_list)
    spec_table = [[k, v] for k, v in zip(spec_count.keys(), spec_count.values())]

    dvfi_value = random.randint(1, 7)

    window["table"].update(values=spec_table)
    window["result_text"].update(f'Antal arter: {len(spec_count.keys())} \nAntal individer: {sum(spec_count.values())} \nDVFI score: {dvfi_value}')

def white_screen(window, img_size):
    white_screen = np.full((img_size, img_size), 255)
    white_screen_bytes = cv2.imencode('.png', white_screen)[1].tobytes()
    window['image'].update(data=white_screen_bytes)
    window["image_text"].update('Click start to begin')
    save_list = []
    window["table"].update(values=save_list)
    window["result_text"].update()

def main():

    sg.theme('Black')

    save_list = []

    layout = [[sg.Text('BugID', size=(20, 1), font='Helvetica 22')],
              [sg.Button('Start', size=(8, 1), font='Helvetica 12'),
               sg.Button('Stop', size=(8, 1), font='Helvetica 12'),
               sg.Button('Exit', size=(8, 1), font='Helvetica 12')],
              [sg.Text('Click start to begin', font='Helvetica 16', key="image_text")],
              [sg.Image(filename='', key='image')],
              [sg.Table(values=save_list, headings=["Art", "Antal"], 
                        key="table", auto_size_columns=False, 
                        col_widths=[20, 8], justification="left")],
              [sg.Button('Save', size=(8, 1), font='Helvetica 12'),
               sg.Button('Undo', size=(8, 1), font='Helvetica 12')],
              [sg.Text('', key="result_text")]]

    window = sg.Window('BugID Live DEMO', layout, location=(600, 400))

    model_path = path.abspath(path.join(path.dirname(__file__), "models", "effnet_b0.onnx"))
    model = cv2.dnn.readNetFromONNX(model_path)
    vocab_path = path.abspath(path.join(path.dirname(__file__), "models", "dk_vocab.txt"))
    model_vocab = read_vocab(vocab_path)

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
            white_screen(window, images_size)

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
                update_table(window, save_list)

            if event == "Undo":
                if save_list:
                    save_list.pop()
                    update_table(window, save_list)

            frame_output = cv2.cvtColor((np.transpose(model_input.squeeze(), (1, 2, 0))*255).astype(np.uint8), cv2.COLOR_RGB2BGR) #image flipped on ubuntu vs windows?

            frame_output_bytes = cv2.imencode('.png', frame_output)[1].tobytes()
            window['image'].update(data=frame_output_bytes)

main()
