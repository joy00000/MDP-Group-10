# Image Recognition Server

## About
This Image Recognition Server makes use of a YOLOv5 model to perform inference on provided images to return a trained symbol of the highest precision.
Refer to the src folder in the project directory for the code files of this project
- ImageRecognitionServer.py > The server process that receives images, acquires inference results and sends the result back to the connected RPi
  - Contains configurable settings for the server process
- SymbolRecognizer.py > Class that holds an object where the model is loaded into and contains wrapper functions for performing and processing inferences

## Folder Structure
IRS
- collage (Output inference collage)
- inferences (Inference processed images)
- receivedimg (Images received from RPi <Unprocessed>)
- src (Source code)
- weights (Trained weights for the YOLOv5 model)
- yolov5 (Local YOLOv5 repository used for loading the model)
  
## Notes
- In between runs of IRS, please empty the inference folders to allow for correct collage output

# Installation Guide
## Setup w/ GPU
- Install pip https://pypi.org/project/pip/

- Install Python 3.9 https://www.python.org/downloads/release/python-390/

- Install CUDA 11.3 https://developer.nvidia.com/cuda-11.3.0-download-archive

- Change directory (cd) to project root, (D:YOUR DIRECTORY\MDP-Group-10\IRS), run the following in cmd prompt
  - pip install torch==1.10.2+cu113 torchvision==0.11.3+cu113 torchaudio===0.10.2+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
  - pip install -r yolov5/requirements.txt

## Setup without GPU
- Install pip https://pypi.org/project/pip/

- Install Python 3.9 https://www.python.org/downloads/release/python-390/

- Change directory (cd) to project root, (D:YOUR DIRECTORY\MDP-Group-10\IRS), run the following in cmd prompt
  - pip install -r yolov5/requirements.txt

- Install Pytorch, pip install torch

- Open ImageRecognitionServer.py
  - Edit the following parameters
    - USE_GPU, set to False
    - DEBUG_MODE_ON, set to False

## Running the Server
- Run the ImageRecognitionServer.py
  - cd IRS\src (IMPORTANT TO SWITCH TO SRC DIRECTORY)
  - python ImageRecognitionServer.py


