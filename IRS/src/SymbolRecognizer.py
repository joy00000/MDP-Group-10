'''
SymbolRecognizer - Recognizes symbols from input images using a weighted YOLOv5 Model
@author Lim Rui An, Ryan
@version 1.2
@since 2022-02-10
@modified 2022-02-18
'''

# Imported dependencies
import torch # For the inference model
import pandas as pd # For processing purposes

class SymbolRecognizer:
    ModelStatus = "nil"
    Model = None
    Classes = None
    ClassCount = -1

    # Class constuctor to setup weights
    def __init__(self, weightPath, classes, numclasses, useGPU = True):
        print("> Begin initiallization of YOLOv5 Model")
        self.LoadWeights(weightPath, useGPU)
        self.Classes = classes
        self.ClassCount = numclasses

    # Import the selected weights file into YOLOv5
    def LoadWeights(self, weightPath, useGPU = True):
        # Set the current weight to be the status
        self.ModelStatus = weightPath
        # Initialize the model
        #self.Model = torch.hub.load('ultralytics/yolov5', 'custom', path = weightPath)
        if useGPU:
            self.Model = torch.hub.load('../yolov5/', 'custom', path=weightPath, source='local')
        else: self.Model = torch.hub.load('../yolov5/', 'custom', path=weightPath, source='local', device='cpu')
        # Print status
        print("\nYOLOv5 Model initiallized with weight: " + weightPath + "\n")

    # Run inference on the source images in the path with the model
    def ProcessSourceImages(self, srcPath, savePath = "runs/detect/exp", saveImg = False):
        # Conduct Inferencez
        results = self.Model(srcPath)
        if saveImg:
            results.save(save_dir = savePath)
        results.show()
        outputMessage = self.SetupResultString(self.ProcessInferenceResults(results))
        return outputMessage

    # Process results of model inference to determine which symbol is most likely the result
    def ProcessInferenceResults(self, results):
        print("\n> Processing Inference Results")
        print(results.pandas().xyxy[0])  # predictions (pandas)
        labels, coord = results.xyxy[0][:, -1].to('cpu').numpy(), results.xyxy[0][:, :-1].to('cpu').numpy()
        # Area calculations
        heightList = []
        for i in range(len(coord)):
            #x = coord[i][2] - coord[i][0]
            y = coord[i][3] - coord[i][1]
            #areaList.append(x * y) # Area of bounding box
            heightList.append(y) # Height of bounding box
        print("Height for each bound: " + ' '.join([str(Height) for Height in heightList]))
        labelswithheight = pd.DataFrame({'labels' : labels, 'height' : heightList})
        return labelswithheight

    # Make use of processed results to create an output string to be sent back to RPi
    def SetupResultString(self, results):
        print("\n> Setting Up Result Message")
        # Return the label that has the greatest vertical height
        label = "Nothing"
        maxHeight = -1
        bullseyeFound = False
        labels = results["labels"]
        height = results["height"]
        # Loop through the dataframe and return the symbol name (not bullseye) with the greatest height
        for idx in range(len(results)):
            i = idx
            tag = self.Classes[int(labels[i])]
             # Found one that isn't a bullseye and having a greater max height
            if tag != 'bullseye' and height[i] > maxHeight:
                maxHeight = height[i]
                label = tag
            elif tag == 'bullseye':
                bullseyeFound = True
        # If there was no tallest symbol but a bullseye was found
        if label == "Nothing" and bullseyeFound:
            label = 'bullseye'
        return label
