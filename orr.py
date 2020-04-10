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
        google_drive_id_col = df[df['folderName'] == dic[Const.WHAT_THIS_FILE]]
        folder_id = google_drive_id_col.iloc[0, 0]
        print(folder_id)
        return folder_id

    def UpdateWorkSheet(self,dic:{}):

        if(dic[Const.WHAT_THIS_FILE]==Const.TUTORIAL):
            work = str(dic[Const.COURSE_ID]) + Const.TUTORIAl_LECTURE_WORK
            sheet = self.client.open("Courses").worksheet(work)
            insertRow=[dic[Const.FOLDERID], dic[Const.FILEID],dic[Const.YEAR],
                       dic[Const.SEMSTER],dic[Const.LECTURE_NAME],
                       dic[Const.WHAT_THIS_FILE],dic[Const.NUMOFLECTURE],
                       dic[Const.PARTOFLECTURE],Const.PATH_TO_FILE_DRIVE,dic[Const.REMARKS]]
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
            "what_this_file": "Tutorial",
            "WhatKind": "TutorialLecture"
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

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))



    def AddCourse(self,courseName:str,courseId:int):
        # save the curseTakeWeCreate as exal file and then we going to enter them file
        file_root_id = self._AddFolder(name=(str(courseName)+str(courseId)), fileId="root")

        # FolderId: int, courseId: int, courseName: str):
        self.mySheet.InsertCourse(FolderId=file_root_id, courseId=courseId, courseName=courseName)

        # add TestDiractory
        test_folder = self._AddFolder(name=Const.TEST, fileId=file_root_id)
        test_not_sol_folder = self._AddFolder(name=Const.TESTWITHOUTSOL, fileId=test_folder)
        test_with_sol_folder = self._AddFolder(name=Const.TESTWITHSOL, fileId=test_folder)


        # CREATE fOLDERS
        file__mid_tests_id = self._AddFolder(name=Const.MIDTEST, fileId=file_root_id)

        mid_test_not_sol_folder = self._AddFolder(name=Const.MIDTESTWITHOUTSOL, fileId=file__mid_tests_id)

        mid_test_with_sol_folder = self._AddFolder(name=Const.TESTWITHSOL, fileId=file__mid_tests_id)

        lecture_folder = self._AddFolder(name=Const.LECTURE, fileId=file_root_id)

        turital_folder_id = self._AddFolder(name=Const.TUTORIAL, fileId=file_root_id)

        HW_folder_id = self._AddFolder(name=Const.HWFOLDER, fileId=file_root_id)

        help_staff_folder_id = self._AddFolder(name=Const.HELPSTAFF, fileId=file_root_id)


        # Create Data Frame
        df_list = []

        dataFolder = {'GoogleDriveID': [test_folder,
                                        test_not_sol_folder,
                                        test_with_sol_folder,
                                        file__mid_tests_id,
                                        mid_test_not_sol_folder,
                                        mid_test_with_sol_folder,
                                        lecture_folder,
                                        turital_folder_id,
                                        help_staff_folder_id,
                                        HW_folder_id],
                      'folderName': [Const.TEST,
                                     Const.TESTWITHOUTSOL,
                                     Const.TESTWITHSOL,
                                     Const.MIDTEST,
                                     Const.MIDTESTWITHOUTSOL,
                                     Const.MIDTESTWWIHSOL,
                                     Const.LECTURE,
                                     Const.TUTORIAL,
                                     Const.HELPSTAFF,
                                     Const.HWFOLDER]}

        # Create DataFrame
        df = pd.DataFrame(dataFolder)

        df_list.append((df,Const.FOLDERID))

        data_lecture_totorial = {Const.FOLDERID: [],
                Const.FILEID: [],
                Const.YEAR: [],
                Const.SEMSTER: [],
                Const.LECTURE_NAME: [],
                Const.LECTURE_OR_TOTURIAL:[],
                Const.NUMOFLECTURE: [],
                Const.PARTOFLECTURE: [],
                Const.PATH_TO_FILE_DRIVE: [],
                Const.REMARKS: []
                }
        df_lecture_totorial = pd.DataFrame(data_lecture_totorial)

        df_list.append((df_lecture_totorial,Const.TUTORIAl_LECTURE_WORK))

        data_HW = {Const.FOLDERID: [],
                Const.FILEID: [],
                Const.YEAR: [],
                Const.SEMSTER: [],
                Const.LECTURE_NAME: [],
                Const.NUM_OF_HW: [],
                Const.PART_OF_HW: [],
                Const.PATH_TO_FILE_DRIVE: [],
                Const.SOL_OR_HW: [],
                Const.REMARKS: []
                }

        df_HW = pd.DataFrame(data_HW)

        df_list.append((df_HW,Const.HWFOLDER))
        # add חומרי עזר נוספ;


        data_help_staff = {Const.FOLDERID: [],
                Const.FILEID: [],
                Const.YEAR: [],
                Const.SEMSTER: [],
                Const.WORKSPACE: [],
                Const.REMARKS: []
                }

        df_help_staf = pd.DataFrame(data_help_staff)
        df_list.append((df_help_staf,Const.HELPSTAFF))

        create = lambda df,name: self.mySheet.addNewWorkSheet(data=df,name=str(courseId)+str(name))


        [create(item[0],item[1]) for item in df_list]


    def _UpdateExalToFolder(self,name:str,derctory:int):
        file_metadata = {
            'name': name,
            'parents': [derctory]
        }
        media = MediaFileUpload(name,
                                mimetype='application / vnd.google - apps.spreadsheet',
                                resumable=True)
        file = self.service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()


    def _AddSheet(self,name:str,fileId:str):
        file_metadata = {
            'name': name,
            'mimeType': 'application / vnd.google - apps.spreadsheet',
            'parents': [fileId]
        }
        file = self.service.files().create(body=file_metadata,
                                           fields='id').execute()
        return file.get('id')



    def _AddFolder(self,name:str,fileId:str):
        if(fileId!="root"):
            file_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents' :[fileId]
        }
        else:
            file_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder',
            }

        file = self.service.files().create(body=file_metadata,
                                               fields='id').execute()
        print('Folder ID: %s' % file.get('id'))
        return file.get('id')




    def _getFilePath(self,fileid:str):
        fileId = fileid
        tree = []  # Result
        file = self.service.files().get(fileId=fileId,fields='id,name, parents').execute()
        parent = file.get('parents')
        if parent:
            while True:
                folder = self.service.files().get(
                    fileId=parent[0], fields='id, name, parents').execute()
                parent = folder.get('parents')
                if parent is None:
                    break
                tree.append({'id': parent[0], 'name': folder.get('name')})

        print(tree)




    def AddFile(self,data:{}):


        folderId=self.mySheet.GetFolderID(dic=data,courseId=data["course_id"])


        name ="{} Number {} Part {} Semster {} Year {} LectureName {} Autor by {}"
        file_metadata={
            'name': name.format(data[Const.WHAT_THIS_FILE],data[Const.NUMOFLECTURE],
                                data[Const.PARTOFLECTURE],data[Const.SEMSTER]
                                ,data[Const.YEAR],data[Const.LECTURE_NAME],data[Const.REMARKS]),

            'mineType':'application/pdf',
            'parents': [folderId]
        }
        media = MediaFileUpload(data[Const.PATH_TO_FILE])

        file_id = self.service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()

        #self._getFilePath(file.get('id'))

        data[Const.FILEID]=file_id.get("id")
        data[Const.FOLDERID]=folderId

        self.mySheet.UpdateWorkSheet(data)


        # find the course




        print(data)


    def UpdateFile(self,fileName:str):
        file_metadata = {'name': 'photo.jpg','mimeType':'file'}
        file = self.service.files().create(body=file_metadata,
                                            fields='id').execute()
        'File ID: %s' % file.get('id')





if __name__ == '__main__':
    gda=GoogleDriveApi()
  #  gda.AddCourse(courseName="TEST",courseId="8220")
    # Create DataFrame
    dict = {
        Const.COURSE_ID:"8220",
        Const.YEAR: "2018",
        Const.SEMSTER: "A",
        Const.NUMOFLECTURE: "1",
        Const.PARTOFLECTURE: "1",
        Const.REMARKS: "OrrLaniado",
        Const.PATH_TO_FILE:"unit 2.pdf",
        Const.WHAT_THIS_FILE:"Tutorial",
        Const.TUTORIAl_LECTURE_WORK:"TutorialLecture",
        Const.LECTURE_NAME:"AVIV SENSOR",
        Const.PATH_TO_FILE_DRIVE:"YESS"
    }
    gda.AddFile(dict.copy())

   # gda.AddFolder("Orr")
   # gda.UpdateFile("yes")