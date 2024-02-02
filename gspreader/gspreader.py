# import os
from gspread import service_account, service_account_from_dict
from time import sleep
from rich import print
from gspreader.config import *
import json
import traceback

def get_sheet(spreadsheet: str, worksheet: str | int, client=None):
    """
    Share the google spreadsheet with the client_email address in your google credentials file

    Then get a worksheet by name

        sheet = get_sheet('suzy', 'titles')

    or by index

        sheet = get_sheet('suzy', 0)

    then get the data

        data = sheet.get_all_records()

    If you supply an authorized client to this function, it will open and return the sheet
    without authorizing a new client.
    """
    print(f"get_sheet '{spreadsheet}'")
    # print("sheet=", sheet)
    # print("worksheet=", worksheet)

    if not client:
        print("no client supplied, creating one")
        client = get_client()
        # print(client)

    # while True:
    try:
        if type(worksheet) == str:
            print(f"getting sheet '{spreadsheet}' by worksheet name '{worksheet}'")
            sheet = client.open(spreadsheet).worksheet(worksheet)
            # break
        elif type(worksheet) == int:
            print("getting sheet by index")
            sheet = client.open(spreadsheet).get_worksheet(worksheet)
            # break
        else:
            print(
                "You must provide either a sheet name or an index to gspreader get_sheet()."
            )
            print(f"worksheet={worksheet}")
            exit()
    except Exception as e:
        # print(e.args)
        print(f"failed to get sheet with error: {traceback.format_exc()}")
        if e.args != ():
            # print("\n\n")
            print(e)
            # print("sleeping for 10 seconds...")
            # sleep(10)
            # exit()
        else:
            print(e)
            print(type(e))
            print(vars(e))
            print(type(worksheet))
            print(
                f"\n\nDid you forget to share the {spreadsheet} with {GSPREADER_GOOGLE_CLIENT_EMAIL}:  \n\n\nOr did you change the name of the worksheet?"
            )
        exit()
    print("\n")
    return sheet

def get_sheet_and_client(spreadsheet: str, worksheet: str | int, client=None):
    """
    Share the google spreadsheet with the client_email address in your google credentials file

    Then get a worksheet by name

        sheet = get_sheet('suzy', 'titles')

    or by index

        sheet = get_sheet('suzy', 0)

    then get the data

        data = sheet.get_all_records()

    If you supply an authorized client to this function, it will open and return the sheet
    without authorizing a new client.
    """
    print(f"get_sheet '{spreadsheet}'")
    # print("sheet=", sheet)
    # print("worksheet=", worksheet)

    if not client:
        print("no client supplied, creating one")
        client = get_client()
        # print(client)

    sheet = get_sheet(spreadsheet, worksheet, client)
    return sheet, client


def get_client():
    print("get_client()")
    # while True:
    try:
        print("signing in with GSPREADER_GOOGLE_CREDS_PATH...")
        client = service_account(GSPREADER_GOOGLE_CREDS_PATH)
    except:
        # print(f"failed with GSPREADER_GOOGLE_CREDS_PATH: {GSPREADER_GOOGLE_CREDS_PATH}")
        try:
            print("signing in with GSPREADER_GOOGLE_CREDS...")
            # generate json - if there are errors here remove newlines in .env
            json_data = json.loads(GSPREADER_GOOGLE_CREDS)
            # the private_key needs to replace \n parsed as string literal with escaped newlines
            json_data['private_key'] = json_data['private_key'].replace('\\n', '\n')

            client = service_account_from_dict(json_data)
        except:
            print(f"failed with GSPREADER_GOOGLE_CREDS: {GSPREADER_GOOGLE_CREDS}")
            print(traceback.format_exc())
            exit()

        # break
        # except Exception as e:
        #     print(e)
        #     print("wait to try again")
        #     print(
        #         f"Did you forget to share the sheet with {GSPREADER_GOOGLE_CLIENT_EMAIL}")
        #     sleep(1)
    return client


def error_routine(e):
    print(e)
    print("sleeping...")
    sleep(2)


