class XYZFile:
    """
    Class for an xyz file that
    creates a trajectory.
    """
    def __init__(self, filename):
        self.filename = filename
        self.num_atoms = 0  # Set this in "parse_xyz_file"
        self.num_frames = 0
        self.frames = self.parse_xyz_file(filename)

    def __str__(self):
        return f"{self.filename}, with {self.num_atoms} atoms in {self.num_frames} frames"

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

        assert filename.endswith(".xyz"), "File must be in .xyz format."

        with open(filename, "r") as infile:
            lines = infile.readlines()
            try:
                self.num_atoms = int(lines[0])
            except ValueError:
                raise ValueError('Cannot convert num_atoms in line 0 to an integer')

            assert self.num_atoms != 0, "num_atoms in line 0 cannot be 0."
            assert self.num_atoms > 0, "num_atoms in line 0 cannot be negative."

            xyz_header_lines = 2

            self.num_frames = int(len(lines) / (self.num_atoms + xyz_header_lines))
            # Make sure we have got a sensible integer, and not a floating
            # point number.
            assert self.num_frames == len(lines) / (self.num_atoms + xyz_header_lines)

            frames = []
            for i in range(self.num_frames):
                start_index = i * (self.num_atoms + xyz_header_lines) + xyz_header_lines
                end_index = (i + 1) * (self.num_atoms + xyz_header_lines)

                frame_num_atoms_index = start_index - 2
                frame_num_atoms = int(lines[frame_num_atoms_index])
                assert frame_num_atoms == self.num_atoms, f"""
                                                           num_atoms at line {frame_num_atoms_index }inconsistent.
                                                           Got {frame_num_atoms}, expected {self.num_atoms}.
                                                           """

                frame_lines = lines[start_index: end_index]
                frame = self.parse_one_frame(frame_lines)
                frames.append(frame)
                assert len(frame_lines) == self.num_atoms

        return frames


if __name__ == "__main__":
    input_file = XYZFile("./Resources/malonaldehyde_IRC.xyz")
    print(input_file)
