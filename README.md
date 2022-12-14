To publish to PyPi you have to pass the creds for pypi
poetry build
poetry publish --username(not email) --password

If poetry is installed in a python you no longer have (no poetry commands recognized)):
curl -sSL https://install.python-poetry.org | python - --uninstall
Install via powershell:
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# GSPREADER
## DESCRIPTION
A few helper functions to make gspread even easer to use.

## INSTALLATION
Make sure you have a cred.json file to a google service account.

Set environment variables for 

    GSPREADER_GOOGLE_CLIENT_EMAIL=client_email_from_your_creds.json

    GSPREADER_GOOGLE_CREDS=the dict of your creds (in the case that you've deployed to Heroku and you've set the creds dict as an env var)
    OR
    GSPREADER_GOOGLE_CREDS_PATH=path_to_your_creds.json
    

## USAGE
Share your google spreadsheet with the client_email address in your google credentials file.

Then get a worksheet by name

    `sheet = get_sheet('suzy', 'titles')`

or by index

    `sheet = get_sheet('suzy', 0)`

then get the data

    `data = sheet.get_all_records()`

and then update the data

    `update_range(sheet, data)`
