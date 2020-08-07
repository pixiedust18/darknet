from ctypes import *
import math
import random
import os
import cv2
import numpy as np
import time
import darknet
from skimage import io, draw
import cv2
from scipy.spatial import distance
from google.colab.patches import cv2_imshow

SD = 0
x1_co=[]
y1_co=[] 
x2_co=[] 
y2_co =[]
m_co=[]
c_co=[]
'''with open("floor_coordinates.txt") as f:
    zones = int(next(f)) # read first line
    wd, ht = [int(y) for y in next(f).split()]
    start_x1, start_y1, start_x2, start_y2 = [int(y) for y in next(f).split()] # read first line
    end_x1, end_y1, end_x2, end_y2 = [int(y) for y in next(f).split()]
    array = []
    for line in f: # read rest of lines
        x1, y1, x2, y2, m, c = ([float(x) for x in line.split()])
        x1_co.append(x1)
        y1_co.append(y1)
        x2_co.append(x2)
        y2_co.append(y2)
        m_co.append(m)
        c_co.append(c)'''
zones = 4
wd = 690 
ht = 388
start_x1, start_y1, start_x2, start_y2 = 3, 179, 605, 386
end_x1, end_y1, end_x2, end_y2 = 403 ,0 ,683, 0
x1_, y1_, x2_, y2_, m_, c_  = 3, 179, 605, 386, 0.3438538205980066 ,177.968438538206
x1_co.append(x1_)
y1_co.append(y1_)
x2_co.append(x2_)
y2_co.append(y2_)
m_co.append(m_)
c_co.append(c_)
x1_, y1_, x2_, y2_, m_, c_  = 136, 119 ,631 ,257 ,0.2789757412398922 ,81.29964061096132
x1_co.append(x1_)
y1_co.append(y1_)
x2_co.append(x2_)
y2_co.append(y2_)
m_co.append(m_)
c_co.append(c_)
x1_, y1_, x2_, y2_, m_, c_  = 269, 59, 657, 128, 0.17814113597246128, 11.627940332759593
x1_co.append(x1_)
y1_co.append(y1_)
x2_co.append(x2_)
y2_co.append(y2_)
m_co.append(m_)
c_co.append(c_)

def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax
f = 0.0046
import math
def check(p1, p2, w1, w2, h1, h2, SD, f):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    if(x1==x2 and y1==y2):
        return True
    coords = [(x1, y1), (x2, y2)]
       
    social_distance = distance.euclidean([x1, y1], [x2, y2])
    print(social_distance)
    param = (x1+x2)/2
    if(social_distance > 0 and social_distance < 0.25 * param):
        return False
    
    return True
'''def check(p1, p2, w1, w2, h1, h2, SD, f):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    if(x1==x2 and y1==y2):
        print("eq")
        return True
    v1 = 1.6 * f / (h1)
    v2 = 1.6 * f / (h2)
    print("v1, v2", v1, v2)
    sensor_w, sensor_h = 4.8, 3.6
    sensor_w_px, sensor_h_px = 3200, 2400
    real_dist = sensor_w * abs(x1-x2) / sensor_w_px
    x1_ = 0
    x2_ = real_dist
    ed = math.sqrt((x1_ - x2_)*(x1_ - x2_) + (v1-v2) * (v1 - v2))    
    print(ed)
    if (ed>0 and ed<SD):
        return False
    return True'''
    #param = (x1+x2)/2
    #if(social_distance > 0 and social_distance < 0.25 * param):
    #    return False
    
    #return True
def pointaboveline(m, c, x1, y1):
  if (y1 >= (m*x1 + c)):
    return True
  return False

def pointbelowline(m, c, x1, y1):
  if (y1 <= (m*x1 + c)):
    return True
  return False
