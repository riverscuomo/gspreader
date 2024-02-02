# Gspreader [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)

## To publish to PyPi you have to pass the creds for pypi
1. Update your package files with the necessary changes (code, documentation, tests, etc.).

2. Update the version number of your package in the `pyproject.toml` file. Semantic versioning (MAJOR.MINOR.PATCH) is a common strategy for version numbers. For example:
    ```toml
    [tool.poetry]
    name = "your-package-name"
    version = "1.0.1"  # update this with the new version
    description = "Your package description"
    # ... other metadata
    ```

3. Commit your changes to your version control system (e.g., Git). It's a good practice to tag your release with the version number:
    ```bash
    git commit -am "Update package to version 1.0.1"
    git tag -a 1.0.1 -m "Release version 1.0.1"
    git push origin master --tags
    ```
4. poetry build
5. poetry publish --username riverscuomo --password <yourpassword>

If poetry is installed in a python you no longer have (no poetry commands recognized)):
curl -sSL https://install.python-poetry.org | python - --uninstall
Install via powershell:
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

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
