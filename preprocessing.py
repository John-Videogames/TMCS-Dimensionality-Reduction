

def parse_xyz_file(filename: string):
    """
    Loads in an .xyz file into
    a set of 3N x steps vectors
    :param filename:
    :return:
    """

    with open(filename, "r") as infile:
        line = infile.readline()
        try:
            number_of_atoms = int(line)
            print(number_of_atoms)
        except ValueError:
            print("Bad number of atoms.")
            return

if __name__ == "__main__":
    parse_xyz_file("./Resources/")