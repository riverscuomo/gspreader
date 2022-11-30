import os
from gspread import service_account
from time import sleep
from rich import print
from config import *


# by string names
def get_sheet(spreadsheet: str, worksheet, client=None):

    """
    Share the google spreadsheet with the client_email address in your google credentials file

    Then get a worksheet by name

        sheet = get_sheet('suzy', 'titles')
    
    or by index

        sheet = get_sheet('suzy', 0)

    then get the data

        data = sheet.get_all_records()

    and then update the data

        updateRange(sheet, data)

    If you supply an authorized client to this function, it will open and return the sheet
    without authorizing a new client.
    """
    print(f"get_sheet '{spreadsheet}'")
    # print("sheet=", sheet)
    # print("worksheet=", worksheet)

    if not client:
        # print("no client supplied, creating one")
        client = get_client()
        # print(client)

    while True:
        try:
            if type(worksheet) == str:
                # print(f"getting sheet <{spreadsheet}> by worksheet name <{worksheet}>")
                sheet = client.open(spreadsheet).worksheet(worksheet)
                break
            elif type(worksheet) == int:
                # print("getting sheet by index")
                sheet = client.open(spreadsheet).get_worksheet(worksheet)
                break
            else:
                print(
                    "You must provide either a sheet name or an index to gspreader get_sheet()."
                )
                print(f"worksheet={worksheet}")
                exit()
        except Exception as e:
            print(e.args)
            if e.args != ():
                print("\n\n")
                print(e)
                print("sleeping for 10 seconds...")
                sleep(10)
            else:
                print(e)
                print(type(e))
                print(vars(e))
                print(type(worksheet))
                print(
                    f"\n\nDid you forget to share the {spreadsheet} with:  \n\n\nOr did you change the name of the worksheet?"
                )
                exit()

    return sheet


def get_client():
    while True:
        try:
            # if os.environ.get("GSPREADER_CREDENTIALS") is None:
            # print("GSPREADER_CREDENTIALS not set")
            # exit()

            # print("signing into google...")
            client = service_account(GOOGLE_CREDS_PATH)
            break
        except Exception as e:
            print(e)
            print("wait to try again")
            print( f"Did you forget to share the sheet with {CLIENT_EMAIL}"             )
            sleep(1)
    return client


def error_routine(e):
    print(e)
    print("sleeping...")
    sleep(2)

# def updateRange2(sheet, data, **kwargs):
def updateRange(sheet, data, **kwargs):
    """I guess this is the one?
    has the alias update_range
    """
    # print("updateRange2")

    value_input_option = get_options(kwargs)

    # Python >= 3.5 alternative: unpack dictionary keys into a list literal [*newdict]
    # arbitrarily using the first data row to get the keys
    headers = [*data[0]]
    # print(headers)

    row_count = len(data) + 1  # add one to the row for headers
    col_count = len(headers)  # len(sheet_columns)

    # Get the range based on number of rows in the data
    # and the number of columns in the sheet
    while True:
        try:
            cell_range = sheet.range(2, 1, row_count, col_count)
            break
        except Exception as e:
            error_routine(e)

    # flatten the list of dicts into a list of values in order
    flattened_data = flatten_data(data, headers)
    # print(flattened_data)

    populate_cells(cell_range, flattened_data)

    print("now print the updated range to the sheet ", value_input_option)
    # sheet.update_cells(range_of_cells) # DATA WILL be put into the formulas
    sheet.update_cells(cell_range, value_input_option=value_input_option)

    # DATA WILL be put into the formulas
    # sheet.update_cells(range_of_cells, value_input_option='RAW') # data will be pasted as text

    # newly added to shrink the sheet to. BUT WHAT IF YOU HAVE 2 HEADERS OR MORE?
    sheet.resize(rows=len(data) + 1)


