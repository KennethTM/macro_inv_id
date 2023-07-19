#!/usr/bin/env python
import argparse 
import PySimpleGUI as sg
import cv2
import numpy as np
from collections import Counter
from os import path
from dvfi import DVFI

def read_vocab(path):

    with open(path, 'r') as f:
        model_vocab = f.read().splitlines()

    return(model_vocab)

def update_table(window, spec_list):

    spec_count = Counter(spec_list)
    spec_table = [[k.capitalize().replace("sp", ""), v] for k, v in zip(spec_count.keys(), spec_count.values())]

    spec_list_dvfi = [i.capitalize().replace(" sp", "") for i in spec_list]
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

def main(model_name, device, cap_width, cap_height):

    sg.theme('Black')

    save_list = []
    #save_list = ["Leuctra sp", "Asellus sp", "Leuctra sp", "Elmis sp", "Elmis sp", "Elmis sp", "Chironomus sp", "Chironomus sp", "Chironomus sp", "Chironomus sp", "Chironomus sp", "Chironomus sp", "Baetidae sp", "Sericostomatidae sp", "Sericostomatidae sp"]

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
                        col_widths=[20, 10])],
                    [sg.Text('', key="result_text")]]
    
    layout = [[sg.Text('BugID', size=(20, 1), font='Helvetica 16')],
              [sg.Frame("Kamera", layout_left, size=(300, 450)), 
               sg.Frame("Data", layout_right, size = (300, 450))]]

    window = sg.Window('BugID', layout)

    model_path = path.abspath(path.join(path.dirname(__file__), "models", model_name))
    model = cv2.dnn.readNetFromONNX(model_path)

    vocab_path = path.abspath(path.join(path.dirname(__file__), "data", "vocab.txt"))
    model_vocab = read_vocab(vocab_path)

    scale = 1/255
    images_size = 300
    
    cap = cv2.VideoCapture(device)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)

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
            #frame = cv2.imread("image_preproc/valid/Gammarus sp/CPH-Gammarus sp.-1088.png")

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

            frame_output = cv2.cvtColor((np.transpose(model_input.squeeze(), (1, 2, 0))*255).astype(np.uint8), cv2.COLOR_RGB2BGR)
            frame_output_bytes = cv2.imencode('.png', frame_output)[1].tobytes()
            window['image'].update(data=frame_output_bytes)

            label = f'Art: {class_pred.replace("sp", "")} ({int(output[idx_pred]*100)}%)'
            window["image_text"].update(label)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run BugID GUI for species identification using a webcam")
    parser.add_argument("-model_name", type=str, default="mobilenetv2_050.onnx", help="Name of ONNX model in 'models' directory to use. Default: 'mobilenetv2_050.onnx'")
    parser.add_argument("-device", type=int, default=0, help="Camera device index, e.g. try 0, 1 or 2. Default: 0")
    parser.add_argument("-cap_width", type=int, default=1920, help="Camera input width - resolution should be supported by the camera. Default: 1920")
    parser.add_argument("-cap_height", type=int, default=1080, help="Camera input height - resolution should be supported by the camera. Default: 1080")
    arguments = parser.parse_args()

    main(arguments.model_name, arguments.device, arguments.cap_width, arguments.cap_height)
