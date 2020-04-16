import wx

import Const
from PyPDF2 import PdfFileReader,PdfFileWriter ,PdfFileMerger

import os.path
class MergeSplitGUI:

    def __init__(self):

        app = MyApp()
        app.MainLoop()



class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(parent=None, title="MergeSplitGUI")
        self.frame.Show()
        return True

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title,size=(600,800))
        self.panel = MyPanel(self)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        # choose file to split
        course_remarks_box = wx.BoxSizer(wx.HORIZONTAL)
        course_remarks = wx.StaticText(self, label="ChooseFile to split:")
        course_remarks_box.Add(course_remarks, 0, wx.ALL | wx.CENTER, 5)
        self.btn1 = wx.Button(self, label="ChooseFileToSplit")
        course_remarks_box.Add(self.btn1, 0, wx.ALL, 5)

        self.static_text_choose_file = wx.StaticText(self, label="NotFile was choosen!")
        course_remarks_box.Add(self.static_text_choose_file, 0, wx.ALL | wx.Center, 5)


        self.main_sizer.Add(course_remarks_box)





        # choose location where to save

        course_remarks_box = wx.BoxSizer(wx.HORIZONTAL)
        course_remarks = wx.StaticText(self, label="Choose location to save:")
        course_remarks_box.Add(course_remarks, 0, wx.ALL | wx.CENTER, 5)
        self.btn2 = wx.Button(self, label="Choose location to save")
        course_remarks_box.Add(self.btn2, 0, wx.ALL, 5)
        self.static_text_choose_folder = wx.StaticText(self, label="NotFolder was choosen!")
        course_remarks_box.Add(self.static_text_choose_folder, 0, wx.ALL | wx.Center, 5)
        self.main_sizer.Add(course_remarks_box)




       # self.static_text_choose_splits = wx.StaticText(self, label="NotFolder was choosen!")
       # course_remarks_box.Add(self.static_text_choose_folder, 0, wx.ALL | wx.Center, 5)
       # self.main_sizer.Add(course_remarks_box)
       # self.btn2 = wx.Button(self, label="Choose location to save")
       # course_remarks_box.Add(self.btn2, 0, wx.ALL, 5)



        # choose num of split you wanna have to

        num_of_split_box = wx.BoxSizer(wx.HORIZONTAL)
        course_remarks = wx.StaticText(self, label="Choose Num of splits")
        num_of_split_box.Add(course_remarks, 0, wx.ALL | wx.CENTER, 5)
        self.num_of_split = wx.TextCtrl(self)
        num_of_split_box.Add(self.num_of_split, 0, wx.ALL, 5)
        self.btn3 = wx.Button(self, label="Choose Num of splits")
        num_of_split_box.Add(self.btn3, 0, wx.ALL, 5)
        self.main_sizer.Add(num_of_split_box)




        # on spliting!!

        course_remarks_box = wx.BoxSizer(wx.HORIZONTAL)
        course_remarks = wx.StaticText(self, label="I wanna split")
        course_remarks_box.Add(course_remarks, 0, wx.ALL | wx.CENTER, 5)
        self.btn4 = wx.Button(self, label="split now!!")
        course_remarks_box.Add(self.btn4, 0, wx.ALL, 5)
      #  course_remarks_box.Add("Split now", 0, wx.ALL | wx.Center, 5)

        self.main_sizer.Add(course_remarks_box)



       # self.main_sizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)

        self.btn1.Bind(wx.EVT_BUTTON, self.OnAddFile)
        self.btn2.Bind(wx.EVT_BUTTON, self.OnSaveFile)
        self.btn3.Bind(wx.EVT_BUTTON,self.OnNumSplit)
        self.btn4.Bind(wx.EVT_BUTTON,self.OnSplit)
        self.text_from=[]
        self.text_to=[]
        self.SetSizerAndFit(self.main_sizer)




    def OnSplit(self,event):
        print(self.pathname_file)
        pdf_document =self.pathname_file
        pdf = PdfFileReader(pdf_document)


        getIndex = lambda index : (int(self.text_from[index].GetValue()) ,int(self.text_to[index].GetValue()))


        # self.text_from
        # self.text_to
        # num of elemnts self.text_to
        num_of_elemnts = len(self.text_to)

        for i in range(num_of_elemnts):
            (from_page,to_page)=getIndex(i)
            pdf_writer = PdfFileWriter()
            for page in range(from_page,to_page+1):
                current_page = pdf.getPage(int(page))
                pdf_writer.addPage(page=current_page)

            output_file_name = "split_num_{}.pdf".format(i + 1)
            save_path = self.pathname_folder
            compate_name=os.path.join(save_path,output_file_name)
            with open(compate_name, "wb") as out:
                pdf_writer.write(out)
                print("created", output_file_name)


    def _OnNumSplit(self, num):
        split_box = wx.BoxSizer(wx.HORIZONTAL)
        arrayOfElmnts = []

        file_label = wx.StaticText(self, label="subfile" + str(num+1))
        file_lable_from = wx.StaticText(self, label="From")
        self.text_from.append(wx.TextCtrl(self))
        file_lable_To = wx.StaticText(self, label="To")
        self.text_to.append(wx.TextCtrl(self))

        # appending
        arrayOfElmnts.append(file_label)
        arrayOfElmnts.append(file_lable_from)
        arrayOfElmnts.append(self.text_from[num])
        arrayOfElmnts.append(file_lable_To)
        arrayOfElmnts.append(self.text_to[num])
        [split_box.Add(item, 0, wx.ALL | wx.Center, 5) for item in arrayOfElmnts]
        self.main_sizer.Add(split_box)



    def OnNumSplit(self,event):




        num_of_value = int(self.num_of_split.GetValue())
        for i in range(num_of_value):
            self._OnNumSplit(i)

        self.SetSizerAndFit(self.main_sizer)




    def OnSaveFile(self,event):
        with wx.DirDialog(None) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            self.pathname_folder = fileDialog.GetPath()

            # try:
            #    with open(pathname, 'r') as file:
            #        self.doLoadDataOrWhatever(file)
            # except IOError:
            #    wx.LogError("Cannot open file '%s'." % newfile)

            #  global GoogleDriveApi
            #  GoogleDriveApi.AddCourse(self.name.GetValue(),self.course_id.GetValue())
            # self.Close(True)
        print(self.pathname_folder)
        self.static_text_choose_folder.SetLabelText(self.pathname_folder)






    def OnRadioBox(self,event):
        pass

    def OnAddFile(self,event):

        with wx.FileDialog(self, "Open XYZ file",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return  # the user changed their mind

            # Proceed loading the file chosen by the user
                self.pathname_file = fileDialog.GetPath()

                #try:
                #    with open(pathname, 'r') as file:
                #        self.doLoadDataOrWhatever(file)
                #except IOError:
                #    wx.LogError("Cannot open file '%s'." % newfile)

      #  global GoogleDriveApi
      #  GoogleDriveApi.AddCourse(self.name.GetValue(),self.course_id.GetValue())
       # self.Close(True)
        print(self.pathname_file)
        self.static_text_choose_file.SetLabelText(self.pathname_file)

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)
