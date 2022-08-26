#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on  2/6/22 10:02

@author: Edward L. Campbell Hernández
contact: ecampbelldsp@gmail.com
"""

import pkce

code_verifier = pkce.generate_code_verifier(length=128)
code_challenge = pkce.get_code_challenge(code_verifier)

a=1