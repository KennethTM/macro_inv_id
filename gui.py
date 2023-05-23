#!/usr/bin/env python
import PySimpleGUI as sg
import cv2
import numpy as np
from collections import Counter
from os import path
from dvfi_calc import DVFI

#export text file with results??

#https://github.com/PySimpleGUI/PySimpleGUI
#https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_OpenCV_Webcam.py

def read_vocab(path):

    with open(path, 'r') as f:
        model_vocab = f.read().splitlines()

    return(model_vocab)

def update_table(window, spec_list):
    spec_count = Counter(spec_list)
    spec_table = [[k.capitalize().replace("sp", "sp."), v] for k, v in zip(spec_count.keys(), spec_count.values())]

    spec_list_dvfi = [i.capitalize().replace(" sp", "").replace(" adult", "") for i in spec_list]
    dvfi_value, key_value, div_value = DVFI(spec_list_dvfi)

    window["table"].update(values=spec_table)
    window["result_text"].update(f'Antal arter: {len(spec_count.keys())} \nAntal individer: {sum(spec_count.values())} \nAntal diversitetsgrupper: {div_value} \nNøglegruppe: {key_value} \nDVFI score: {dvfi_value}')

def white_screen(window, img_size):
    white_screen = np.full((img_size, img_size), 255)
    white_screen_bytes = cv2.imencode('.png', white_screen)[1].tobytes()
    window['image'].update(data=white_screen_bytes)
    window["image_text"].update('Klik start!')
    window["table"].update(values=[])
    window["result_text"].update("")

def main():

    sg.theme('Black')

    save_list = []

    layout_left = [[sg.Button('Start', size=(8, 1), font='Helvetica 12'),
               sg.Button('Stop', size=(8, 1), font='Helvetica 12'),
               sg.Button('Exit', size=(8, 1), font='Helvetica 12')],
              [sg.Text('Klik start!', font='Helvetica 12', key="image_text")],
              [sg.Image(filename='', key='image')],
              [sg.Button('Gem', size=(8, 1), font='Helvetica 12'),
               sg.Button('Fortryd', size=(8, 1), font='Helvetica 12')],
              ]
    
    layout_right = [[sg.Table(values=save_list, headings=["Art", "Antal"], 
                        key="table", auto_size_columns=False, 
                        col_widths=[20, 8])],
                    [sg.Text('', key="result_text")]]
    
    layout = [[sg.Text('BugID', size=(20, 1), font='Helvetica 16')],
              [sg.Frame("Stereolup", layout_left, size=(300, 450)), 
               sg.Frame("Data", layout_right, size = (300, 450))]]

    window = sg.Window('BugID', layout)

    model_path = path.abspath(path.join(path.dirname(__file__), "models", "effnet_b0.onnx"))
    model = cv2.dnn.readNetFromONNX(model_path)

    vocab_path = path.abspath(path.join(path.dirname(__file__), "models", "dk_vocab.txt"))
    model_vocab = read_vocab(vocab_path)

    scale = 1/255
    images_size = 300
    
    cap = cv2.VideoCapture(1)
    #print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    #print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

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
            save_list = []

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
            
            if event == "Gem":
                save_list.append(class_pred)
                update_table(window, save_list)

            if event == "Fortryd":
                if save_list:
                    save_list.pop()
                    update_table(window, save_list)

            frame_output = cv2.cvtColor((np.transpose(model_input.squeeze(), (1, 2, 0))*255).astype(np.uint8), cv2.COLOR_RGB2BGR) #image flipped on ubuntu vs windows?
            frame_output_bytes = cv2.imencode('.png', frame_output)[1].tobytes()
            window['image'].update(data=frame_output_bytes)

            label = f'Art: {class_pred.replace("sp", "sp.")} ({int(output[idx_pred]*100)}%)'
            window["image_text"].update(label)

main()
