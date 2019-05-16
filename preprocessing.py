
import os
import numpy as np

class XYZFile():
    """
    Class for an xyz file that
    creates a trajectory.
    """
    def __init__(self, filename):
        self.filename = filename
        self.num_atoms = 0 # Set this in "parse_xyz_file"
        self.num_frames = 0
        self.frames = self.parse_xyz_file(filename)

    def __str__(self):
        return f"{self.filename}, with {self.num_atoms} atoms in {self.num_frames} frames"

    def parse_one_frame(self, lines):
        frame = np.array([3 * len(lines)])
        #for line in lines:
        elements = lines[0].split()
        del elements[0]
        elements=np.array(elements)
        elements = np.array(elements)
        elements.astype(np.float)
        x=elements[0]+elements[1]
        #print(x)

        print(elements)
        """
        Parses a simple frame into
        a 3xN vector.
        :param: num_atoms
        :param lines:
        :return:
        """

    def parse_xyz_file(self, filename):
        """
        Loads in an .xyz file into
        a set of 3N x steps vectors
        :param filename:
        :return:
        """

        with open(filename, "r") as infile:
            lines = infile.readlines()
            print(lines[3])
            try:
                self.num_atoms = int(lines[0])
            except ValueError:
                print("Bad number of atoms.")
                return
            xyz_header_lines = 2
            self.num_frames = int(len(lines) / (self.num_atoms + xyz_header_lines))
            frames = np.empty([self.num_atoms * 3, self.num_frames])
            print(frames.shape)
            for i in range(self.num_frames):
                start_index = i * (self.num_atoms + xyz_header_lines) + xyz_header_lines
                end_index = (i + 1) * (self.num_atoms + xyz_header_lines)
                frame_lines = lines[start_index : end_index]
                frame = self.parse_one_frame(frame_lines)
                assert len(frame_lines) == self.num_atoms



if __name__ == "__main__":
    input_file = XYZFile("./Resources/malonaldehyde_IRC.xyz")
    print(input_file)