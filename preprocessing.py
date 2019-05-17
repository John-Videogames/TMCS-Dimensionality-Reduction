#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pre-processing of xyz files into
a object wrapping a 3N x M 
numpy array.
"""

import numpy as np
from collections import defaultdict
import periodictable
import rmsd


def cast_positive_int(in_string) -> int:
    """
    Checks that a string is a valid
    positive integer
    :param in_string:
    :type in_string: object
    :return:
    """
    try:
        int(in_string)
    except ValueError:
        raise ValueError(f"Cannot turn {in_string} into an integer")
    if int(in_string) != float(in_string):
        raise ValueError(f"{in_string} is floating point number, not an int")

    out_int = int(in_string)
    if out_int == 0:
        raise ValueError(f"This integer cannot be zero.")

    if out_int < 0:
        raise ValueError(f"This integer cannot be negative.")

    return out_int


class XYZFile:
    """
    Class for an xyz file that
    creates a trajectory.
    """
    def __init__(self, filename, translate=True):
        self.filename = filename
        self.num_atoms = 0  # Set this in "parse_xyz_file"
        self.num_frames = 0
        self.atom_types = None
        self.energy_frames = []
        self.frames = self.parse_xyz_file(filename, translate)
        self.energy_frames = np.array(self.energy_frames)
        self.minimise_rmsd()

    def __str__(self):
        return f"{self.filename}, with {self.num_atoms} atoms in {self.num_frames} frames"

    def minimise_rmsd(self, method="kabsch"):
        """
        Rotates the frames to minimise their
        RMSD from the first frame, mutating the input
        structure.
        :param method:
        :return:
        """
        if method == "kabsch":
            rotation_func = rmsd.kabsch_rotate
        elif method == "quaternion_rmsd":
            rotation_func = rmsd.quaternion_rotate
        else:
            raise ValueError("Bad rotation method provided.")

        first_frame = self.frames[0, :].reshape(-1, 3)
        for i, other_frame in enumerate(self.frames[1:, :], 1):
            other_frame = other_frame.reshape(-1, 3)
            other_frame = rotation_func(other_frame, first_frame).ravel()
            self.frames[i, :] = other_frame

    @property
    def atom_masses(self):
        """
        Returns a list of atomic masses using
        the periodictable module (and a small
        quantity of filthy black magic)
        :return:
        """
        return np.array([getattr(periodictable, symbol).mass for symbol in self.atom_types])

    @property
    def atom_labels(self) -> list:
        """
        Parses a simple frame into a
        3N array of which atom is in which
        position.
        :return:
        """
        seen_atoms = defaultdict(lambda: 0)
        atom_labels = []
        for atom in self.atom_types:
            atom_count = seen_atoms[atom]
            seen_atoms[atom] += 1
            atom = f"{atom}{atom_count}"
            atom_labels.extend([f"{atom}_x", f"{atom}_y", f"{atom}_z"])
        assert len(atom_labels) == self.num_atoms * 3, "Did not find 3N atomic labels."
        return atom_labels

    def parse_atom_types(self, lines: list) -> list:
        """
        Parses a simple frame into a
        a list of atom types.
        :param lines:
        :return:
        """
        atom_types = [line.split()[0].strip() for line in lines]
        assert len(atom_types) == self.num_atoms, f"Did not find {self.num_atoms} atomic types."
        return atom_types

    def appendEnergy(self, line):
        """
                Appends to energy_frames  the energy of each frame
                :param lines:
                :param
                :return:
                """
        try:
            self.energy_frames.append(float(line.split()[8]))
        except AttributeError:
            self.energy_frames.append(None)

    @staticmethod
    def parse_one_frame(lines: list, translate):
        """
        Parses a simple frame into
        a 3xN vector.
        :param lines:
        :param translate: -- Do we shift with respect
        to the centroid of the molecule.
        :return:
        """
        frame = []
        for line in lines:
            elements = line.split()[1:]
            elements = np.asfarray(elements, float)
            frame.extend(elements)
        frame = np.array(frame).reshape(-1, 3)
        if translate:
            frame -= rmsd.centroid(frame)

        return frame.ravel()

    def parse_xyz_file(self, filename: str, translate: bool):
        """
        Loads in an .xyz file into
        a set of 3N atom coordinates x M steps.
        :param filename:
        :param translate:
        :return:
        """

        assert filename.endswith(".xyz"), "File must be in .xyz format."
        xyz_header_lines = 2
        with open(filename, "r") as infile:
            lines = infile.readlines()
            self.num_atoms = cast_positive_int(lines[0])

            self.num_frames = cast_positive_int(len(lines) / (self.num_atoms + xyz_header_lines))

            frames = np.empty([self.num_frames, self.num_atoms * 3])
            self.atom_types = self.parse_atom_types(lines[xyz_header_lines: xyz_header_lines + self.num_atoms])
            for i in range(self.num_frames):
                start_index = i * (self.num_atoms + xyz_header_lines) + xyz_header_lines
                end_index = (i + 1) * (self.num_atoms + xyz_header_lines)

                frame_num_atoms_index = start_index - 2
                frame_num_atoms = cast_positive_int(lines[frame_num_atoms_index])
                assert frame_num_atoms == self.num_atoms, f"""
                                                           num_atoms at line {frame_num_atoms_index }inconsistent.
                                                           Got {frame_num_atoms}, expected {self.num_atoms}.
                                                           """

                frame_lines = lines[start_index: end_index]
                frame = self.parse_one_frame(frame_lines, translate)
                frames[i, :] = frame
                assert len(frame_lines) == self.num_atoms
                try:
                    self.appendEnergy(lines[i * (self.num_atoms + xyz_header_lines) + 1])
                except IndexError:
                    self.appendEnergy(None)

        return frames

    def write_out(self, file_name):
        """
        Writes out the contents of this
        to a new xyz file
        :param file_name:
        :return:
        """
        with open(file_name, 'w') as out_file:
            for frame in self.frames:
                out_file.write(str(self.num_atoms)+'\n')
                out_file.write('Shifted XYZ\n')
                for index in range(len(frame)//3):
                    label = self.atom_types[index]
                    x = frame[3 * index]
                    y = frame[3 * index + 1]
                    z = frame[3 * index + 2]
                    out_file.write(f"{label}\t{x}\t{y}\t{z}\n")


if __name__ == "__main__":
    input_file = XYZFile("./Resources/trajectory_2019-05-16_03-03-39-PM.xyz",
                         translate=True)
    print(input_file.atom_masses)
    print(input_file.atom_labels)
    print(input_file.atom_types)

    print(input_file.num_atoms)
    print(input_file.energy_frames)
    print(input_file.frames[0])

    input_file_2 = XYZFile("./Resources/malonaldehyde_IRC.xyz")
    print(input_file_2.energy_frames)
