from __future__ import print_function
import pickle
import os.path
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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




     #   insertRow = [FolderId, courseId, courseName]
     #   sheet.insert_row(insertRow,1)



       # d2g.upload(data,"1B8ROxKr8utzDLM-4mLgapvynDzoiPe4oN8byzgTNx4A",name)

        #existing = gd.get_as_dataframe(sheet)
        #updated = existing.append(data)
        #gd.set_with_dataframe(sheet, updated)

        #sheet.insert_row(["hello"],index=1)
        #sheet.insert_row(["BY"],index=2)

        #sheet.insert_row(["BYE"])
       # sheet.add_rows("hello")
        #[sheet.delete_row(i) for i in range(5,)]


    def InsertCourse(self,FolderId:int,courseId:int,courseName:str):

        sheet = self.client.open("Courses").sheet1
        insertRow=[FolderId,courseId,courseName]
        sheet.insert_row(insertRow,2)
        data = sheet.get_all_records()
        df=pd.DataFrame(data)
     #   df.insert(2, "Age", [21, 23, 24, 21], True)
     #   print(df)
        # pprint(data)

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



    def AddNewCourse(self,courseName:str,courseId:int):
        # save the curseTakeWeCreate as exal file and then we going to enter them file
        file_root_id = self._AddFolder(name=courseName, fileId="root")

        # FolderId: int, courseId: int, courseName: str):
        self.mySheet.InsertCourse(FolderId=file_root_id, courseId=courseId, courseName=courseName)

        # add TestDiractory
        file_tests_id = self._AddFolder(name="Test", fileId=file_root_id)
        test_not_sol_folder = self._AddFolder(name="TestWithOutSo", fileId=file_tests_id)
        test_with_sol_folder = self._AddFolder(name="TestWithSol", fileId=file_tests_id)

        # add TestFolder

        # intialise data of lists.
        data = {'GoogleDriveID': [test_not_sol_folder, test_with_sol_folder],
                'folderName': ["TestWithOutSol", "TestWithSol"]}

        # Create DataFrame
        df = pd.DataFrame(data)
   #     df.to_excel("TestsFolder.xlsx")
        # add Test To Folder
   #     self._UpdateExalToFolder(name="TestsFolder.xlsx", derctory=file_tests_id)




        # add minTest Diractory

        file__mid_tests_id = self._AddFolder(name="MidTest", fileId=file_root_id)
        mid_test_not_sol_folder = self._AddFolder(name="MidTestWithOutSol", fileId=file__mid_tests_id)
        mid_test_with_sol_folder = self._AddFolder(name="MidTestWithSol", fileId=file__mid_tests_id)

        # add TestFolder

        # intialise data of lists.
        data = {'GoogleDriveID': [mid_test_not_sol_folder, mid_test_with_sol_folder],
                'folderName': ["MidTestWithOutSol", "MidTestWithSol"]}

        # Create DataFrame
        df = pd.DataFrame(data)

        df.to_excel("MidTestsFolder.xlsx")
        # add Test To Folder
        self._UpdateExalToFolder(name="MidTestsFolder.xlsx", derctory=file__mid_tests_id)

        #  add LectureDiractory

        lecture_folder_id = self._AddFolder(name="Lecture", fileId=file_root_id)

        data = {'GoogleDriveFolderID': [],
                'fileIdGoogleDriveFileId': [],
                'year': [],
                'semster': [],
                'lectureName': [],
                'numOfLecture': [],
                'partOfLecture': [],
                'pathToFile': [],
                'remarks': []
                }
        df = pd.DataFrame(data)
        df.to_excel("Lecture.xlsx")

        self._UpdateExalToFolder(name="Lecture.xlsx", derctory=lecture_folder_id)

        # turital

        turital_folder_id = self._AddFolder(name="Tutorial", fileId=file_root_id)
        df.to_excel("Tutorial.xlsx")
        self._UpdateExalToFolder(name="Tutorial.xlsx", derctory=turital_folder_id)

        # add  HW Folder
        HW_folder_id = self._AddFolder(name="HWFolder", fileId=file_root_id)
        data = {'GoogleDriveFolderID': [],
                'fileIdGoogleDriveFileId': [],
                'year': [],
                'semster': [],
                'lectureName': [],
                'numOfHW': [],
                'partOfHW': [],
                'pathToFile': [],
                'ThisIsSol': [],
                'remarks': []
                }

        df = pd.DataFrame(data)
        df.to_excel("HW.xlsx")
        self._UpdateExalToFolder(name="HW.xlsx", derctory=HW_folder_id)

        # add חומרי עזר נוספים;

        help_staff_folder_id = self._AddFolder(name="HelpStaff", fileId=file_root_id)

        data = {'GoogleDriveFolderID': [],
                'GoogleDriveFileId': [],
                'year': [],
                'semster': [],
                'whatKind': [],
                'remarks': []
                }

        df = pd.DataFrame(data)
        df.to_excel("HelpStaff.xlsx")
        self._UpdateExalToFolder(name="HelpStaff.xlsx", derctory=help_staff_folder_id)

        data = {'GoogleDriveID': [file_tests_id, file__mid_tests_id, HW_folder_id, lecture_folder_id, turital_folder_id,
                                  help_staff_folder_id],
                'folderName': ["TestFolder", "MidTests", "HWFolder", "LectureFolder", "TuritalFolder",
                               "HelpStaffFolder"]}

        df = pd.DataFrame(data)
        df.to_excel("TreeFolder.xlsx")
        self._UpdateExalToFolder(name="TreeFolder.xlsx", derctory=file_root_id)


    def AddCourse(self,courseName:str ,courseId:int):
        # save the curseTakeWeCreate as exal file and then we going to enter them file
        file_root_id=self._AddFolder(name=courseName,fileId="root")

        # FolderId: int, courseId: int, courseName: str):
        self.mySheet.InsertCourse(FolderId=file_root_id,courseId=courseId,courseName=courseName)

        # add TestDiractory
        file_tests_id=self._AddFolder(name="Test",fileId=file_root_id)
        test_not_sol_folder=self._AddFolder(name="TestWithOutSo",fileId=file_tests_id)
        test_with_sol_folder=self._AddFolder(name="TestWithSol",fileId=file_tests_id)

        # add TestFolder

        # intialise data of lists.
        data = {'GoogleDriveID': [test_not_sol_folder,test_with_sol_folder], 'folderName': ["TestWithOutSol","TestWithSol"]}

        # Create DataFrame
        df = pd.DataFrame(data)

        df.to_excel("TestsFolder.xlsx")
        # add Test To Folder
        self._UpdateExalToFolder(name="TestsFolder.xlsx",derctory=file_tests_id)


        # add minTest Diractory

        file__mid_tests_id = self._AddFolder(name="MidTest", fileId=file_root_id)
        mid_test_not_sol_folder = self._AddFolder(name="MidTestWithOutSol", fileId=file__mid_tests_id)
        mid_test_with_sol_folder = self._AddFolder(name="MidTestWithSol", fileId=file__mid_tests_id)

        # add TestFolder

        # intialise data of lists.
        data = {'GoogleDriveID': [mid_test_not_sol_folder, mid_test_with_sol_folder],
                'folderName': ["MidTestWithOutSol", "MidTestWithSol"]}

        # Create DataFrame
        df = pd.DataFrame(data)

        df.to_excel("MidTestsFolder.xlsx")
        # add Test To Folder
        self._UpdateExalToFolder(name="MidTestsFolder.xlsx", derctory=file__mid_tests_id)

        #  add LectureDiractory

        lecture_folder_id=self._AddFolder(name="Lecture",fileId=file_root_id)

        data = {'GoogleDriveFolderID': [],
                'fileIdGoogleDriveFileId': [],
                'year':[],
                'semster':[],
                'lectureName':[],
                'numOfLecture':[],
                'partOfLecture':[],
                'pathToFile':[],
                'remarks':[]
                }
        df = pd.DataFrame(data)
        df.to_excel("Lecture.xlsx")


        self._UpdateExalToFolder(name="Lecture.xlsx", derctory=lecture_folder_id)

        # turital

        turital_folder_id=self._AddFolder(name="Tutorial",fileId=file_root_id)
        df.to_excel("Tutorial.xlsx")
        self._UpdateExalToFolder(name="Tutorial.xlsx", derctory=turital_folder_id)


        # add  HW Folder
        HW_folder_id = self._AddFolder(name="HWFolder", fileId=file_root_id)
        data = {'GoogleDriveFolderID': [],
                'fileIdGoogleDriveFileId': [],
                'year': [],
                'semster': [],
                'lectureName': [],
                'numOfHW': [],
                'partOfHW': [],
                'pathToFile': [],
                'ThisIsSol':[],
                'remarks': []
                }

        df = pd.DataFrame(data)
        df.to_excel("HW.xlsx")
        self._UpdateExalToFolder(name="HW.xlsx", derctory=HW_folder_id)




        #add חומרי עזר נוספים;

        help_staff_folder_id=self._AddFolder(name="HelpStaff",fileId=file_root_id)

        data = {'GoogleDriveFolderID': [],
            'GoogleDriveFileId': [],
            'year': [],
            'semster': [],
            'whatKind': [],
            'remarks': []
            }

        df = pd.DataFrame(data)
        df.to_excel("HelpStaff.xlsx")
        self._UpdateExalToFolder(name="HelpStaff.xlsx", derctory=help_staff_folder_id)


        data = {'GoogleDriveID': [file_tests_id,file__mid_tests_id,HW_folder_id, lecture_folder_id,turital_folder_id,help_staff_folder_id],
                'folderName': ["TestFolder","MidTests","HWFolder", "LectureFolder","TuritalFolder","HelpStaffFolder"]}

        df = pd.DataFrame(data)
        df.to_excel("TreeFolder.xlsx")
        self._UpdateExalToFolder(name="TreeFolder.xlsx", derctory=file_root_id)

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



    def AddFile(self,data:dict):

        self.mySheet.FindDiractoryID(FolderId=file_root_id, courseId=courseId, courseName=courseName)
        sheet = self.client.open("Courses").sheet1

        # find the course




        print(data)


    def UpdateFile(self,fileName:str):
        file_metadata = {'name': 'photo.jpg','mimeType':'file'}
        file = self.service.files().create(body=file_metadata,
                                            fields='id').execute()
        'File ID: %s' % file.get('id')


if __name__ == '__main__':
    #gda=GoogleDriveApi()
    #gda.AddCourse(courseName="לוגיקה למדעי המחשב" ,courseId=11111)
    sh=Sheet()
    sh.FindRootDiractoryID("104032")

    data = {'GoogleDriveFolderID': [1,2,3],
            'GoogleDriveFileId': [4,5,6],
            'year': [7,8,9],
            'semster': [10,11,12],
            'whatKind': [13,14,15],
            'remarks': [16,17,18]
            }

    df = pd.DataFrame(data)
    sh.addNewWorkSheet(data=df,name="yes")


   # gda.AddFolder("Orr")
   # gda.UpdateFile("yes")