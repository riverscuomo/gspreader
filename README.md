# GSPREADER
## DESCRIPTION
A few helper functions to make gspread even easer to use.

## INSTALLATION
Make sure you have a cred.json file to a google service account.

Set environment variables for 

    `GOOGLE_CREDS_PATH="path_to_your_creds.json"`
    `CLIENT_EMAIL="client_email_from_your_creds.json"`

## USAGE
Share your google spreadsheet with the client_email address in your google credentials file.

Then get a worksheet by name

    `sheet = get_sheet('suzy', 'titles')`

or by index

    `sheet = get_sheet('suzy', 0)`

then get the data

    `data = sheet.get_all_records()`

and then update the data

    `updateRange(sheet, data)`
