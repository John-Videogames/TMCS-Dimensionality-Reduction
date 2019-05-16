
import numpy as np
from collections import defaultdict

def cast_num_atoms(num_atoms):
    """
    Validates a string number of atoms
    to make sure it is a valid, positive
    integer, and then returns it.
    :param num_atoms:
    :return:
    """
    try:
        int(num_atoms)
    except ValueError:
        raise ValueError(f"Cannot turn {num_atoms} into an integer")
    if int(num_atoms) != float(num_atoms):
        raise ValueError(f"{num_atoms} is floating point number, not an int")

    num_atoms = int(num_atoms)
    if num_atoms == 0:
        raise ValueError(f"num_atoms cannot be zero.")

    if num_atoms < 0:
        raise ValueError(f"num_atoms cannot be negative.")

    return num_atoms


class XYZFile:
    """
    Class for an xyz file that
    creates a trajectory.
    """
    def __init__(self, filename):
        self.filename = filename
        self.num_atoms = 0  # Set this in "parse_xyz_file"
        self.num_frames = 0
        self.atom_labels = None
        self.frames = self.parse_xyz_file(filename)

    def __str__(self):
        return f"{self.filename}, with {self.num_atoms} atoms in {self.num_frames} frames"

    def parse_atom_labels(self, lines):
        """
        Parses a simple frame into a
        3N array of which atomic is in which
        position.
        :param lines:
        :return:
        """
        seen_atoms = defaultdict(lambda: 0)
        atom_labels = []
        for line in lines:
            atom = line.split()[0]
            seen_atoms[atom] += 1
            atom = f"{atom}{seen_atoms[atom]}"
            atom_labels.extend([f"{atom}_x", f"{atom}_y", f"{atom}_z"])
        return atom_labels

    def parse_one_frame(self, lines):
        """
        Parses a simple frame into
        a 3xN vector.
        :param: num_atoms
        :param lines:
        :return:
        """
        frame = []
        for line in lines:
            elements = line.split()[1:]
            elements = np.asfarray(elements,float)
            frame.extend(elements)
        return np.array(frame)


    def parse_xyz_file(self, filename):
        """
        Loads in an .xyz file into
           a set of 3N x steps vectors
        :param filename:
        :return:
        """

        assert filename.endswith(".xyz"), "File must be in .xyz format."

        with open(filename, "r") as infile:
            lines = infile.readlines()
            self.num_atoms = cast_num_atoms(lines[0])

            xyz_header_lines = 2

            self.num_frames = int(len(lines) / (self.num_atoms + xyz_header_lines))
            # Make sure we have got a sensible integer, and not a floating
            # point number.
            assert self.num_frames == len(lines) / (self.num_atoms + xyz_header_lines)

            frames = np.empty([self.num_frames, self.num_atoms * 3])
            self.atom_labels = self.parse_atom_labels(lines[xyz_header_lines: xyz_header_lines+self.num_atoms])
            for i in range(self.num_frames):
                start_index = i * (self.num_atoms + xyz_header_lines) + xyz_header_lines
                end_index = (i + 1) * (self.num_atoms + xyz_header_lines)

                frame_num_atoms_index = start_index - 2
                frame_num_atoms = cast_num_atoms(lines[frame_num_atoms_index])
                assert frame_num_atoms == self.num_atoms, f"""
                                                           num_atoms at line {frame_num_atoms_index }inconsistent.
                                                           Got {frame_num_atoms}, expected {self.num_atoms}.
                                                           """

                frame_lines = lines[start_index: end_index]
                frame = self.parse_one_frame(frame_lines)
                frames[i, :] = frame
                assert len(frame_lines) == self.num_atoms

        return frames


if __name__ == "__main__":
    input_file = XYZFile("./Resources/malonaldehyde_IRC.xyz")
