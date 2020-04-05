import wx
from orr import GoogleDriveApi

GoogleDriveApi=None

class AddFileGui:

    def __init__(self,googleDriveApi:GoogleDriveApi):
        global GoogleDriveApi
        GoogleDriveApi=googleDriveApi
        app = MyApp()
        app.MainLoop()



class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(parent=None, title="AddFile")
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
        self.name = wx.TextCtrl(self)
        course_year_box.Add(self.name, 0, wx.ALL, 5)


        # course semster box

        what_kind_of_semster_List = ['A', 'B','C']

        self.kind_semster = wx.RadioBox(self, label='whatKindOfSemster', choices=what_kind_of_semster_List,
                                     majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.kind_semster.Bind(wx.EVT_RADIOBOX, self.OnRadioBox)


        # add kind of file ChekeBox
        what_kind_of_file_List = ['Test', 'minTest', 'Tutorial','Lecture','HW','HelpStaff']

        self.kind_file = wx.RadioBox(self, label='whatKindOfFile', choices=what_kind_of_file_List,
                                     majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.kind_file.Bind(wx.EVT_RADIOBOX, self.OnRadioBox)



        #if this test/ mid - this is sol or not

        what_kind_of_exam_list = ['Questionnaire', 'Sol']

        self.kind_exam = wx.RadioBox(self, label='ifThisExam', choices=what_kind_of_exam_list,
                                     majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.kind_exam.Bind(wx.EVT_RADIOBOX, self.OnRadioBox)


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
        main_sizer.Add(self.kind_semster,0,wx.ALL,5)
        main_sizer.Add(self.kind_file, 0, wx.ALL, 5)
        main_sizer.Add(self.kind_exam, 0, wx.ALL, 5)

        btn = wx.Button(self, label="AddFile")
        btn.Bind(wx.EVT_BUTTON, self.OnAddCourse)
        main_sizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(main_sizer)


    def OnRadioBox(self,enent):
        pass
    def OnAddCourse(self,event):
        global GoogleDriveApi
        GoogleDriveApi.AddCourse(self.name.GetValue(),self.course_id.GetValue())
        self.Close(True)

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)
