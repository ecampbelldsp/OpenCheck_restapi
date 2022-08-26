#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on  23/8/22 11:41

@author: Edward L. Campbell Hernández
contact: ecampbelldsp@gmail.com
"""


import cv2
from datetime import datetime

def take_picture():
    def returnCameraIndexes():
        # checks the first 10 indexes.
        index = 0
        arr = []
        i = 3
        while i > 0:
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
            index += 1
            i -= 1
        return arr

    ind = returnCameraIndexes()

    cam = cv2.VideoCapture(ind[-1])

    date = datetime.now()
    date_str = date.strftime("%d_%m_%Y_%H_%M_%S")
    # sleep(1)
    # while True:
    ret, image = cam.read()
        # cv2.imshow('Imagetest',image)
        # k = cv2.waitKey(1)
        # if k != -1:
        # 		break
    cv2.imwrite("data/photo/"+date_str+".png", image)
    cam.release()
    cv2.destroyAllWindows()

    return "0"
