'''
SymbolRecognizer - Recognizes symbols from input images using a weighted YOLOv5 Model
@author Lim Rui An, Ryan
@version 1.3
@since 2022-02-10
@modified 2022-03-01
'''

# Imported dependencies
import torch # For the inference model
import pandas as pd # For processing purposes

class SymbolRecognizer:
    ModelStatus = "nil"
    Model = None
    Classes = None
    ClassCount = -1
    ConfThreshold = 0.6 # NMS confidence threshold

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
        # Set acceptable confidence
        self.Model.conf = self.ConfThreshold
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
        # ALL CALCULATIONS OF BOUNDING BOXES WILL BE DONE IN TERMS OF RATIO
        labels, coords, conf = results.xyxyn[0][:, -1].to('cpu').numpy(), results.xyxyn[0][:, :-2].to('cpu').numpy(), results.xyxyn[0][:, -2].to('cpu').numpy()

        # Vertical Height calculations
        print("Calculating Bound Heights")
        heightList = []
        for i in range(len(coords)):
            y = coords[i][3] - coords[i][1]
            heightList.append(y) # Height of bounding box
        #print("Height for each detected bound: " + ' '.join([str(Height) for Height in heightList]))

        # Get class names for each label
        nameList = []
        print("Identifying Class Tags")
        for i in labels:
            nameList.append(self.Classes[int(i)])

        # Get X offset of bound from center of image
        offsetList = []
        print("Calculating Directional Offset")
        for coord in coords:
            # Calculate center for each bound
            x, y = (coord[2] - coord[0]) * 0.5 + coord[0], (coord[3] - coord[1]) * 0.5 + coord[1]
            # Use the x bound to determine directional offset from the center of the image
            offsetX = x - 0.5 # As we are working in ratio, center is 0.5
            # If the offset is positive, symbol is on the right of image, negative -> left
            offsetList.append(offsetX)

        # Merge results into a dataframe of <label, coords, height, confidence>
        resultDF = pd.DataFrame({'name' : nameList, 'labels' : labels, 'height' : heightList, 'offset' : offsetList, 'conf' : conf})
        print("\n> Processed Detection Results")
        print(resultDF)

        return resultDF

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