def setRange(sheet, data, **kwargs):
    """
    including the headers
    """
    print("setRange")

    value_input_option = get_options(kwargs)

    # Python >= 3.5 alternative: unpack dictionary keys into a list literal [*newdict]
    # arbitrarily using the first data row to get the keys
    headers = [*data[0]]
    # print(len(headers))

    row_count = len(data) + 1  # add one to the row for headers
    col_count = len(headers)  # len(sheet_columns)
    # col_count = 33
    # print(row_count * col_count)

    # Get the range based on number of rows in the data
    # and the number of columns in the sheet
    while True:
        try:
            cell_range = sheet.range(1, 1, row_count, col_count)
            break
        except Exception as e:
            error_routine(e)

    # # flatten the list of dicts into a list of values in order
    flattened_data = set_flatten_data(data, headers)
    # print(flattened_data)
    # print(f"row count: {row_count}")
    # print(f"col count: {col_count}")
    populate_cells(cell_range, flattened_data)

    # for cell in cell_range:
    #     cell.value = "yeah"

    print("now print the updated range to the sheet ", value_input_option)
    # sheet.update_cells(range_of_cells) # DATA WILL be put into the formulas
    sheet.update_cells(cell_range, value_input_option=value_input_option)

    # DATA WILL be put into the formulas
    # sheet.update_cells(range_of_cells, value_input_option='RAW') # data will be pasted as text

    # newly added to shrink the sheet to. BUT WHAT IF YOU HAVE 2 HEADERS OR MORE?
    sheet.resize(rows=len(data) + 1)


def get_options(kwargs):
    if kwargs:
        if kwargs["value_input_option"]:
            value_input_option = kwargs["value_input_option"]
    else:
        value_input_option = "USER_ENTERED"
    return value_input_option


def populate_cells(cell_range, flattened_data):
    # print("updating the cell data in the range")
    # print(f"len(cellrange) = {len(cell_range)}")
    # print(f"len(flattened_data) = {len(flattened_data)}")
    for i, cell in enumerate(cell_range):
        cell.value = flattened_data[i]


def flatten_data(data, headers):
    flattened_data = []

    for row in data:
        for column in headers:
            try:
                flattened_data.append(row[column])
            except Exception:
                flattened_data.append("")  # I just added this try except thing
    return flattened_data


def set_flatten_data(data, headers):
    # print("set_flatten_data")
    flattened_data = []
    flattened_data.extend(headers)

    # flattened_data = []
    # print(headers)

    # for h in headers:
    #     print(h)
    # exit()

    for row in data:
        for h in headers:
            try:
                flattened_data.append(row[h])
            except Exception:
                print("failed at column: ", h)
                flattened_data.append("")
    return flattened_data

def test():
    sheet = get_sheet("Language", "phrases")
    print(sheet)


"""
YOU CAN'T ADD COLUMNS WITH UPDATE RANGE SO USE SOMETHING LIKE THIS
updated_header_row = headers + new_channel_names
print(updated_header_row)

sheet.update("A1:ZZ1", [updated_header_row])


"""



# def updateRange(sheet, data, **kwargs):
#     """deprecated? but some functions still call it?"""
#     print("you're in the wrong updateRange()")

#     if kwargs:
#         if kwargs["value_input_option"]:
#             value_input_option = kwargs["value_input_option"]
#     else:
#         value_input_option = "USER_ENTERED"

#     while True:
#         try:
#             sheet_columns = sheet.row_values(1)
#             break
#         except Exception as e:
#             error_routine(e)

#     row_count = len(data) + 1  # add one to the row for headers
#     col_count = len(sheet_columns)

#     while True:
#         try:
#             cell_range = sheet.range(2, 1, row_count, col_count)
#             break
#         except Exception as e:
#             error_routine(e)

#     # flatten the list of dicts into a list of values in order
#     flattened_data = []

#     for row in data:
#         for column in sheet_columns:
#             try:
#                 flattened_data.append(row[column])
#             except Exception as e:
#                 flattened_data.append("")

#     print("updating the cell data in the range")
#     for i, cell in enumerate(cell_range):
#         cell.value = flattened_data[i]

#     # THIS BLOCK IS JUST FOR CLEARING THE SHEET
#     print(f"clearing the {sheet} sheet")
#     # you may have to increase row_count if the updated sheet has fewer rows than the original sheet
#     range_of_cells = sheet.range(2, 1, row_count, col_count)
#     for cell in range_of_cells:
#         cell.value = ""
#     sheet.update_cells(range_of_cells)

#     print("now print the updated range to the sheet ", value_input_option)
#     # sheet.update_cells(range_of_cells) # DATA WILL be put into the formulas
#     sheet.update_cells(
#         cell_range, value_input_option=value_input_option
#     )  # DATA WILL be put into the formulas
#     # sheet.update_cells(range_of_cells, value_input_option='RAW') # data will be pasted as text
#     # newly added to shrink the sheet to. BUT WHAT IF YOU HAVE 2 HEADERS OR MORE?
#     sheet.resize(rows=len(data) + 1)