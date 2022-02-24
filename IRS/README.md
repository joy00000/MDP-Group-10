# Image Recognition Server

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
- Connect to RPi via WiFi
- Run the ImageRecognitionServer.py
  - cd IRS\src (IMPORTANT TO SWITCH TO SRC DIRECTORY)
  - python ImageRecognitionServer.py