def set_range(sheet, data, **kwargs):
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
    # while True:
    #     try:
    #         cell_range = sheet.range(1, 1, row_count, col_count)
    #         break
    #     except Exception as e:
    #         error_routine(e)

    try:
        cell_range = sheet.range(1, 1, row_count, col_count)
        # break
    except Exception as e:
        print(traceback.format_exc())
        exit()
        # error_routine(e)

    # # flatten the list of dicts into a list of values in order
    flattened_data = set_flatten_data(data, headers)
    # print(flattened_data)
    # print(f"row count: {row_count}")
    # print(f"col count: {col_count}")
    populate_cells(cell_range, flattened_data)

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
    return cell_range


def flatten_data(data, headers):
    """ flatten the list of dicts into a list of values IN ORDER OF THE sheet headers"""
    flattened_data = []

    for row in data:
        for column in headers:
            try:
                flattened_data.append(row[column])
            except Exception:
                flattened_data.append("")
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


def update_range(sheet, data, head: int = 1, **kwargs):
    """
    """
    # print("update_range")

    value_input_option = get_options(kwargs)

    # ## THIS DOESN'T WORK WHEN THE DATA.HEADERS AND THE SHEET.HEADERS ARE IN A DIFFERENT ORDER
    # ## BASICALLY THE KEYS CAN'T CHANGE AFTER YOU GET THE SHEET
    # # # Python >= 3.5 alternative: unpack dictionary keys into a list literal [*newdict]
    # # # arbitrarily using the first data row to get the keys
    # data_headers = [*data[0]]

    # sheet_headers = sheet.row_values(1)

    # # headers = sheet_headers if data_headers != sheet_headers else data_headers
    # print(data_headers == sheet_headers)
    # # print(headers)
    # print("data headers: ", data_headers)
    # print("sheet headers: ", sheet_headers)
    # # exit()
    while True:
        try:
            headers = sheet.row_values(head)
            break
        except Exception as e:
            print(e)
            print("sleeping...")
            sleep(2)

    # headers = sheet_headers

    row_count = len(data) + 1  # add one to the row for headers
    col_count = len(headers)  # len(sheet_columns)

    first_data_row = head + 1 # in case the header row is below the first row

    # # Get the range based on number of rows in the data and the number of columns in the sheet
    # while True:
    #     try:
    #         cell_range = sheet.range(first_data_row, 1, row_count, col_count)
    #         break
    #     except Exception as e:
    #         error_routine(e)

    try:
        cell_range = sheet.range(first_data_row, 1, row_count, col_count)

    except Exception as e:
        # error_routine(e)
        print(traceback.format_exc())
        exit()

    # 
    flattened_data = flatten_data(data, headers)
    # print(flattened_data)

    cell_range = populate_cells(cell_range, flattened_data)

    print("now print the updated range to the sheet ", value_input_option)

    try:
        # sheet.update_cells(range_of_cells) # DATA WILL be put into the formulas
        sheet.update_cells(cell_range, value_input_option=value_input_option)
    except Exception as e:
        print(traceback.format_exc())
        exit()

    # DATA WILL be put into the formulas
    # sheet.update_cells(range_of_cells, value_input_option='RAW') # data will be pasted as text

    # Shrink the sheet to the size of the data plus the header row(s)
    sheet.resize(rows=len(data) + head)


def sanitize_key(s: str):
    s = s.lower()
    bads = ["'", '"', "(", ")", ":", ";", "!", "?", "’", "“", "”", "‘", "–", "—", "…", ",", ".", " ", "-"]
    for b in bads:
        s = s.replace(b, "")
    return s


def update_sheet_data_by_matching_key(sheet_data: list, new_data: list, key: str):
    """ update the sheet_data with the new_data (if there's a matching row in the new data)"""
    print("update_sheet_data...")
    for row in sheet_data:
        for new_row in new_data:
            if sanitize_key(str(row[key])) == sanitize_key(str(new_row[key])):
                # print(f"Updating {row[key]}")

                # Update the columns for this song in this new_row
                row.update(new_row)
    return sheet_data
