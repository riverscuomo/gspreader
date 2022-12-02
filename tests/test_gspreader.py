from gspreader import __version__
from gspreader import *


def test():
    sheet = get_sheet("Language", "phrases")
    print(sheet)

def test_version():
    assert __version__ == '0.1.0'

if __name__ == "__main__":
    test()