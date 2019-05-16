from preprocessing import *

def test_first_index():
    try:
        XYZFile("./Test_Resources/bad_firstindex.xyz")
    except ValueError:
        return True

def test_later_index():
    try:
        XYZFile("./Test_Resources/bad_laterindex.xyz")
    except AssertionError:
        return True

def test_inconsistent_lines():
    try:
        XYZFile("./Test_Resources/inconsistent_lines.xyz")
    except AssertionError:
        return True

if __name__ == "__main__":
    test_first_index()
    test_later_index()