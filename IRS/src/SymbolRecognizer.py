# SymbolRecognizer - Recognizes symbols from input images using a weighted YOLOv5 Model
# @author Lim Rui An, Ryan
# @version 1.0
# @since 2022-02-10
# @modified 2022-02-10

# Imported dependencies
import torch # For the inference model

class SymbolRecognizer:
    ModelStatus = "nil"
    Model = None
    Classes = None
    ClassCount = -1

    # Class constuctor to setup weights
    def __init__(self, weightPath, classes, numclasses, useGPU = True):
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
        print("\nYOLOv5 Model initiallized with weight: " + weightPath)

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
        print("\nProcessing Inference Results")
        print(results.pandas().xyxy[0])  # predictions (pandas)
        labels, coord = results.xyxy[0][:, -1].to('cpu').numpy(), results.xyxy[0][:, :-1].to('cpu').numpy()
        # Area calculations
        areaList = []
        for i in range(len(coord)):
            x = coord[i][2] - coord[i][0] 
            y = coord[i][3] - coord[i][1]
            areaList.append(x * y) # Area of bounding box
        print("Area for each bound: " + ' '.join([str(area) for area in areaList]))
        return labels

    # Make use of processed results to create an output string to be sent back to RPi
    def SetupResultString(self, results):
        print("\nSetting Up Result Message")
        # Do stuff with passed labels
        label = "No Symbol Detected"
        for idx in results:
            i = int(idx)
            if (label[i] != "bullseye"):
                label = self.Classes[i]
        return label
