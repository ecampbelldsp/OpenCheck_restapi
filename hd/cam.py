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

    with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
        try:
            cam = cv2.VideoCapture(1)

            ret, image = cam.read()
            cv2.imwrite(tmp.name, image)

            cam.release()
            cv2.destroyAllWindows()

            return {"success": "true", "path": "data/photo/picture.png"}
        except Exception as e:
            return {"success": "false", "message": f"Hardware error on the WEBCAM occurs: {e}", "path": ""}
        B
