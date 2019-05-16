#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TMCS Dimensionality Reduction docstring
"""

from preprocessing import *
from processing import *
from plotting import *

if __name__ == "__main__":
    input_file = XYZFile("./Resources/malonaldehyde_IRC.xyz")
    print(input_file.frames)
    print(input_file.atom_labels)
    print(input_file.atom_masses)