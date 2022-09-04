import socket
from tkinter import messagebox
import pandas as pd
HOST = '10.5.247.136'
PORT = 42051

def ThrowError():
    messagebox.showerror('Error', 'Unable To connect to server')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print('Conencted')

#ThrowError()

def csvOrga(dta:bytes) -> pd.DataFrame:
    f = open("buffer.txt", 'w')
    f.write(dta.decode('utf-8'))
    f.close()
    return pd.read_csv('buffer.txt')

def command(clnt, rep):
    ts = "None"
    if(rep == 'r'):
        ts == "REC"
    elif(rep == 'iv'):
        ts == "INV"
    elif(rep == 'v'):
        ts == "VLD"
    clnt.send(ts.encode('utf-8'))
def reply(cmd):
    print(cmd)
    cmd = cmd.decode("utf-8")
    if cmd == '-1':
        return 'break'

def NewUser(cmd : bytes) -> str:
    rep1 = s.recv(1024)
    print(rep1)
    if rep1 == b'READY':
        s.send(cmd)
        rep2 = s.recv(1024)
        if rep2 == b'DONE':
            return "DONE"
        elif rep2 == b'EXIST': 
            return "EXIST"
        else:
            return "False"
def write():
    rep1 = s.recv(1024)
    file = open('test.txt').read()
    if rep1 == b'READY':
        cmd = "WRITE FILENAME txt"
        s.send(cmd.encode('utf-8'))
        rep2 = s.recv(1024)
        if rep2 == b'READY':
            s.send(file.encode('utf-8'))
def getConfig():
    dta = s.recv(40000000)
    s.send(b' ')
    return dta
def ReqAccess(cmd : str) -> str: 
    s.send(cmd.encode('utf-8'))
    buf = s.recv(1024)
    print(buf)
    if buf == b'GET':
        s.send(b' ')
        return getConfig()
    else:
        return "Invalid"
def GetFile(cmd : str):
    rep1 = s.recv(1024)
    if rep1 == b'READY':
        s.send(cmd.encode('utf-8'))
        a= s.recv(40000000)
        return a
            
    else:
        print("Foo")
        return

while False:    
    A = [s.recv(1024)]
    if A[0].decode('utf-8') == 'READY':
        cmd = input("Enter the command : ")
        s.send(cmd.encode('utf-8'))
        print(s.recv(1024))
    elif A[0].decode('utf-8') == 'BREAK':
        break

    

