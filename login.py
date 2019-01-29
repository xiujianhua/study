from main_menu import *



class Login_page(object):
    def __init__(self, master,ADDR,file_no):
        self.ADDR = ADDR
        self.s = socket()
        self.root = master
        self.file_no = file_no
        self.root.geometry('300x180')
        self.username = StringVar()
        self.username.set('a')
        self.password = StringVar()
        self.password.set('a')
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
        Button(self.page, text='注册').grid(row=3, column=1)

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
        try:
            self.s.connect(self.ADDR)
            print('链接成功')
        except Exception as e:
            showerror('connect error :','%s'%e)
        else:
            name = self.username.get()
            passwd = self.password.get()
            if name == 'a' and passwd == 'a':
                self.update(self.s)
                self.page.destroy()
                Main_page(self.root,self.s)
            else:
                showinfo(title='error', message='账号密码错误')
