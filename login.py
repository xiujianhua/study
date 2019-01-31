from main_menu import *
import os



class Login_page(object):
    def __init__(self, master,ADDR,file_no):
        self.ADDR = ADDR
        self.root = master
        self.file_no = file_no
        self.root.geometry('300x180')
        self.s = socket()
        try:
            self.s.connect(self.ADDR)
            print('链接成功')
        except Exception as e:
            showerror('connect error :', '%s' % e)
            sys.exit()
        self.username = StringVar()
        self.password = StringVar()
        self.create_page()

    def create_page(self):
        self.page = Frame(self.root)
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)
        Label(self.page, text='账户:').grid(row=1, pady=10, stick=W)
        Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=E)
        Label(self.page, text='密码: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.password, show='*').grid(row=2, column=1, stick=E)
        Button(self.page, text='登陆', command=self.loginCheck).grid(row=3, stick=W, pady=10)
        Button(self.page, text='退出', command=self.page.quit).grid(row=3, column=2, stick=E)
        Button(self.page, text='注册',command=self.register).grid(row=3, column=1)


    def register(self):
        def do_reg():
            if ' ' in id.get() or not id.get():
                showerror('error','账号不能为空,不能含有空格')
                return
            if ' ' in name.get() or not name.get():
                showerror('error','昵称不能为空,不能含有空格')
                return
            if ' ' in passw1.get() or not passw1.get():
                showerror('error','密码不能为空,不能含有空格')
                return
            if passw1.get() != passw2.get():
                showerror('error','两次密码不一致')
                return

            data='R##%s##%s##%s'%(id.get(),name.get(),passw1.get())
            self.s.send(data.encode())
            data = self.s.recv(128).decode()
            if data == 'OK':
                showinfo('恭喜','注册成功')
                regpage.destroy()
            else:
                showinfo('error','%s'%data)




        regpage=Toplevel(self.root)
        regpage.title('注册')
        regpage.geometry('300x300')
        id = StringVar()
        id.set(' 此处乱填应有各种bug...')
        name = StringVar()
        name.set(' 此处乱填应有各种bug...')
        passw1 = StringVar()
        passw2 = StringVar()
        Label(regpage).grid(row=0, stick=W)
        Label(regpage, text='账户:').grid(padx=25,row=1, column=1,pady=10)
        Entry(regpage, textvariable=id).grid(row=1, column=2)
        Label(regpage, text='昵称:').grid(row=2,column=1, pady=10)
        Entry(regpage, textvariable=name).grid(row=2, column=2)
        Label(regpage, text='密码: ').grid(row=3, column=1, pady=10)
        Entry(regpage, textvariable=passw1,show='*').grid(row=3, column=2)
        Label(regpage, text='重复密码:').grid(row=4, column=1, pady=10)
        Entry(regpage, textvariable=passw2, show='*').grid(row=4, column=2)
        Button(regpage, text='退出', command=regpage.destroy).grid(row=5, column=2)
        Button(regpage, text='注册', command=do_reg).grid(row=5, column=1)




    def update(self,s):
        data = 'U##%s'%self.file_no
        s.send(data.encode())
        data = s.recv(128).decode()
        print('recv file no :',data)
        if data > self.file_no:
            choo = askokcancel('识别该软件版本为旧版本', '需要升级到最新的版本吗？')
            if choo == True:
                try:
                    os.system("python3 update.py")
                except Exception as e:
                    showinfo('updata error','%s'%e)
                else:
                    sys.exit()
            else:
                return
        return

    def loginCheck(self):
        name = self.username.get()
        passwd = self.password.get()
        data = 'I##%s##%s'%(name,passwd)
        self.s.send(data.encode())
        data = self.s.recv(128).decode()
        if data=='OK':
            self.update(self.s)
            self.page.destroy()
            Main_page(self.root,self.s)
        else:
            showinfo(title='error', message='%s'%data)
