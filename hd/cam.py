#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on  23/8/22 11:41

@author: Edward L. Campbell Hernández
contact: ecampbelldsp@gmail.com
"""
import tempfile

import cv2
from datetime import datetime


def take_picture() -> dict:

    with open("/tmp/photo.png", "w") as tmp:

        for device in range(-1, 10):

            cam = cv2.VideoCapture(device)
            ret, image = cam.read()

            if image is None:
                cam.release()
                cv2.destroyAllWindows()
                continue
            else:
                cv2.imwrite(tmp.name, image)
                return {"success": "true", "path": tmp.name}

        return {"success": "false", "message": f"Hardware error on the WEBCAM occurs: {e}", "path": ""}
