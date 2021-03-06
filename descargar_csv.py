#!/usr/bin/env python3

from __future__ import print_function
import pickle
import csv
import os
import os.path
from os.path import join, dirname
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SPREADSHEET_RANGE_NAME = os.getenv('SPREADSHEET_RANGE_NAME')
OUT_FILE_NAME = 'inventario.csv'

def login():
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.pickle'):
      with open('token.pickle', 'rb') as token:
          creds = pickle.load(token)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
          flow = InstalledAppFlow.from_client_secrets_file(
              'credentials.json', SCOPES)
          creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open('token.pickle', 'wb') as token:
          pickle.dump(creds, token)

  return creds


def main():
    creds = login()
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=SPREADSHEET_RANGE_NAME).execute()
    values = result.get('values', [])

    with open(OUT_FILE_NAME, "w", newline="") as f:
      writer = csv.writer(f)
      writer.writerows(values)


if __name__ == '__main__':
    main()
