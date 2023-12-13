import time
from gspreader import __version__
from gspreader import *

"""
 pytest tests/test_gspreader.py
"""

spreadsheet = 'Klas Title Demos Ratings Comments'
def test_update_range():
    # sheet = get_sheet("gspread test", 0)
    sheet = get_sheet(spreadsheet,0)
    print(sheet)
    data = sheet.get_all_records()
    print(data[0])
    update_range(sheet, data)

def test_multiple():


    for i in range(10):
        print('\n\ni = ', i)
        sheet = get_sheet(spreadsheet, 0)       
        
        sheet = get_sheet(spreadsheet, 0)
        print (sheet)
        print(sheet.row_values(1))
        time.sleep(2)

def test():

    sheet = get_sheet(spreadsheet, 0)
    print(sheet)

def test_version():
    assert __version__ == '0.1.0'

# if __name__ == "__main__":
#     test_version()
    # test_multiple()

    # test_update_range()