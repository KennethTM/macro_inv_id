# macro_inv_id

A deep learning model embedded in a graphical user interface (GUI) to identify macroinvertebrates from a videofeed e.g. microscope, webcam etc.

To use, download the repository as a '.zip' file, extract and open a command prompt in the folder. Create an environment and install the depencies required to run the GUI:

```
conda create --name macro_inv_id python
conda activate macro_inv_id
pip install -r requirements_gui.txt
python gui.py
```

Compile using pyinstaller (tested on windows):

```
pyinstaller -i logo.ico --windowed --onefile --add-data "models;models" gui.py   
```
