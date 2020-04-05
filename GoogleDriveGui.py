import wx

from orr import GoogleDriveApi
from AddCourseGuI import AddCourseGuI
from AddFileGui import AddFileGui
from AddLectureTutorial import AddLectureTutorial

from os import listdir
from os.path import isfile, join
class MyFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="",
                 pos=wx.DefaultPosition, size=(800, 1000),
                 style=wx.DEFAULT_FRAME_STYLE
                 , name="MyFrame"):
        super(MyFrame, self).__init__(parent, id, title, pos, size, style, name)
        self.panel = wx.Panel(self)

        self.googleDriveApi=GoogleDriveApi()



        # Setting  menu
        file_menu = wx.Menu()

        # first file menu
        menu_about = file_menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        file_menu.AppendSeparator()

        menu_witch_courses = file_menu.Append(wx.ID_ANY, "Know what courses we have in big drive")
        file_menu.AppendSeparator()

        menu_exit = file_menu.Append(wx.ID_EXIT, "&Exit", " Terminate the program")

        # Creating the menubar
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")  # Adding the "file_menu" to the MenuBar
        self.SetMenuBar(menu_bar)  # Adding the MenuBar to the Frame content.

        # add Events to the tool bar
    #    self.Bind(wx.EVT_MENU, self.OnAbout, menu_about)
    #    self.Bind(wx.EVT_MENU, self.OnExit, menu_exit)
    #    self.Bind(wx.EVT_MENU, self.onMenuWitchCourses, menu_witch_courses)

        # add buttens to the application
        self.btn1 = wx.Button(self.panel, label="Push Me to Log in")
        self.btn2 = wx.Button(self.panel, label="I wanna add new Curse")
        self.btn3 = wx.Button(self.panel, label="I wanna add new Files")


        self.btn4 = wx.Button(self.panel, label="I wanna Add Exam/midExam")
        self.btn5 = wx.Button(self.panel, label="I wanna Add Turtial/Lecture")
        self.btn6 = wx.Button(self.panel, label="I wanna Add HW")
        self.btn7 = wx.Button(self.panel, label="I wanna Add HelpStaff")


        self.btn8 = wx.Button(self.panel,label="I wanna to do nice qulity")





        # show all course
        self.course_namese = wx.StaticText(self.panel, -1, label="")
        self.course_namese.SetForegroundColour(wx.RED)

        # self.btn2 = wx.Button(self.panel, label="")

        # add sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.btn1, 0, wx.ALL, 10)
        sizer.Add(self.btn2, 0, wx.ALL, 10)
        sizer.Add(self.btn3, 0, wx.ALL, 10)
        sizer.Add(self.btn4, 0, wx.ALL, 10)
        sizer.Add(self.btn5,0,wx.ALL,10)
        sizer.Add(self.btn6,0,wx.ALL,10)
        sizer.Add(self.btn7,0,wx.ALL,10)
        sizer.Add(self.btn8, 0, wx.ALL, 10)




        sizer.SetSizeHints(self.panel)

        self.panel.SetSizer(sizer)
        # Connect the buttuns to the libary

        self.Bind(wx.EVT_BUTTON, self.OnInit, self.btn1)
        self.Bind(wx.EVT_BUTTON, self.OnAddNewCourse, self.btn2)
        self.Bind(wx.EVT_BUTTON, self.OnAddNewFile, self.btn3)
        self.Bind(wx.EVT_BUTTON, self.OnAddNewExamMidExam, self.btn4)
        self.Bind(wx.EVT_BUTTON, self.OnAddNewLectureTutorial, self.btn5)
        self.panel.Layout()

    def OnInit(self,event):
        pass


    def OnAddNewLectureTutorial(self,event):
        print("tttt")
        self.add_lecutre_tutorial = AddLectureTutorial(self.googleDriveApi)

    def OnAddNewExamMidExam(self,event):
        pass

    def OnAddNewCourse(self, event):
        print("yes!!")
        self.addCourseGuI=AddCourseGuI(self.googleDriveApi)

        print("Yes")


    def OnAddNewFile(self,event):
        print("no")
        self.addFileGui=AddFileGui(self.googleDriveApi)

    def OnDoQulity(self,event):
        pass







class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Technio")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()








