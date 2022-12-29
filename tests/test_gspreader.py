from gspreader import __version__
from gspreader import *


def test_update_range():
    # sheet = get_sheet("gspread test", 0)
    sheet = get_sheet("Song List","demos")
    print(sheet)
    data = sheet.get_all_records()
    print(data[0])
    update_range(sheet, data)


def test():

    sheet = get_sheet("Language", "phrases")
    print(sheet)

def test_version():
    assert __version__ == '0.1.0'

if __name__ == "__main__":
    test()

    test_update_range()