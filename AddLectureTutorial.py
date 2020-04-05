import wx
from orr import GoogleDriveApi

GoogleDriveApi=None

class AddLectureTutorial:

    def __init__(self,googleDriveApi:GoogleDriveApi):
        global GoogleDriveApi
        GoogleDriveApi=googleDriveApi
        app = MyApp()
        app.MainLoop()



class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(parent=None, title="AddLectureTutorial")
        self.frame.Show()
        return True

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)
        self.panel = MyPanel(self)

        # course_id box
        course_id_box = wx.BoxSizer(wx.HORIZONTAL)
        course_id = wx.StaticText(self, label="CourseID:")
        course_id_box.Add(course_id, 0, wx.ALL | wx.CENTER, 5)
        self.course_id = wx.TextCtrl(self)
        course_id_box.Add(self.course_id, 0, wx.ALL, 5)


        # course_year box
        course_year_box = wx.BoxSizer(wx.HORIZONTAL)
        course_year = wx.StaticText(self, label="CourseYear:")
        course_year_box.Add(course_year, 0, wx.ALL | wx.CENTER, 5)
        self.course_year = wx.TextCtrl(self)
        course_year_box.Add(self.course_year, 0, wx.ALL, 5)


        # what num of lecture/tutorial box
        course_num_box = wx.BoxSizer(wx.HORIZONTAL)
        course_num = wx.StaticText(self, label="lecture/tutorial num")
        course_num_box.Add(course_num, 0, wx.ALL | wx.CENTER, 5)
        self.course_num = wx.TextCtrl(self)
        course_num_box.Add(self.course_num, 0, wx.ALL, 5)


        # what part of lectue/tutorial box

        what_kind_of_part_List = ['1', '2', '3']

        self.kind_part = wx.RadioBox(self, label='whatKindOfPart', choices=what_kind_of_part_List,
                                        majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.kind_part.Bind(wx.EVT_RADIOBOX, self.OnRadioBox)



        # course semster box

        what_kind_of_semster_List = ['A', 'B','C']

        self.kind_semster = wx.RadioBox(self, label='whatKindOfSemster', choices=what_kind_of_semster_List,
                                     majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.kind_semster.Bind(wx.EVT_RADIOBOX, self.OnRadioBox)






        # course remarks box

        course_remarks_box = wx.BoxSizer(wx.HORIZONTAL)
        course_remarks = wx.StaticText(self, label="Remarks:")
        course_remarks_box.Add(course_remarks, 0, wx.ALL | wx.CENTER, 5)
        self.remarks = wx.TextCtrl(self)
        course_remarks_box.Add(self.remarks, 0, wx.ALL, 5)

        # add kind of file ChekeBox
        what_kind_of_file_List = ['Tutorial','Lecture']

        self.kind_file = wx.RadioBox(self, label='whatKindOfFile', choices=what_kind_of_file_List,
                                     majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.kind_file.Bind(wx.EVT_RADIOBOX, self.OnRadioBox)










        # if this






       # course_year_box = wx.BoxSizer(wx.HORIZONTAL)
       # course_name = wx.StaticText(self, label="WhatKindOfFile:")
       # course_year_box.Add(course_name, 0, wx.ALL | wx.CENTER, 5)
       # self.name = wx.TextCtrl(self)
       # course_year_box.Add(self.name, 0, wx.ALL, 5)

        # connect
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(course_id_box, 0, wx.ALL, 5)
        main_sizer.Add(course_year_box, 0, wx.ALL, 5)
        main_sizer.Add(course_num_box,0,wx.ALL,5)
        main_sizer.Add(self.kind_part, 0, wx.ALL, 5)
        main_sizer.Add(self.kind_semster,0,wx.ALL,5)
        main_sizer.Add(self.kind_file, 0, wx.ALL, 5)
        main_sizer.Add( course_remarks_box,0,wx.ALL,5)




        # add File



        btn = wx.Button(self, label="AddFile")
        btn.Bind(wx.EVT_BUTTON, self.OnAddFile)
        main_sizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)

        # update to google drive

        btn = wx.Button(self, label="Update")
        btn.Bind(wx.EVT_BUTTON, self.OnUpdate)
        main_sizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)


        self.SetSizer(main_sizer)


    def OnUpdate(self,event):

        dict={
                "course_id": self.course_id.GetValue(),
                "year": self.course_year.GetValue(),
                "semster":self.kind_semster.GetSelection(),
                "numOfLecture":self.course_num.GetValue(),
                "partOfLecture":self.kind_part.GetSelection(),
                "remark":self.remarks.GetValue(),
                "path_to_file":str(self.pathname),
                "kind_file":self.kind_file.GetSelection()
        }
        GoogleDriveApi.AddFile(data=dict.copy())





    def OnRadioBox(self,event):
        pass

    def OnAddFile(self,event):

        with wx.FileDialog(self, "Open XYZ file",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return  # the user changed their mind

            # Proceed loading the file chosen by the user
                self.pathname = fileDialog.GetPath()

                #try:
                #    with open(pathname, 'r') as file:
                #        self.doLoadDataOrWhatever(file)
                #except IOError:
                #    wx.LogError("Cannot open file '%s'." % newfile)

      #  global GoogleDriveApi
      #  GoogleDriveApi.AddCourse(self.name.GetValue(),self.course_id.GetValue())
       # self.Close(True)
        print(self.pathname)

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)
