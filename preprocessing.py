
import os


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

    def parse_one_frame(self, lines):
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
            try:
                self.num_of_atoms = int(lines[0])
            except ValueError:
                print("Bad number of atoms.")
                return
            xyz_header_lines = 2
            self.num_frames = int(len(lines) / (self.num_of_atoms + xyz_header_lines))
            for i in range(len(self.num_frames)):
                start_index = 2 + (i * )
                frame_lines = lines[xyz_header]



if __name__ == "__main__":
    input_file = XYZFile("./Resources/malonaldehyde_IRC.xyz")
    print(input_file.num_atoms, input_file.num_frames)