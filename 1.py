from pymongo import MongoClient
from socket import *
from multiprocessing import *
from random import randint
import signal
import sys
import time


class main(object):
    def __init__(self, addr,file_no):
        self.file_no = file_no
        self.s = socket()
        self.connect(addr)

    def connect(self, addr):
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s.bind(addr)
        self.s.listen(3)
        print('listen to', addr)
        while True:
            try:
                c, addr = self.s.accept()
            except KeyboardInterrupt:
                sys.exit('已经键盘退出')
            except Exception as e:
                print('错误:', e)
                continue
            else:
                print('connect from', addr)
            p = Process(target=self.handle, args=(c,))
            p.start()
            c.close()

    def handle(self, c):
        print('开启新进程：', c.getpeername())
        self.s.close()
        while True:
            data = c.recv(1024).decode()
            if not data:
                sys.exit('客户端退出')
            l = data.split('##')
            if l[0] == 'S':
                self.db_insert(l)
            elif l[0] == 'L':
                self.db_load(c,l)
            elif l[0] == 'U':
                self.file_no_check(c,l)
            elif l[0] == 'G':
                self.sendfile(c,l)
            elif l[0] == 'R':
                self.do_register(c,l)
            elif l[0] == 'I':
                self.do_login(c,l)

    def do_login(self,c,l):
        c_id = l[1]
        c_passw = l[2]
        conn = MongoClient('localhost', 27017)
        db = conn['text']
        myset = db['account']
        a = myset.find({})
        for i in a:
            if i['id'] == c_id and i['passw'] == c_passw:
                c.send(b'OK')
                return
        else:
            msg = '账号或密码不正确'
            c.send(msg.encode())



    def do_register(self,c,l):
        c_id = l[1]
        c_name =l[2]
        c_passw = l[3]
        conn = MongoClient('localhost', 27017)
        db = conn['text']
        myset = db['account']
        a = myset.find({})
        for i in a:
            if i['name'] == c_name or i['id'] == c_id:
                data = '用户名或昵称已被使用'
                c.send(data.encode())
                return

        myset.insert_one({'id': '%s'%c_id, 'name': '%s'%c_name, 'passw': '%s'%c_passw})
        c.send(b'OK')
        conn.close()


    def sendfile(self,c,l):
        filename= l[1]
        try:
            fb = open(filename, 'rb')
        except Exception:
            c.send('文件不存在'.encode())
            return
        c.send(b'OK')
        time.sleep(0.1)
        while True:
            data = fb.read(1024)
            if not data:
                time.sleep(0.1)
                c.send(b'###')
                break
            c.send(data)


    def file_no_check(self,c,l):
        data = self.file_no
        c.send(data.encode())

    def db_load(self,c,status):
        conn = MongoClient('localhost', 27017)
        db = conn['text']
        myset = db['season2']
        a = myset.find({})
        l=[]
        for i in a:
            l.append(i)
        ro = randint(0,len(l)-1)
        data = "%s##%s"%(l[ro]['Ask'],l[ro]['Answer'])
        time.sleep(0.1)
        c.send(data.encode())
        conn.close()


    def db_insert(self, l):
        conn = MongoClient('localhost', 27017)
        db = conn['text']
        myset = db['season2']
        myset.insert_one({'Ask': '%s' % l[2],'Answer': '%s' % l[3],'Type': '%s' % l[1]})
        a = myset.find({}, {'_id': 0})
        for i in a:
            print(i)
        conn.close()


if __name__ == '__main__':
    HOST = '0.0.0.0'
    file_no = '4.0'
    PORT = 6671
    ADDR = (HOST, PORT)
    main(ADDR,file_no)
