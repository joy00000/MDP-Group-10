# MDP-IRS

## Setup Steps
- Install CUDA 11.3 https://developer.nvidia.com/cuda-11.3.0-download-archive

- cd to project root, 
  - pip install torch==1.10.2+cu113 torchvision==0.11.3+cu113 torchaudio===0.10.2+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
  - pip install -r yolov5/requirements.txt

- Run the ImageRecognitionServer.py
  - cd mdp-irs\src
  - python ImageRecognitionServer.py
