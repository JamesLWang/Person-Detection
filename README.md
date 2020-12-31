## Person Detection using MobileNetSSD with Flask Server
This project was sourced from [this repository](https://github.com/mm5631/live_object_detection) for live object detection. 

This script uses OpenCV's DNN library to load weights from a MobileNet SSD tensorflow model.
The classes available are from the COCO dataset. 
The efficient [imutils](https://github.com/jrosebr1/imutils) is used for camera interfacing. 

### Setup

Run the following commands. It is recommended to use a virtual environment. 
```
pip install --upgrade pip
cd live_object_detection
pip install -r requirements.txt
```

### Execution
To run the logger, run ```$ python src/detect.py```
To run the Flask server, run ```python interface.py```
Both should run simultaneously. 

The logger captures once every `INTERVAL` seconds, located in `detect.py`. Only the `CACHE_CAP` most recent minute events will be saved, located in `interface.py`. 