# BugID

**Project acronym: macro_inv_id**

![](https://github.com/KennethTM/macro_inv_id/blob/main/logo.png)

*BugID - a deep learning model embedded in a graphical user interface to identify macroinvertebrates from a videofeed e.g. microscope, webcam etc.*

## Installation

![](https://github.com/KennethTM/macro_inv_id/blob/main/screenshot.png)

*BugID graphical user interface*

### Run from executable

The provided 'BugID.exe' executable file in the 'dist' directory is a ready to run version of the graphical user interface (GUI) for Windows compiled using [PyInstaller](https://github.com/pyinstaller/pyinstaller). 

Download the file and run it to use the GUI with the default settings (model: mobilenetv2_050.onnx, device: 0, cap_width: 1920, cap_height: 1080). 

To run the program using other than default options, the executable file can be run from the command line. Open a command prompt, navigate to the directory with the executable file and run:

```
./BugID.exe -device 1
```

This command uses another camera device, see further description of options below. 

Due to size limitations, the executable file only contains the smallest model (mobilenetv2_050.onnx). However, after downloading the 'macro_inv_id' project as a '.zip' file, the executable file can be compiled with other options by changing the included model (see below) or in the 'gui.py' script.

To compile the GUI as an executable file (with the 'mobilenetv2_050.onnx' model) using PyInstaller (only tested on Windows):

```
pyinstaller -i logo.ico --windowed --onefile --add-data "models/mobilenetv2_050.onnx;models" --add-data "data;data" -n "BugID" gui.py
```

### Run from script

To setup and run the GUI from the provided scripts, download the 'macro_inv_id' project as a '.zip' file or `git clone` the repository. Extract and open a command prompt in the directory. Create a virtual environment, e.g. using conda or pyenv, and install the dependencies required to run the GUI:

```
#Create a conda environment (only nescessary the first time)
conda create --name bugid python

#Activate the environment
conda activate bugid

#Install requirements (only nescessary the first time)
pip install -r requirements_gui.txt

#Launch GUI with default arguments
python gui.py
```

To use the GUI after installing and setting up the environment the first time, just open a command prompt in the directory:

```
conda activate bugid
python gui.py
```

## Options

### Models

Three models are included as ONNX files in the 'models' directory (listed by increasing size/accuracy):

* mobilenetv2_050.onnx
* resnet18.onnx
* convnext_tiny.onnx

The GUI can use all three models, try them out using the command line options (`-model_name` option).

The models have been fine-tuned from pre-trained models using timm and fastai. 

25 taxa of macroinvertebrates found in Danish streams are recognised:

* *Ancylus* sp.
* *Asellus* sp.
* *Baetidae* sp.
* *Caenidae* sp.
* *Chironomus* sp.
* *Elmis* sp.
* *Ephemera* sp.
* *Ephemerellidae*
* *Erpobdella* sp.
* *Gammarus* sp.
* *Glossosomatidae* sp.
* *Goeridae* sp.
* *Heptageniidae* sp.
* *Hydropsychidae* sp.
* *Leptophlebiidae* sp.
* *Leuctra* sp.
* *Limnius* sp.
* *Lymnea* sp.
* *Nemoura* sp.
* *Oligochaeta* sp.
* *Sericostomatidae* sp.
* *Sialis* sp.
* *Simuliidae* sp.
* *Siphlonuridae*
* *Sphaerium* sp.

### Camera

The input image feed for the GUI should be a webcam, camera from a microscope, etc. If the camera cannot be opened (e.g. OpenCV error or exception), try another device index using the command line options (`-device` option).

Different resolutions of the input feed can be accommodated depending device/camera  (`-cap_height` and `-cap_width` options).

## Data

The data used to train and validate the models have been collected, identified and processed by us (see About) and supplemented with images from the [Global Biodiversity Information Facility](https://www.gbif.org/composition/57twunvM3vrUotO12WDNgc/what-is-gbif).

The data collected by us is available from [Kaggle](https://www.kaggle.com/datasets/kennethtm/stream-macroinvertebrates).

## About

This project is the result of a collaboration between Kenneth Thorø Martinsen (University of Copenhagen, Copenhagen, Denmark) and Søren Thromsholdt Christensen (Cphbusiness, Hillerød, Denmark).
