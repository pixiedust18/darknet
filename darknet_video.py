from ctypes import *
import math
import random
import os
import cv2
import numpy as np
import time
import darknet

def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax

import math
def check(p1, p2, w1, w2, h1, h2):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    if(x1==x2 and y1==y2):
        return True
    coords = [(x1, y1), (x2, y2)]
       
    ed = distance.euclidean([x1, y1], [x2, y2])
    print(ed)
    
    x_dist = abs(x1-x2)
    y_dist = abs(y1-y2)
    theta = math.atan(y_dist / x_dist)
    
    sd1 = h1 / 1.6 * math.cos(theta)
    sd2 = h2 / 1.6 * math.cos(theta)
    
    if (ed > 0 and (sd1 + sd2) > ed):
        return False
    
    return True
    '''param = (x1+x2)/2
    if(social_distance > 0 and social_distance < 0.25 * param):
        return False
    
    return True'''

def cvDrawBoxes(detections, img):
    face_mids = []
    person_feet = []
    xywh = []
    wp = []
    hp = []
    i=0
    font_scale = 0.35
    thickness = 1
    blue = (0,0,255)
    green = (0,255,0)
    red = (255,0,0)
    font=cv2.FONT_HERSHEY_COMPLEX
    
    for detection in detections:
        x, y, w, h = detection[2][0],\
            detection[2][1],\
            detection[2][2],\
            detection[2][3]
        xmin, ymin, xmax, ymax = convertBack(
            float(x), float(y), float(w), float(h))
        
        coord = [x, y, w, h]
        
        if (label=='Person'):
            print(i)
            xywh.append(coord)
            wp.append(w)
            hp.append(h)
            i+=1
               
        if (label=='Mask'):
            boxColor = green
            cv2.putText(img, "Mask", (x,y - 10), font, font_scale, green, thickness)
        elif (label=='No_mask'):
            boxColor = red
            cv2.putText(img, "No Mask", (x,y - 10), font, font_scale, red, thickness)
        elif (label=='Person'):
            x_pmid = x + w/2
            y_pmid = y + h
            feet_coord = (x_pmid, y_pmid)
            person_feet.append(feet_coord)
            
    sd_main = []
    i=0
    j=0
    for mid1 in person_feet:
        truth = True
        j=0
        for mid2 in person_feet:
            sd = check(mid1, mid2, wp[i], wp[j], hp[i], hp[j])
            print(i, " -> ", j," = ", sd)
            if(sd == False):
                truth = False
                break
            j+=1
        i+=1
        sd_main.append(truth)
            
        pt1 = (xmin, ymin)
        pt2 = (xmax, ymax)
        
    i=0
    for coord in xywh:
        x, y, w, h = coord
        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)
        
        if (sd_main[i] == True):
            print("SD")
            cv2.rectangle(img, (x, y), (x + w, y + h), (150, 150, 0), 2)
            cv2.putText(img, str(i)+" SD", (x,y - 10), font, font_scale, (150, 150, 0), thickness)
        else:  
            print("NO SD")
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 150), 2)
            cv2.putText(img, str(i)+" No SD", (x,y - 10), font, font_scale, (0, 0, 150), thickness)
        i+=1
                
                
                
        '''cv2.rectangle(img, pt1, pt2, (0, 255, 0), 1)
        cv2.putText(img,
                    detection[0].decode() +
                    " [" + str(round(detection[1] * 100, 2)) + "]",
                    (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    [0, 255, 0], 2)'''
    return img


netMain = None
metaMain = None
altNames = None


def YOLO(video_path = '/content/mask_footage.mp4', configPath = "cfg/custom-yolov4-detector.cfg", weightPath = "/content/custom-yolov4-detector_best.weights", metaPath = "data/obj.data"):

    global metaMain, netMain, altNames
    '''configPath = "./cfg/yolov4.cfg"
    weightPath = "./yolov4.weights"
    metaPath = "./cfg/coco.data"'''
    if not os.path.exists(configPath):
        raise ValueError("Invalid config path `" +
                         os.path.abspath(configPath)+"`")
    if not os.path.exists(weightPath):
        raise ValueError("Invalid weight path `" +
                         os.path.abspath(weightPath)+"`")
    if not os.path.exists(metaPath):
        raise ValueError("Invalid data file path `" +
                         os.path.abspath(metaPath)+"`")
    if netMain is None:
        netMain = darknet.load_net_custom(configPath.encode(
            "ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
    if metaMain is None:
        metaMain = darknet.load_meta(metaPath.encode("ascii"))
    if altNames is None:
        try:
            with open(metaPath) as metaFH:
                metaContents = metaFH.read()
                import re
                match = re.search("names *= *(.*)$", metaContents,
                                  re.IGNORECASE | re.MULTILINE)
                if match:
                    result = match.group(1)
                else:
                    result = None
                try:
                    if os.path.exists(result):
                        with open(result) as namesFH:
                            namesList = namesFH.read().strip().split("\n")
                            altNames = [x.strip() for x in namesList]
                except TypeError:
                    pass
        except Exception:
            pass
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(video_path)
    cap.set(3, 1280)
    cap.set(4, 720)
    out = cv2.VideoWriter(
        "output.avi", cv2.VideoWriter_fourcc(*"MJPG"), fps,
        (darknet.network_width(netMain), darknet.network_height(netMain)))
    print("Starting the YOLO loop...")

    # Create an image we reuse for each detect
    darknet_image = darknet.make_image(darknet.network_width(netMain),
                                    darknet.network_height(netMain),3)
    while True:
        try:
            prev_time = time.time()
            ret, frame_read = cap.read()
            frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb,
                                       (darknet.network_width(netMain),
                                        darknet.network_height(netMain)),
                                       interpolation=cv2.INTER_LINEAR)

            darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())
           
        
            detections = darknet.detect_image(netMain, metaMain, darknet_image, thresh=0.25)
            image = cvDrawBoxes(detections, frame_resized, mask_wt_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            out.write(image)
            print(1/(time.time()-prev_time))
            #io.imshow(image)
            #io.show()
            cv2.waitKey(3)
        except:
            break;
      
    cap.release()
    out.release()
    
if __name__ == "__main__":
    YOLO(video_path = '/content/mask_footage.mp4', configPath = "cfg/custom-yolov4-detector.cfg", weightPath = "/content/custom-yolov4-detector_best.weights", metaPath = "data/obj.data")
