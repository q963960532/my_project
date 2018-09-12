import Tkinter as tk
import ttk
from serial import *
from time import sleep
import thread

px_unit = 0.1427
px_unit_height = 0.070
pt_unit = int(1 / px_unit)
# Measured by actual size
win_px_width = 810
win_px_height = 610


def getActualWidth(px_value):
    return int(px_value * px_unit)

def getActualHeight(px_value):
    return int(px_value * px_unit_height)


class SerialPortFrame(tk.Tk, object):
    def __init__(self):
        super(SerialPortFrame, self).__init__()
        self.title('SerialPortTool')
        self.geometry('800x600')
        self.wm_attributes('-topmost', 1)
        self.protocol('WM_DELETE_WOW', self.close)
        self.propagate(False)

        self.topView = tk.Frame(self, width=getActualWidth(win_px_width), height=50)#, bg='yellow')
        self.topView.propagate(False)
        self.topView.pack(fill=tk.BOTH)
        self.centerView = tk.Frame(self, width=getActualWidth(win_px_width), height=getActualHeight(350))#, bg='green')
        self.centerView.propagate(False)
        self.centerView.pack(fill=tk.BOTH)
        self.bottomView = tk.Frame(self, width=getActualWidth(win_px_width))#, bg='orange')
        self.bottomView.propagate(False)
        self.bottomView.pack(fill=tk.BOTH)

        self.setCenterWindow()

        self.addTopView()
        self.addCenterView()
        self.addBottomView()

        print 'width: ', self.winfo_width()
        print 'height: ', self.winfo_height()
        self.ser=Serial()
        self.ser.setPort('/dev/ttyUSB0')
        self.ser.setBaudrate(9600)

    def addTopView(self):
        # step1: add one line
        tk.Button(self.topView, text='Open device', bd=3, command=self.openDevice, width=10).grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        tk.Label(self.topView, text='Device: ', width=10).grid(row=0, column=1, sticky=tk.W)
        self.listValue=tk.StringVar()
        list_devices = ttk.Combobox(self.topView, width=15, textvariable=self.listValue)
        list_devices['values'] = ('/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2')
        list_devices.current(0)
        list_devices.bind('<<ComboboxSelected>>', self.selectedDevice)
        list_devices.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

        # step2: add two line
        tk.Button(self.topView, text='Close device', bd=3, command=self.closeDevice, width=10).grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        tk.Label(self.topView, text='Baud rate: ', width=10).grid(row=1, column=1, sticky=tk.W)
        self.list_baudrate = tk.Listbox(self.topView, width=15, height=1, exportselection=False)
        list_item = ['9600', '19200', '38400', '57600', '115200', '230400', '460800', '576000', '921600']
        for i in list_item:
            self.list_baudrate.insert(tk.END, i)

        scr1 = tk.Scrollbar(self.topView)
        self.list_baudrate.configure(yscrollcommand=scr1.set)
        scr1['command'] = self.list_baudrate.yview
        scr1.grid(row=1, column=3, sticky=tk.W)
        self.list_baudrate.bind('<ButtonRelease>',self.search)
        self.list_baudrate.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

        self.var=tk.IntVar()
        self.log=tk.Checkbutton(self.topView,text='log',variable=self.var,bd=3,command=self.save).grid(row=1,column=6,padx=10,pady=5,sticky=tk.W)
        self.e=tk.StringVar()
        self.e.set('/home/syrup/Desktop/SerialPortTool/message')
        self.label1=tk.Entry(self.topView,textvariable=self.e,width=40)
        self.label1.grid(row=1,column=7,padx=10,pady=5,sticky=tk.W)




    def addCenterView(self):
        print 'center width:', self.centerView['width']
        self.text = tk.Text(self.centerView, width=getActualWidth(win_px_width) - 2, height=self.centerView['height'] - 2)
        self.text.grid(row=0, column=0, padx=pt_unit, pady=pt_unit, rowspan=5, sticky=tk.NW)



        btn_clear = tk.Button(self.centerView, text='Clear0', bd=3, height=1,command=self.clear0)
        btn_clear.grid(row=5, column=0, padx=pt_unit, pady=pt_unit, sticky=tk.NW)

    def addBottomView(self):
        btn_clear = tk.Button(self.bottomView, text='Clear', bd=3, height=1,command=self.clear)
        btn_clear.grid(row=0, column=0, padx=pt_unit, pady=pt_unit, sticky=tk.NW)
        sendfile = tk.Button(self.bottomView, text='sendfile', bd=3, height=1,command=self.sendFile)
        sendfile.grid(row=1, column=0, padx=pt_unit, pady=pt_unit, sticky=tk.NW)





        self.f=tk.StringVar()
        self.f.set('/home/syrup/Desktop/SerialPortTool/message')
        self.sendfile2=tk.Entry(self.bottomView,textvariable=self.f,width=40)
        self.sendfile2.grid(row=1,column=1,padx=pt_unit,pady=pt_unit,sticky=tk.W)






        # btn_clear2 = tk.Button(self.bottomView, text='Clear0', bd=3, height=1)
        # btn_clear2.grid(row=2, column=0, padx=pt_unit, pady=pt_unit, sticky=tk.NW)

        self.input=tk.Button(self.bottomView,text='input',command=self.submit,bd=3,height=1)
        self.input.grid(row=2,column=0,padx=pt_unit,pady=pt_unit,sticky=tk.NW)
        self.input2=tk.Entry(self.bottomView,width=40)
        self.input2.grid(row=2,column=1,padx=pt_unit,pady=pt_unit,sticky=tk.NW)

        self.list2Value=tk.StringVar()
        list_device2=ttk.Combobox(self.bottomView,width=10,textvariable=self.list2Value)
        list_device2['values']=['CRLF','CR','LF']
        list_device2.current(0)
        list_device2.bind('<<ComboboxSelected>>',self.changeDevice)
        list_device2.grid(row=2, column=3, padx=5, pady=5, sticky=tk.W)
        self.changeValue='\r\n'

        self.text2=tk.Text(self.bottomView,width=60,height=3)
        self.text2.grid(row=0,column=1,padx=3,pady=3,sticky=tk.N)



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
        (screen_height) * 1 / 4))  # center window on desktop
        self.deiconify()

    def close(self):
        self.destroy()

    def openDevice(self):
        try:
            self.ser.open()
            if self.ser.isOpen()==True:
                print 'serial has been opened '
                print 'the port is: ',self.ser.port
                print 'the baudrate is: ',self.ser.baudrate
                self.text.insert('end','serial has been opened ')
        except SerialException as e:
            print 'failed to open serial'


    def closeDevice(self):
        self.ser.close()
        if self.ser.isOpen()==False:
            print 'it has been closed '

    def selectedDevice(self,event):
        self.port=self.listValue.get()
        self.ser.setPort(self.port)
        print self.port
    def search(self,event):
        self.bautrate=self.list_baudrate.get(self.list_baudrate.curselection())
        self.ser.setBaudrate(self.bautrate)
        print self.bautrate


    def clearRecvBox(self):
        pass

    def submit(self):
        # context1=self.input2.get()+'\r\n'
        # n=self.ser.write(context1)
        # output=self.ser.read(n)
        # print output
        # self.text.insert(0.0,output)





        if self.ser.isOpen():
            context1=self.input2.get()+self.changeValue
            self.ser.write(context1)
            self.text2.insert('end',self.input2.get()+'\n')
        else:
            print 'please open the serial'
        # self.data=self.recv(self.ser)
        #
        # print self.data
        # # self.text.delete(0.0,END)
        # self.text.insert(0.0,self.data)




    # def recv(self,serial):
    #     s=''
    #     while True:
    #         data=serial.read()
    #         if data=='*':
    #             break
    #         s=s+data
    #
    #         # sleep(0.08)
    #     data=s
    #     return data


    def save(self):
        if self.var.get()==1:
            with open(str(self.label1.get()),'w') as f:
                f.write(self.text.get('0.0','end'))
            print 'has created a file'


    def recv1(self,timeout=100):

        while 1:
            if self.ser.isOpen() == True:
                self.data=self.ser.read()
                self.text.insert('end',self.data)



    def clear0(self):
        self.text.delete('0.0','end')
    def changeDevice(self,event):
        if self.list2Value.get()=='CRLF':
            self.changeValue='\r\n'
            print '\\r\\n'
        if self.list2Value.get()=='CR':
            self.changeValue='\r'
            print '\\r'
        if self.list2Value.get()=='LF':
            self.changeValue='\n'
            print '\\n'

    def sendFile(self):
        if self.ser.isOpen():
            fp=self.sendfile2.get()
            with open(str(fp),'r') as f:
                while True:
                    s=f.readline()

                    if s=='':
                        break
                    print s
                    context1 = s + self.changeValue
                    self.ser.write(context1)
                    self.text2.insert('end', s)
                    sleep(0.5)



    def clear(self):
        self.text2.delete('0.0','end')


def main():
    app = SerialPortFrame()
    thread.start_new_thread(app.recv1, ())
    app.mainloop()

if __name__ == '__main__':
    main()