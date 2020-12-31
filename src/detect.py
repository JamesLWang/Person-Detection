import os
import logging
import imutils
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import time
import cv2

ASSETS_PATH = 'assets/'
MODEL_PATH = os.path.join(ASSETS_PATH, 'frozen_inference_graph.pb')
CONFIG_PATH = os.path.join(ASSETS_PATH, 'ssd_mobilenet_v2_coco_2018_03_29.pbtxt')
LABELS_PATH = os.path.join(ASSETS_PATH, 'labels.txt')
SCORE_THRESHOLD = 0.7
NETWORK_INPUT_SIZE = (300, 300)
NETWORK_SCALE_FACTOR = 1
INTERVAL = 3

logger = logging.getLogger('detector')
logging.basicConfig(level=logging.INFO)

# Reading coco labels
with open(LABELS_PATH, 'rt') as f:
    labels = f.read().rstrip('\n').split('\n')
COLORS = [[0, 0, 255]] * len(labels)

ssd_net = cv2.dnn.readNetFromTensorflow(model=MODEL_PATH, config=CONFIG_PATH)

vs = VideoStream(src=0).start()
time.sleep(0.5)
fps = FPS().start()

temp_time = time.time()
while True:
    # Reading frames
    frame = vs.read()
    frame = imutils.resize(frame, width=1200)
    height, width, channels = frame.shape

    # Converting frames to blobs using mean standardization
    blob = cv2.dnn.blobFromImage(image=frame,
                                 scalefactor=NETWORK_SCALE_FACTOR,
                                 size=NETWORK_INPUT_SIZE,
                                 mean=(127.5, 127.5, 127.5),
                                 crop=False)

    # Passing blob through neural network
    ssd_net.setInput(blob)
    network_output = ssd_net.forward()

    for detection in network_output[0, 0]:
        score = float(detection[2])
        class_index = np.int(detection[1])
        label = f'{labels[class_index]}: {score:.2%}'

        
        if score > SCORE_THRESHOLD:
            left = np.int(detection[3] * width)
            top = np.int(detection[4] * height)
            right = np.int(detection[5] * width)
            bottom = np.int(detection[6] * height)

            
            if(label.split(':')[0] == 'person'):
                if(time.time() - temp_time > INTERVAL):
                    timestr = time.strftime("%Y%m%d-%H%M%S")
                    time_wo_sec = timestr[:-2]
                    directory = "static/" + time_wo_sec + '/'
                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    cv2.imwrite(directory + timestr + ".png", frame)
                    print("Person detected at %s" %(timestr))
                    temp_time = time.time()

                    cv2.rectangle(img=frame,
                                rec=(left, top, right, bottom),
                                color=COLORS[class_index],
                                thickness=4,
                                lineType=cv2.LINE_AA)

                    cv2.putText(img=frame,
                                text=label,
                                org=(left, np.int(top*0.9)),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=2,
                                color=COLORS[class_index],
                                thickness=2,
                                lineType=cv2.LINE_AA)

                    cv2.imwrite(directory + timestr + "_labeled.png", frame)
            
    fps.update()

fps.stop()
cv2.destroyAllWindows()
vs.stop()
