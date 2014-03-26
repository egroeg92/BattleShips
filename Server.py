"""

Server

Author: George Macrae
2014

"""


from socket import *
import threading
import sys

import os

count = 0
lock = threading.Lock()

def handler(clientsocket, clientaddr):
    print "Accepted connection from: ", clientaddr
    print clientsocket
    clients.append(clientsocket)
    oppAddr = ''
    oppSock = ''
    while 1:
        data = '' 
        data = clientsocket.recv(1024)
        name = str(clientaddr[1])
        print matchup_sockets
        print name+" has "+ data
        

        if data == 'Signed Out' :
            clientsocket.send('Signout')
            matchup_address.remove(clientaddr[1])
            matchup_sockets.remove((clientsocket,clientaddr[1]))
            connections.remove((clientsocket,clientaddr[1]))
            for x in matchup_sockets:
                x[0].send(str(matchup_address))    
            break

        elif data == 'SetupC' :
            # clientsocket.send('Set up')
            print 'SetupC'
            clientsocket.send('Setup')
            matchup_address.remove(clientaddr[1])
            matchup_sockets.remove((clientsocket,clientaddr[1]))
            for x in matchup_sockets:
                x[0].send(str(matchup_address))
            
        
        elif data == 'SetupA' :
            print 'SetupA'
            matchup_address.remove(clientaddr[1])
            matchup_sockets.remove((clientsocket,clientaddr[1]))
            for x in matchup_sockets:
                x[0].send(str(matchup_address))

            # break

        elif data == 'Matchup' :
            print 'MATCHUP'
            matchup_address.append(clientaddr[1])
            matchup_sockets.append((clientsocket,clientaddr[1]))
            if (clientsocket,clientaddr[1]) not in connections:
                print 'just once'
                connections.append((clientsocket,clientaddr[1]))
            for x in matchup_sockets:
                x[0].send(str(matchup_address))
                
        elif data == 'StartGame':
            print "STARTED"
            print 'oppAddr = '+ str(oppAddr)
            print 'oppSock = ' + str(oppSock)

        elif data == 'LoseGame':
            print 'LoseGame'
            oppSock.send('Win')
            clientsocket.send('Lose')
        elif data == 'BreakListener':
            clientsocket.send('BreakListener')

        dataList = data.split(':')

        # SIGNING IN
        if dataList[0] == 'Login':
            un = dataList[1]
            pw = dataList[2]
            print un
            print pw
            si = False
            lock.acquire()
            try:
                f = open('users.dat','r')
                content = f.readlines()
                for c in content:
                    c1 =c.split(':')
                    print str(c1[0])
                    print str(c1[1])[:-1]
                    if str(c1[0]) == str(un) and str(c1[1])[:-1] == str(pw):
                        print 'login success!'
                        clientsocket.send('SignedIn')
                        si = True
                        break
                if not si:
                    clientsocket.send('DNE')
                f.close()
            finally:
                lock.release()

        elif dataList[0] == 'SignUp':
            un = dataList[1]
            pw = dataList[2]
            write = True
            lock.acquire()
            try:

                f = open('users.dat','r')
                content = f.readlines()
                print content
                for c in content:
                    print c[0]

                    c1 = c.split(':')
                    if str(c1[0]) == str(un):
                        print c1[0]
                        print 'UN already exists...'
                        clientsocket.send('exists')
                        write = False
                        break
                if write:
                    f.close()
                    print 'writing'
                    f = open('users.dat','a')
                    f.write(str(un)+':'+str(pw)+'\n')
                    clientsocket.send('SignedIn')
                f.close()
            finally:
                lock.release()
        elif dataList[0] == 'Disconnect':
            break
                
        elif dataList[0] == 'Challenge':
            print 'challenge'

            for x in matchup_sockets:
                print str(x[1])+ dataList[1]
                if str(x[1]) == dataList[1]:
                    x[0].send("CHALLENGED"+str(clientaddr[1]))

        elif dataList[0] == 'Accept':
            print 'accepted'
            print dataList
            for x in matchup_sockets:
                if str(x[1]) == dataList[1]:
                    x[0].send('ACCEPTED'+str(clientaddr[1]))

        elif dataList[0] == 'ExitSetup':
            print 'ExitSetup'
            exiter = dataList[1]
            for x in connections:
                if(str(x[1]) ==  str(exiter)):
                    x[0].send('ExitSetup')
            oppAddr = ''
            oppSock = ''
            
        elif dataList[0] == 'Ready':
            oppAddr = dataList[1]
            for x in connections:
                if (str(x[1]) == str(oppAddr)):
                    oppSock = x[0]
                    oppSock.send('OppReady')
        
        elif dataList[0] == 'Move':
            oppSock.send('Move:'+dataList[1]+':'+dataList[2]+':'+dataList[3]+':'+dataList[4])

        elif dataList[0] == 'Position':
            print str(dataList)
            oppSock.send(str(dataList))
        elif dataList[0] == 'Turn':
            oppSock.send('Turn:'+dataList[1]+':'+dataList[2]+':'+dataList[3]+':'+dataList[4])
        elif dataList[0] == 'Cannon':
            oppSock.send('Cannon:'+dataList[1]+':'+dataList[2]+':'+dataList[3])
        elif dataList[0] == 'HCannon':
            oppSock.send('HCannon:'+dataList[1]+':'+dataList[2]+':'+dataList[3])
        elif dataList[0] == 'Torpedo':
            oppSock.send('Torpedo:'+dataList[1]+':'+dataList[2]+':'+dataList[3])
            
            
        
 
if __name__ == "__main__":
 
    host = gethostbyname(gethostname())
    # host = '127.0.0.1'
    port = 9999
    addr = (host, port)
 
    print host
    serversocket = socket(AF_INET, SOCK_STREAM)
 
    serversocket.bind(addr)
    print "Server is listening for matchup_sockets\n"

    serversocket.listen(2)
    

    global clients
    global matchup_address
    global matchup_sockets
    global connections
    clients = []
    connections = []
    matchup_sockets = []
    matchup_address = []
    while 1:
 
        clientsocket, clientaddr = serversocket.accept()
        h_thread = threading.Thread(target = handler, args = (clientsocket, clientaddr))
        h_thread.start()
