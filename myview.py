from tkinter import *
from tkinter.messagebox import *
import sys
import time
from socket import *
from tkinter import ttk
from random import randint


class Do_random(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.create_page()

    def create_page(self):
        def dorandom():
            no = randint(start.get(), end.get())
            Label(self, text='恭喜 %s 号同学！！' % no, pady='50', font=('Calibri', 30)).grid(row=4, column=1, columnspan=3)

        start = IntVar()
        end = IntVar()
        start.set(1)
        end.set(17)
        Label(self, pady='10').grid(row=0, column=1)
        Label(self, text='随机起始值', pady='10').grid(row=1, column=1)
        Label(self, text='随机终止值', pady='10').grid(row=2, column=1)
        Entry(self, textvariable=start).grid(row=1, column=2)
        Entry(self, textvariable=end).grid(row=2, column=2)
        Button(self, text='随机选个号', command=dorandom, pady='30', font=('Calibri', 12)).grid(row=3, column=1)


class InputFrame(Frame):
    def __init__(self, master, s):
        Frame.__init__(self, master)
        self.s = s
        self.create_page()

    def create_page(self):
        name = StringVar()
        name.set('--上传者姓名--')

        type = StringVar()
        type.set('--输入新的类型--')

        def save(s):
            type1 = c.get()
            name1 = name.get()
            if type1 == '--输入新的类型--':
                showerror('error', '请选择题目类型...')
                return
            elif name1 == '--上传者姓名--':
                showerror('error', '输入大名')
                return
            ask = t1.get(1.0, END)
            answer = t2.get(1.0, END)
            data = 'S##%s##%s##%s##%s' % (type1, name1, ask, answer)
            s.send(data.encode())
            data = s.recv(128).decode()
            if data == 'OK':
                showinfo('感谢您','题目上传成功！')
                t1.delete(1.0, END)
                t2.delete(1.0, END)
                type.set('--输入新的类型--')
            else:
                showerror('有bug！','%s'%data)



        def create_type():
            showinfo('error','功能等待完善')

        t1 = Text(self, height=5, width=80)
        t1.grid(row=2, columnspan=4)
        t1.insert(INSERT, '填入问题')

        t2 = Text(self, height=15, width=80)
        t2.grid(row=3, columnspan=4)
        t2.insert(INSERT, '填入答案')

        c = ttk.Combobox(self, textvariable=type)
        c['values'] = ['1.网络编程', '2.进程线程', '3.MySQL基础', '4.MongDB', '5.正则表达式', '6.git']
        c.grid(row=0, sticky=W)
        Entry(self, textvariable=name).grid(row=0, column=1)
        Button(self, text='存入题库', command=lambda s=None: save(self.s)).grid(row=0, column=2)
        Button(self, text='新建题型', command=create_type).grid(row=0, column=3)


class QueryFrame(Frame):
    def __init__(self, master, s):
        Frame.__init__(self, master)
        self.s = s
        self.create_page()

    def create_page(self):
        group = StringVar()
        group.set('填入类型')
        flag = 1
        type = StringVar()
        type.set('--题目类型--')
        name = StringVar()
        name.set('--上传人--')

        def ask(s):
            nonlocal flag
            if flag == 1:
                data = 'L##%s' % group.get()
                s.send(data.encode())
                data = s.recv(1024).decode()
                self.l = data.split('##')
                t1.delete(1.0, END)
                t1.insert(INSERT, '%s' % self.l[0])
                t1.tag_add('answer', '1.0', END)
                t1.tag_config('answer', font=('Calibri', 12))
                type.set('题目类型：%s'%self.l[2])
                name.set('上传者：%s'%self.l[3])
                flag = 0
            else:
                t1.insert(INSERT, '%s' % self.l[1])
                t1.tag_add('answer', '1.0', END)
                t1.tag_config('answer', font=('Calibri', 12))
                flag = 1

        t1 = Text(self, height=30, width=80)
        t1.grid(row=2, column=1, columnspan=4)
        Label(self, textvariable=type, pady='10').grid(row=1, column=2)
        Label(self, textvariable=name, pady='10').grid(row=1, column=3)
        Button(self, text='随机抽题', command=lambda s=None: ask(self.s)).grid(row=1, column=1)


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
