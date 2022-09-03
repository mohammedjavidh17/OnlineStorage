import socket
import pandas as pd

HOST = '10.5.247.136'
PORT = 42051
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print ("Server running", HOST, PORT)
s.listen(1)
cnt =0


#predefines
def reply(clnt, rep):
    ts = 'READY'
    clnt.send(ts.encode('utf-8'))
def cmd(cmd, conn):
    cmd = cmd.decode("utf-8")
    if cmd.split()[0] == "AUTH":
        print("requesed For auth")
        reply(conn, 'r')
        return 'None'
    elif cmd.split()[0] == '-1':
        return 'break'

def Authn(cmd):
    id = cmd.split()[1]
    pas = cmd.split()[2]
    df = pd.read_csv("assets\user.csv")
    for indx in df.shape[0]:
        if df.iloc[indx:0] == pas:
            pass
while True:
    conn, addr = s.accept()
    print('Connected by', addr)
    cnt = cnt+1
    conn.send(str('READY').encode('utf-8'))
    while True:
        rep = conn.recv(1024)
        print(rep)
        if rep.split()[0].decode('utf-8') == 'AUTH':
            print("Reqested authetication")
