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
    id = cmd.split()[1].decode('utf-8')
    pas = cmd.split()[2].decode('utf-8')
    df = pd.read_csv("assets\\user.csv")
    for indx in range(df.shape[0]):
        if str(df.iloc[indx,0]) == str(id):
            if str(df.iloc[indx, 1]) == str(pas):
                return True
            else:
                return False
while True:
    conn, addr = s.accept()
    print('Connected by', addr)
    cnt = cnt+1
    conn.send(str('READY').encode('utf-8'))
    while True:
        rep = conn.recv(1024)
        print(rep)
        try:
            rep.split()[0]
        except:
            continue
        if rep.split()[0].decode('utf-8') == 'AUTH':
            if Authn(rep):
                conn.send(b'GET')
                UserId = rep.split()[1]
                #assets\data\U10001\config.csv
                file = "assets\data\\"+'U'+str(UserId.decode('utf-8'))+"\config.csv"
                f = open(file)
                conn.recv(1)
                conn.sendall(f.read().encode('utf-8'))  #SEND FILE
                f.close()
                conn.recv(1)
                while True:
                    conn.send(b"READY")
                    cmd2 = conn.recv(1024)
                    try:
                        cmd2.split()[0]
                    except:
                        continue
                    if cmd2.split()[0] == b'READ':
                        lstCmd2 = cmd2.split()   #['READ', '<FILENO>/INDX']
                        file = "assets\data\\"+'U'+str(UserId.decode('utf-8'))+"\\"+str(lstCmd2[1].decode('utf-8'))+".txt"
                        f = open(file)
                        conn.sendall(f.read().encode('utf-8')) #SEND FILE
                        f.close()
                        conn.recv(1)
                        conn.send(b"READY")
                    elif cmd2.split()[0] == b'WRITE':  #['WRITE', '<FileNAme>', extention]
                        lstCmd2 = cmd2.split()
                        config = pd.read_csv(file)
                        configN = pd.DataFrame({
                            "Fileno" : [config.shape[0]+1],
                            "FileName": [lstCmd2[1].decode('utf-8')],
                            "extention":[lstCmd2[2].decode('utf-8')]
                        })
                        config = config.append(configN, ignore_index=True)
                        conn.send(b'READY')
                        fileTXT = conn.recv(40000000)
                        file = "assets\data\\"+'U'+str(UserId.decode('utf-8'))+"\\"+str(config.shape[0])+".txt"
                        DES = open(file, 'w')
                        DES.write(str(fileTXT.decode('utf-8')))
                        file = "assets\data\\"+'U'+str(UserId.decode('utf-8'))+"\config.csv"
                        config.to_csv(file, index=False)
                    elif cmd2.split()[0] == "NEW": #[NEW, "ID", "pas"]
                        NewId = cmd2.split()[1]
                        file = "assets\data\\U"+str(NewId)+"\\config.csv"
                        Sam = pd.read_csv("EmpytyConfig.csv")
                        Sam.to_csv(file, index=False)
                        conn.send(b'DONE')  #Confirmation
                    elif cmd2.split()[0] == 'DIS': #["DIS", "DUMMY"]
                        conn.close()
            else: 
                conn.send(b"FAILED")
