import os
import shutil
import sys
import subprocess

POSSIBLE_FILES = ['./Resources/trajectory_2019-05-16_03-49-27-PM.xyz',
                  './Resources/trajectory_2019-05-16_03-44-22-PM.xyz',
                  './Resources/trajectory_2019-05-16_03-43-00-PM.xyz',
                  './Resources/trajectory_2019-05-16_03-03-39-PM.xyz',
                  './Resources/trajectory_2019-05-16_03-48-20-PM.xyz',
                  './Resources/trajectory_2019-05-16_03-48-54-PM.xyz',
                  './Resources/trajectory_2019-05-16_03-04-45-PM.xyz']


for possible_file in POSSIBLE_FILES:
    basename = os.path.split(possible_file)[-1]
    basename, ext = os.path.splitext(basename)
    for subfile in os.listdir("./Resources/components/"):
        if subfile.startswith(basename):
            print("Rendering", subfile)
            filetext= f"""package require vmdmovie 
                          display resize 512 512
                          mol new ./Resources/{basename}{ext} waitfor all autobonds off
                          axes location off
                          mol representation DynamicBonds 1.5 0.2 24
                          mol addrep top
                          mol representation CPK 1.0 24 0.3 24
                          mol addrep top
                          mkdir -p /tmp/mytmpdir 
                          ::MovieMaker::makemovie /tmp/mytmpdir example ppmtogif libtachyon 10 trajectory 
                          set ::MovieMaker::framerate 24 
                          set ::MovieMaker::trjstep 1 
                          set ::MovieMaker::userframe 0 
                          set ::MovieMaker::numframes [molinfo top get numframes] 
                          exit"""
            with open("moviemaker.tcl", "w") as outfile:
                outfile.write(filetext)

            result = subprocess.check_call(["vmd", "-e", "moviemaker.tcl"], stdout=None)
            shutil.copyfile("/tmp/mytmpdir/example.gif", f"./Outputs/gifs/{subfile}.gif")
