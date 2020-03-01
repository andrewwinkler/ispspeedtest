#!/usr/bin/env python3

import csv
import os.path
import pickle
import subprocess

from googleapiclient import discovery
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1a-wVlpRJYVamcDs-SX2MpfW26teERmuKC3YUVXx80Yg'
RANGE = 'raw_data!A1:J1'
VALUE_INPUT_OPTION = 'USER_ENTERED'
INSERT_DATA_OPTION = 'INSERT_ROWS'

COMMAND = ['speedtest-cli', '--csv']


def get_credentials():
    credentials = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    return credentials


def get_speed_data():
    data = subprocess.run(COMMAND, stdout=subprocess.PIPE).stdout.decode('UTF-8')
    data = csv.reader([data], delimiter=',')
    return [row for row in data]


def main():
    service = discovery.build('sheets', 'v4', credentials=get_credentials())

    value_range_body = {
        'range': RANGE,
        'majorDimension': 'ROWS',
        'values': get_speed_data()
    }

    request = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE,
        valueInputOption=VALUE_INPUT_OPTION,
        insertDataOption=INSERT_DATA_OPTION,
        body=value_range_body
    )
    request.execute()


if __name__ == "__main__":
    main()
