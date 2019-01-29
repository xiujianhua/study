from tkinter import *
from tkinter.messagebox import *
import sys
import time
from socket import *
from tkinter import ttk


class InputFrame(Frame):
    def __init__(self, master, s):
        Frame.__init__(self, master)
        self.s = s
        self.create_page()

    def create_page(self):
        group = StringVar()
        group.set('填入类型')

        def save(s):
            ask = t1.get(1.0, END)
            answer = t2.get(1.0, END)
            group1=c.get()
            
            data = 'S##%s##%s##%s' % (group1,ask, answer)
            s.send(data.encode())

        t1 = Text(self, height=40, width=50)
        t1.grid(row=1, column=0)
        t1.insert(INSERT,'填入问题')

        t2 = Text(self, height=40, width=50)
        t2.grid(row=1, column=2)
        t2.insert(INSERT, '填入答案')
        c = ttk.Combobox(self,textvariable=group)
        c['values'] = ('1.网络编程','2.进程线程','3.MySQL基础','4.MongDB','5.正则表达式','6.git')
        c.grid(row=2, column=2)
        Button(self, text='存入题库', command=lambda s=None: save(self.s)).grid(row=2, column=3)


class QueryFrame(Frame):
    def __init__(self, master, s):
        Frame.__init__(self, master)
        self.s = s
        self.create_page()

    def create_page(self):
        group = StringVar()
        group.set('填入类型')

        def ask(s):
            data = 'L##%s'%group.get()
            s.send(data.encode())
            data = s.recv(1024).decode()
            l = data.split('##')
            print(l)
            t1.delete(1.0, END)
            t1.insert(INSERT, '%s'%l[0])
            t1.tag_add('answer', '1.0', END)
            t1.tag_config('answer',font=('Calibri',12))
            t2.delete(1.0, END)
            t2.insert(INSERT, '%s'%l[1])
            t2.tag_add('answer', '1.0', END)
            t2.tag_config('answer', foreground='white',font=('Calibri',12))

        def answer():
            t2.tag_add('answer', '1.0', END)
            t2.tag_config('answer',  foreground='black')



        t1 = Text(self, height=40, width=50)
        t1.grid(row=1, column=1)
        t1.insert(INSERT, '1')

        t2 = Text(self,height=40, width=50)
        t2.grid(row=1, column=2)
        t2.insert(INSERT, '1')


        Button(self, text='随机抽题', command=lambda s=None: ask(self.s)).grid(row=2, column=1)
        Button(self, text='显示答案', command=answer).grid(row=2, column=2)


class CountFrame(Frame):
    def __init__(self, master, s):
        Frame.__init__(self, master)
        self.s = s
        self.create_page()

    def create_page(self):
        Label(self, text='count page').grid()


class AboutFrame(Frame):
    def __init__(self, master, s):
        Frame.__init__(self, master)
        self.s = s
        self.create_page()

    def create_page(self):
        Label(self, text='about page').grid()
