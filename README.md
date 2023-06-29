# BugID

## Project acronym: macro_inv_id

*BugID - a deep learning model embedded in a graphical user interface to identify macroinvertebrates from a videofeed e.g. microscope, webcam etc.*

### Installation and usage

To setup, download a '.zip' file or `git clone` the repository. Extract and open a command prompt in the directory. Create a virtual environment, e.g. using conda or pyenv, and install the dependencies required to run the GUI:

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
### Models

Three models are included as ONNX files in the 'models' directory (listed by increasing size/accuracy):

* 'mobilenetv2_050.onnx'
* 'resnet18.onnx'
* 'convnext_tiny.onnx'

The GUI can use all three models, try them out using the command line options.

The models have been fine-tuned from pre-trained models using timm and fastai. 

25 taxa of macroinvertebrates found in Danish streams are recognised:

* Ancylus sp
* Asellus sp
* Baetidae sp
* Caenidae sp
* Chironomus sp
* Elmis sp
* Ephemera sp
* Ephemerellidae
* Erpobdella sp
* Gammarus sp
* Glossosomatidae sp
* Goeridae sp
* Heptageniidae sp
* Hydropsychidae sp
* Leptophlebiidae sp
* Leuctra sp
* Limnius sp
* Lymnea sp
* Nemoura sp
* Oligochaeta sp
* Sericostomatidae sp
* Sialis sp
* Simuliidae sp
* Siphlonuridae
* Sphaerium sp

### Camera

The input image feed for the GUI should be a webcam, camera from a microscope, etc. If the camera cannot be opened, try another device index using the command line options.

Different resolutions of the input feed can be accommodated depending device/camera.

### Compile as executable file

Compile using pyinstaller (only tested on Windows):

```
pyinstaller -i logo.ico --windowed --onefile --add-data "models;models" --add-data "data;data" gui.py   
```

### Data

The data used to train and validate the models have been collected, identified and processed by us (see About) and supplemented with images from the [Global Biodiversity Information Facility](https://www.gbif.org/composition/57twunvM3vrUotO12WDNgc/what-is-gbif).

The data collected by us is available from Kaggle [URL TO COME]()

### About

This project is the result of a collaboration between Kenneth Thorø Martinsen (University of Copenhagen, Copenhagen, Denmark) and Søren Thromsholdt Christensen (Copenhagen Business Academy, Hillerød, Denmark).
