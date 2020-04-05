import wx
import orr
from orr import GoogleDriveApi

GoogleDriveApi=None

class AddCourseGuI:

    def __init__(self,googleDriveApi:GoogleDriveApi):
        global GoogleDriveApi
        GoogleDriveApi=googleDriveApi
        app = MyApp()
        app.MainLoop()



class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(parent=None, title="AddCousre")
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


        # course_name box
        course_name_box = wx.BoxSizer(wx.HORIZONTAL)

        course_name = wx.StaticText(self, label="CourseName:")
        course_name_box.Add(course_name, 0, wx.ALL | wx.CENTER, 5)
        self.name = wx.TextCtrl(self)
        course_name_box.Add(self.name, 0, wx.ALL, 5)


        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(course_id_box, 0, wx.ALL, 5)
        main_sizer.Add(course_name_box, 0, wx.ALL, 5)

        btn = wx.Button(self, label="AddCourse")
        btn.Bind(wx.EVT_BUTTON, self.OnAddCourse)
        main_sizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(main_sizer)


    def OnAddCourse(self,event):
        global GoogleDriveApi
        GoogleDriveApi.AddCourse(self.name.GetValue(),self.course_id.GetValue())
        self.Close(True)

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)





