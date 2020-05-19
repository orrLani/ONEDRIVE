from __future__ import print_function
import pickle
import os.path
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import Const
from  oauth2client.service_account import ServiceAccountCredentials
import gspread

import gspread_dataframe as gd
from df2gspread import df2gspread as d2g

# to google sheet
import pandas as pd

# if we wanna print nicly
from pprint import pprint

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

# Scope for google Sheet

scope_sheet = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/sprea','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive']


class Sheet:
    def __init__(self):
        creds =ServiceAccountCredentials.from_json_keyfile_name("googleSheet.json",SCOPES)
        self.client=gspread.authorize(creds)
#        self.client.create()
#        self.client.open().add_worksheet()
        sheet = self.client.open("hello").sheet1
        self.my_course_xl = self.client.open("Courses")

    def addNewWorkSheet(self,data:pd.DataFrame,name:str):

        print(data)
        self.my_course_xl.add_worksheet(name,10,10)
        sheet=self.client.open("Courses").worksheet(name)
        data_head_list = list(data.head())
        sheet.insert_row(data_head_list, 1)
        [sheet.insert_row(list(data.iloc[i]),2) for i in range(len((data)))]


    def GetFolderID(self,dic,courseId:str):
        work = str(courseId) + Const.FOLDERID
        sheet = self.client.open("Courses").worksheet(work)
        data = sheet.get_all_values()
        headers = data.pop(0)

        df = pd.DataFrame(data, columns=headers)
        if dic[Const.WHAT_THIS_FILE] == Const.SOLUTION or dic[Const.WHAT_THIS_FILE] == Const.HW:
            google_drive_id_col =  df[df['folderName'] == Const.HWSOLUTION]
        else:
            google_drive_id_col = df[df['folderName'] == dic[Const.WHAT_THIS_FILE]]
        folder_id = google_drive_id_col.iloc[0, 0]
        print(folder_id)
        return folder_id

    def UpdateWorkSheet(self,dic:{}):

        what_this_file = dic[Const.WHAT_THIS_FILE]
        if what_this_file==Const.Toturial or what_this_file==Const.LECTURE:
            work = str(dic[Const.COURSE_ID]) + Const.Toturial_LECTURE_WORK
            sheet = self.client.open("Courses").worksheet(work)
            insertRow=[dic[Const.FOLDERID], dic[Const.FILEID],dic[Const.YEAR],
                       dic[Const.SEMSTER],dic[Const.LECTURE_NAME],
                       dic[Const.WHAT_THIS_FILE],dic[Const.NUMOFLECTURE],
                       dic[Const.PARTOFLECTURE],Const.PATH_TO_FILE_DRIVE,dic[Const.REMARKS]]
            print(insertRow)
            sheet.insert_row(insertRow, 2)

        if what_this_file ==Const.HW or what_this_file==Const.SOLUTION:
            work = str(dic[Const.COURSE_ID]) + Const.HWSOLUTION
            sheet = self.client.open("Courses").worksheet(work)
            insertRow = [dic[Const.FOLDERID], dic[Const.FILEID], dic[Const.YEAR],
                         dic[Const.SEMSTER], dic[Const.LECTURE_NAME],
                         dic[Const.WHAT_THIS_FILE], dic[Const.NUMOFLECTURE],
                         dic[Const.PARTOFLECTURE], Const.PATH_TO_FILE_DRIVE, dic[Const.REMARKS]]
            print(insertRow)
            sheet.insert_row(insertRow, 2)

        #TODO dic["lecture_name"] dic["path of file]
        dict = {
            "course_id": "8220",
            "year": "2018",
            "semster": "A",
            "numOfLecture": "1",
            "partOfLecture": "1",
            "remark": "OrrLaniado",
            "path_to_file": "unit 2.pdf",
            "what_this_file": "Toturial",
            "WhatKind": "ToturialLecture"
        }

      #  google_drive_id_col = df[df['CourseID'] == CourseId]
      #  folder_id = google_drive_id_col.iloc[0, 0]
      #  print(folder_id)
      #  return folder_id



    def InsertCourse(self,FolderId:int,courseId:int,courseName:str):

        sheet = self.client.open("Courses").sheet1
        insertRow=[FolderId,courseId,courseName]
        sheet.insert_row(insertRow,2)
        data = sheet.get_all_records()
        df=pd.DataFrame(data)


    def FindDiractoryID(self,CourseId,folderName):
        pass



    def FindRootDiractoryID(self,CourseId:str):
        # root Find In Courses
        sheet=self.client.open("Courses").sheet1
        data = sheet.get_all_values()
        headers=data.pop(0)
        df = pd.DataFrame(data, columns=headers)
        col=df.loc['CourseID':]==CourseId
        google_drive_id_col = df[df['CourseID'] == CourseId]
        folder_id=google_drive_id_col.iloc[0,0]
        print(folder_id)
        return folder_id


    # google sheet id1B8ROxKr8utzDLM-4mLgapvynDzoiPe4oN8byzgTNx4A
    gsheet_id=""




class GoogleDriveApi:
    def __init__(self):


        self.mySheet=Sheet()
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
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

        self.service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = self.service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])


      #  results_1 =self.service.files().list(pageSize=10, fields="nextPageToken, folder(id, name)").execute()
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))

    def removefile(self):
        page_token = None
        l=[]
        with open('your_file3.txt', 'a', encoding='UTF-8') as f:
            while True:
                response = self.service.files().list(

                                                     spaces='drive',
                                                  fields='nextPageToken, files(id, name)',
                                                  pageToken=page_token).execute()
                for file in response.get('files', []):
                    # Process change

                    s='%s (%s)' % (file.get('name'), file.get('id'))
                    f.write("%s\n" % s)

                    #f.write('%s' % (file.get('name')))
                    l.append(s)
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break
        import csv



if __name__ == '__main__':
    g=GoogleDriveApi()
    g.removefile()