###############################################################
def draw_zones(image):
    color = (0, 255, 0) 
    thickness = 5

        
    pt1 = (start_x1,start_y1)
    pt2 = (start_x2,start_y2)
    image = cv2.line(image, pt1, pt2, color, thickness) 

    pt1 = (end_x1, end_y1)
    pt2 = (end_x2,end_y2)
    image = cv2.line(image, pt1, pt2, color, thickness) 

    pt1 = (end_x2,end_y2)
    pt2 = (start_x2,start_y2)
    image = cv2.line(image, pt1, pt2, color, thickness) 

    pt1 = (start_x1,start_y1)
    pt2 = (end_x1, end_y1)
    image = cv2.line(image, pt1, pt2, color, thickness) 


    for i in range(zones-1):
        pt1 = (int(x1_co[i]), int(y1_co[i]))
        pt2 = (int(x2_co[i]), int(y2_co[i]))
        image = cv2.line(image, pt1, pt2, color, thickness)
        
    return image 
###############################################################
def find_zone(find_x, find_y):
    if (pointaboveline(m_co[0], c_co[0], find_x, find_y)==True):
        print("Zone", 1)
        return 1

    for i in range(zones-2):
        if (pointaboveline(m_co[i], c_co[i], find_x, find_y)==True and pointbelowline(m_co[i+1], c_co[i+1], find_x, find_y)==True):
            print("Zone", i+2)
            return i+2
    print("Zone", zones)
    return zones
###############################################################
def draw_zone1(image, zone_no):
    color = (0, 0, 255) 
    thickness = 5
        
    if (zone_no == 1):
        pt1 = (int(start_x1),int(start_y1))
        pt2 = (int(start_x2),int(start_y2))
        image = cv2.line(image, pt1, pt2, color, thickness) 

        pt1 = (int(start_x1),int(start_y1))
        pt2 = (int(x1_co[0]),int(y1_co[0]))
        image = cv2.line(image, pt1, pt2, color, thickness) 

        pt1 = (int(x1_co[0]),int(y1_co[0]))
        pt2 = (int(x2_co[0]),int(y2_co[0]))
        image = cv2.line(image, pt1, pt2, color, thickness) 

        pt1 = (int(start_x2),int(start_y2))
        pt2 = (int(x2_co[0]),int(y2_co[0]))
        image = cv2.line(image, pt1, pt2, color, thickness) 

    elif(zone_no == zones):
        pt1 = (int(end_x1), int(end_y1))
        pt2 = (int(end_x2), int(end_y2))
        image = cv2.line(image, pt1, pt2, color, thickness)

        pt1 = (int(end_x1), int(end_y1))
        pt2 = (int(x1[zone_no - 2]), int(y1[zone_no-2]))
        image = cv2.line(image, pt1, pt2, color, thickness)

        pt1 = (int(x2[zone_no - 2]), int(y2[zone_no-2]))
        pt2 = (int(x1[zone_no - 2]), int(y1[zone_no-2]))
        image = cv2.line(image, pt1, pt2, color, thickness)

        pt1 = (int(x2[zone_no - 2]), int(y2[zone_no-2]))
        pt2 = (int(end_x2), int(end_y2))
        image = cv2.line(image, pt1, pt2, color, thickness)
  
    else:
        
        pt1 = (int(x2[zone_no - 2]), int(y2[zone_no-2]))
        pt2 = (int(x1[zone_no - 2]), int(y1[zone_no-2]))
        image = cv2.line(image, pt1, pt2, color, thickness)

        pt1 = (int(x1[zone_no - 1]), int(y1[zone_no-1]))
        pt2 = (int(x1[zone_no - 2]), int(y1[zone_no-2]))
        image = cv2.line(image, pt1, pt2, color, thickness)

        pt1 = (int(x2[zone_no - 1]), int(y2[zone_no-1]))
        pt2 = (int(x2[zone_no - 2]), int(y2[zone_no-2]))
        image = cv2.line(image, pt1, pt2, color, thickness)

        pt1 = (int(x2[zone_no - 1]), int(y2[zone_no-1]))
        pt2 = (int(x1[zone_no - 1]), int(y1[zone_no-1]))
        image = cv2.line(image, pt1, pt2, color, thickness)

    return image


