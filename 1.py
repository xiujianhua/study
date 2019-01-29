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
    def sendfile(self,c,l):
        filename= l[1]
        print(filename)
        try:
            fb = open(filename, 'rb')
        except Exception:
            c.send('文件不存在'.encode())
            print('文件不存在')
            return
        c.send(b'OK')
        time.sleep(0.1)
        while True:
            data = fb.read(1024)
            print(data)
            if not data:
                time.sleep(0.1)
                c.send(b'###')
                break
            c.send(data)
            print('sending',data)
        print('send finished')

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
        print(l[ro]['Ask'])
        print(l[ro]['Answer'])
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
