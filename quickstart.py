from __future__ import print_function
from __future__ import print_function
import httplib2
import os, io

from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import auth
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)


def listFiles(size):
    results = drive_service.files().list(
        pageSize=size,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    output = []
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            output.append(item['id'])
            print('{0} ({1})'.format(item['name'], item['id']))

    return output

def searchFile(size,query):
    results = drive_service.files().list(
    pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item)
            print('{0} ({1})'.format(item['name'], item['id']))

from googleapiclient import errors

def deleteFile(id):
    try:
        drive_service.files().delete(fileId=id).execute()
        print('Delete %s success' %(id))
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


while True:
    input = listFiles(1)
    for i in input:
        deleteFile(i)
    break