######################################################################
def cvDrawBoxes(detections, img, SD, f):
    print("SD: ", SD)
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
        
        coord = [x-w/2, y-h/2, w, h]
        
        if(isinstance(detection[0], str)):
            label = detection[0]
        else:
            label = detection[0].decode()
            
        if (label=='Person'):
            print(i)
            xywh.append(coord)
            wp.append(w)
            hp.append(h)
            i+=1
               
        if (label=='Mask'):
            boxColor = green
            x = int(x)
            y = int(y)
            cv2.putText(img, "Mask", (x,y - 10), font, font_scale, green, thickness)
        elif (label=='No_mask'):
            x = int(x)
            y = int(y)
            boxColor = red
            cv2.putText(img, "No Mask", (x,y - 10), font, font_scale, red, thickness)
        elif (label=='Person'):
            x_pmid = x 
            y_pmid = y + h/2
            print("person")
            feet_coord = (x_pmid, y_pmid)
            person_feet.append(feet_coord)
            
    sd_main = []
    i=0
    j=0
    #img = draw_zones(img)

    for mid1 in person_feet:
        truth = True
        j=0
        for mid2 in person_feet:
            sd = check(mid1, mid2, wp[i], wp[j], hp[i], hp[j], SD, f)
            print(i, " -> ", j," = ", sd)
            if(sd == False):
                #zone_no = find_zone(mid1[0], mid1[1])
                #img = draw_zone1(img, zone_no)
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


def YOLO(F= 0.00415, sd = 0, video_path = '/content/mask_footage.mp4', configPath = "cfg/custom-yolov4-detector.cfg", weightPath = "/content/custom-yolov4-detector_best.weights", metaPath = "data/obj.data"):

    global metaMain, netMain, altNames
    '''configPath = "./cfg/yolov4.cfg"
    weightPath = "./yolov4.weights"
    metaPath = "./cfg/coco.data"'''
    SD = sd
    sensor_w = 4.8
    f = F

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
            print("DF")
            
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
    fps = 30.0
    out = cv2.VideoWriter(
        "output.avi", cv2.VideoWriter_fourcc(*"MJPG"), fps,
        (darknet.network_width(netMain), darknet.network_height(netMain)))
    print("Starting the YOLO loop...")

    w = darknet.network_width(netMain)
    f = f *1000 * 512 / sensor_w
    print(f, SD)
    # Create an image we reuse for each detect
    darknet_image = darknet.make_image(darknet.network_width(netMain),
                                    darknet.network_height(netMain),3)
    main_tim = 0
    frame_no = 0
    while True:
        #try:
            prev_time = time.time()
            ret, frame_read = cap.read()
            frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (wd, ht))
            #frame_resized = cv2.rotate(frame_resized, cv2.ROTATE_90_CLOCKWISE)
            darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())
           
        
            detections = darknet.detect_image(netMain, metaMain, darknet_image, thresh=0.25)
            image = cvDrawBoxes(detections, frame_resized, SD, f)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            out.write(image)
            print(1/(time.time()-prev_time))
            main_tim += time.time()-prev_time
            frame_no += 1
            print("-------------------------------------------------------------------\n frame no  = ", frame_no, '\n------------------------------------------------------------')
            io.imshow(image)
            io.show()
            cv2.waitKey(3)
        #except:
            #break;
      
    cap.release()
    out.release()
    
if __name__ == "__main__":
    YOLO(F = 0.00415, sd = 0 , video_path = '/content/mask_footage.mp4', configPath = "cfg/custom-yolov4-detector.cfg", weightPath = "/content/custom-yolov4-detector_best.weights", metaPath = "data/obj.data")
