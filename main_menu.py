from myview import *





class Main_page(object,):
    def __init__(self, master=None,s=None):
        self.s = s
        self.root = master
        self.root.geometry('800x600')
        self.root.title('main')
        self.create_page()

    def create_page(self):
        self.input_page = InputFrame(self.root,self.s)
        self.query_page = QueryFrame(self.root,self.s)
        self.count_page = CountFrame(self.root,self.s)
        self.about_page = AboutFrame(self.root,self.s)
        self.query_page.pack()

        menubar = Menu(self.root)
        menubar.add_command(label='查询', command=self.queryData)
        menubar.add_command(label='题库录入', command=self.inputData)
        menubar.add_command(label='统计', command=self.countData)
        menubar.add_command(label='关于', command=self.aboutData)
        self.root['menu'] = menubar

    def inputData(self):
        self.input_page.pack()
        self.query_page.pack_forget()
        self.count_page.pack_forget()
        self.about_page.pack_forget()

    def queryData(self):
        self.input_page.pack_forget()
        self.query_page.pack()
        self.count_page.pack_forget()
        self.about_page.pack_forget()

    def countData(self):
        self.input_page.pack_forget()
        self.query_page.pack_forget()
        self.count_page.pack()
        self.about_page.pack_forget()

    def aboutData(self):
        self.input_page.pack_forget()
        self.query_page.pack_forget()
        self.count_page.pack_forget()
        self.about_page.pack()
