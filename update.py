from socket import *
import os
from time import sleep



def main(addr,filename):
    sockfd = socket()
    try:
        sockfd.connect(addr)
    except Exception as e:
        print(e)
    sockfd.send(('G##' + filename).encode())
    data = sockfd.recv(128).decode()
    if data == 'OK':
        try:
            fd = open(filename,'wb')
        except Exception as e:
            print('open file error:',e)
        else:
            while True:
                data = sockfd.recv(1024)
                if data == b'###':
                    break
                fd.write(data)
                print('writing',data)
        finally:
            fd.close()
        print('fd close')

    else:
        print(data)

if __name__ == '__main__':
    print("updata is running")
    addr = ('176.136.4.36',6671)
    filename= ['main.py','main_menu.py','login.py','myview.py','1.py']
    for i in filename:
        sleep(0.5)
        main(addr,i)
    os.system('python3 main.py')


