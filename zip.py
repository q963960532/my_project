import Tkinter as tk
import ttk
import zipfile
import tkFileDialog
import os
import subprocess

px_unit = 0.1427
px_unit_height = 0.070
pt_unit = int(1 / px_unit)
# Measured by actual size
win_px_width = 810
win_px_height = 610


def getActualWidth(px_value):
    return int(px_value * px_unit)

class ZIPFrame(tk.Tk,object):
    def __init__(self):
        super(ZIPFrame, self).__init__()
        self.title('ZIPFrame')
        self.geometry('400x180')
        self.wm_attributes('-topmost',1)
        self.protocol('WM_DELETE_WINDOW',self.close)
        self.propagate(False)
        self.topView=tk.Frame(self,width=getActualWidth(win_px_width),height=50)
        self.topView.propagate(False)
        self.topView.pack(fill=tk.BOTH)
        self.setCenterWindow()
        self.addTopView()

    def setCenterWindow(self):
        self.withdraw()  # hide window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()  # under windows, taskbar may lie under the screen
        self.resizable(False, False)
        # add some widgets to the root window...
        self.update_idletasks()
        self.deiconify()  # now window size was calculated
        self.withdraw()  # hide window again
        # root.geometry('%sx%s+%s+%s'%(root.winfo_width()+10,root.winfo_height()+10,(screen_width-root.winfo_width())/2,(screen_height-root.winfo_height())/2))#center window on desktop
        self.geometry('%sx%s+%s+%s' % (
            self.winfo_width() + 10, self.winfo_height() + 10, (screen_width - self.winfo_width()) / 2,
            (screen_height) * 1 / 6))  # center window on desktop
        self.deiconify()


    def close(self):
        self.destroy()

    def addTopView(self):
        self.f=tk.StringVar()
        self.f.set('please input the path')
        self.g=tk.StringVar()
        self.g.set('please input the path')
        self.input=tk.Entry(self.topView,textvariable=self.f,width=30)
        self.input.grid(row=1,column=1,padx=pt_unit,pady=pt_unit,sticky=tk.W)
        tk.Button(self.topView,text='extract',command=self.openFile,width=10).grid(row=1,column=2,sticky=tk.W)
        self.input2=tk.Entry(self.topView,textvariable=self.g,width=30)
        self.input2.grid(row=2,column=1,padx=pt_unit,pady=pt_unit,sticky=tk.W)
        # tk.Button(self.topView,text='start',command=self.start,width=10).grid(row=2,column=2,sticky=tk.W)

        self.h=tk.StringVar()
        self.h.set('')
        self.input3=tk.Entry(self.topView,textvariable=self.h,width=20)
        self.input3.grid(row=4, column=1, padx=pt_unit, pady=pt_unit, sticky=tk.W)
        tk.Button(self.topView, text='compress', command=self.compress, width=10).grid(row=2, column=2, sticky=tk.W)
        # tk.Button(self.topView, text='Encrypted', command=self.compress1, width=10).grid(row=4, column=2, sticky=tk.W)
        # tk.Button(self.topView, text='UnEncrypted', command=self.compress2, width=10).grid(row=5, column=2, sticky=tk.W)
        tk.Label(self.topView,text='input the password first:',width=20).grid(row=3,column=1,padx=pt_unit,pady=pt_unit,sticky=tk.W)
        # tk.Label(self.topView, text='no password: ', width=10).grid(row=5, column=1, padx=pt_unit, pady=pt_unit, sticky=tk.W)


    def openFile(self):
        default_dir=r''
        fname=tkFileDialog.askopenfilename(title=u'choose file',
                                           initialdir=(os.path.expanduser(default_dir)))
        self.f.set(fname)
        self.a=os.path.split(fname)
        file=os.path.splitext(self.a[1])
        filename,type=file
        if type=='.zip':
            print self.a,fname
            self.g.set(self.a[0])
            # os.system('unzip -dP '+self.a[0]+' '+fname+''+self.input3.get())



        else:
            self.g.set(self.a[0]+'/11.zip')

        self.start()
        # self.input.delete('0.0','end')
        # self.input.insert('0.0',fname)

        # azip=zipfile.ZipFile(str(self.input.get()))
        # azip.extractall('/home/syrup/Desktop',pwd='123')

    def start(self):
        file=os.path.splitext(self.a[1])
        filename,type=file
        if type=='.zip':
            azip=zipfile.ZipFile(str(self.input.get()))
            azip.extractall(self.input2.get(),pwd=self.input3.get())
            azip.close()
        else:
            azip=zipfile.ZipFile(str(self.input2.get()),'w')
            azip.write(self.a[1])
            azip.setpassword(pwd=self.input3.get())
            # else:
            #     azip.write(self.input.get(),compress_type=zipfile.ZIP64_LIMIT)
            azip.close()


    def compress(self):
        dirname=tkFileDialog.askdirectory(title=u'choose directory')
        self.f.set(dirname)
        self.a = os.path.split(dirname)
        self.g.set(self.a[0]+'/'+self.a[1]+'.zip')
        self.c=os.path.split(self.input2.get())
        print self.a[1]
        if self.input3.get()=='':
            os.system('cd ' + self.a[0] + ' && zip -r ' + self.a[1] + '.zip' + ' ' + self.a[1])
        else:
            os.system('cd ' + self.a[0] + ' && zip -rP ' + self.input3.get() + ' ' + self.a[1] + '.zip' + ' ' + self.a[1])



        # z=zipfile.ZipFile(str(self.input2.get()),'w')
        # if os.path.isdir(self.a[1]):
        #     for d in os.listdir(self.a[1]):
        #         z.write(self.a[1]+os.sep+d)
        # z.close()

    # def compress1(self):

        # os.system('cd '+self.a[0]+' && zip -rP '+self.input3.get()+' '+self.a[1]+'.zip'+' '+self.a[1])

        # self.zip_path(self.input.get(), self.c[0], self.c[1])

    def compress2(self):
        os.system('cd ' + self.a[0] + ' && zip -r '+ self.a[1] + '.zip' + ' ' + self.a[1])
        # self.zip_path(self.input.get(), self.c[0], self.c[1])

    def dfs_get_zip_file(self,input_path, result):

        #
        files = os.listdir(input_path)
        for file in files:
            if os.path.isdir(input_path + '/' + file):
                self.dfs_get_zip_file(input_path + '/' + file, result)
            else:
                result.append(input_path + '/' + file)

    def zip_path(self,input_path, output_path, output_name):

        f = zipfile.ZipFile(output_path + '/' + output_name, 'w', zipfile.ZIP_DEFLATED)
        f.pwd='123'

        filelists = []
        self.dfs_get_zip_file(input_path, filelists)
        for file in filelists:
            f.write(file)

        f.close()
        return output_path + r"/" + output_name

def main():
    app=ZIPFrame()
    app.mainloop()
if __name__=='__main__':
    main()