from preprocessing import *
from processing import *
from plotting import *
import os

if __name__ == "__main__":
    input_file = XYZFile("./Resources/malonaldehyde_IRC.xyz")
    print(input_file.frames)
    print(input_file.atom_labels)
