import socket # server
HOST = '10.7.234.196'
PORT = 41201
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(1)
con, add = s.accept()
print('Connected')
file = open("D:\BU15948_stocks.csv")
while True:
    for x in file:
        con.send(x.encode('utf-8'))
    break