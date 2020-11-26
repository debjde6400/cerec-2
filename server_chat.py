import socket

s = socket.socket()
host = socket.gethostname()
port = 10001
s.bind((host, port))

s.listen(5)

while True:
    c, addr = s.accept()
    print('Got connection from : ',addr)
    txt = input("Message:")
    c.send('Napa says thank you.')
    c.close()