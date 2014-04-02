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
    un = ''
    clients.append(clientsocket)
    oppAddr = ''
    oppSock = ''
    while 1:
        data = '' 
        data = clientsocket.recv(1024)
        name = str(clientaddr[1])
        print matchup_sockets
        print name+" has "+ data
        



        if data == 'SetupC' :
            # clientsocket.send('Set up')
            print 'SetupC'
            clientsocket.send('Setup')
            matchup_address.remove(str(un))
            matchup_sockets.remove((clientsocket,str(un)))
            for x in matchup_sockets:
                x[0].send(str(matchup_address))
            
        
        elif data == 'SetupA' :
            print 'SetupA'
            matchup_address.remove(str(un))
            matchup_sockets.remove((clientsocket,str(un)))
            for x in matchup_sockets:
                x[0].send(str(matchup_address))

            # break

        elif data == 'StartGame':
            print "STARTED"
            print 'oppAddr = '+ str(oppAddr)
            print 'oppSock = ' + str(oppSock)

        elif data == 'WinGame':
            n = un.split(';')
            w = int(n[2]) + 1
            print w
            un = (n[0] + '; Wins; '+str(w)+' ; Loses; '+n[4])
            print 'WIN ',un

        elif data == 'LoseGame':
            print 'LoseGame'

            oppSock.send('Win')
            clientsocket.send('Lose')

            n = un.split(';')
            l = int(n[4]) + 1
            print l
            un = (n[0] + '; Wins; '+n[2]+' ; Loses; '+str(l))
            print 'Lose ',un


        elif data == 'BreakListener':
            clientsocket.send('BreakListener')

        dataList = data.split(':')

        if dataList[0] == 'Signed Out' :
            clientsocket.send('Signout')
            matchup_address.remove(str(un))
            matchup_sockets.remove((clientsocket,str(un)))
            connections.remove((clientsocket,str(un)))
            for x in matchup_sockets:
                x[0].send(str(matchup_address))

            user = dataList[1]
            print user
            lock.acquire()
            try:
                f = open('users.dat','r+')
                f2 = open('tmp.dat', 'w+')
                f2.write('')
                f2.close()
                f2 = open('tmp.dat', 'a+')
                content = f.readlines()
                for c in content:
                    c1 =c.split(':')
                    print str(c1[0])
                    print str(c1[1])
                    if str(c1[0]) == str(user):
                        stri = un.split(';')
                        w = stri[2]
                        w = w.replace(' ','')
                        l = stri[4]
                        l = l.replace(' ','')
                        l = l.replace('\n','')
                        x = str(c1[0])+':'+str(c1[1])+':OFFLINE:'+w+':'+l+'\n'
                        f2.write(x)
                    else:
                        x = str(c1[0])+':'+str(c1[1])+':'+str(c1[2])+':'+str(c1[3])+':'+str(c1[4])
                        
                        f2.write(x)

                f.close()
                f = open('users.dat','w')
                f.write('')
                f.close()
                f = open('users.dat','a+')
                f2.close()
                f2 = open('tmp.dat','r')

                content = f2.readlines()
                for c in content:
                    print c
                    f.write(c)

                f.close()
                f2.close()
            finally:
                lock.release() 
            
            break

        # SIGNING IN
        elif dataList[0] == 'Login':
            un = dataList[1]
            pw = dataList[2]

            print un
            print pw
            w = '0'
            l = '0'
            si = False
            lock.acquire()
            try:
                f = open('users.dat','r+')
                f2 = open('tmp.dat', 'w+')
                f2.write('')
                f2.close()
                f2 = open('tmp.dat', 'a+')
                content = f.readlines()
                for c in content:
                    c1 =c.split(':')
                    print str(c1[0])
                    print str(c1[1])
                    if str(c1[0]) == str(un) and str(c1[1])== str(pw) and str(c1[2]) == 'OFFLINE':
                        print 'login success!'
                        x = str(c1[0])+':'+str(c1[1])+':ONLINE:'+str(c1[3])+':'+str(c1[4])
                        w = str(c1[3])
                        l = str(c1[4])
                        f2.write(x)
                        clientsocket.send('SignedIn')
                        si = True
                        
                    else:
                        x = str(c1[0])+':'+str(c1[1])+':'+str(c1[2])+':'+str(c1[3])+':'+str(c1[4])
                        f2.write(x)

                if not si:
                    clientsocket.send('Does not exist or already logged in')
                else:

                    f.close()
                    f = open('users.dat','w')
                    f.write('')
                    f.close()
                    f = open('users.dat','a+')
                    f2.close()
                    f2 = open('tmp.dat','r')
                    content = f2.readlines()
                    for c in content:
                        f.write(c)

                    l = l.replace('\n','')
                    print "YOOO",l
                    un = (str(un) + '; Wins; '+w+' ; Loses; '+l)


                f.close()
                f2.close()
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
                    f.write(str(un)+':'+str(pw)+':ONLINE:0:0\n')
                    un = (str(un) + '; Wins; 0 ; Loses; 0')
                    clientsocket.send('SignedIn')
                f.close()
            finally:
                lock.release()
                
            
        
        elif dataList[0] == 'Matchup' :
            print 'MATCHUP'

            matchup_address.append(str(un))
            matchup_sockets.append((clientsocket,str(un)))

            if (clientsocket,str(un)) not in connections:
                connections.append((clientsocket,str(un)))
            for x in matchup_sockets:
                x[0].send(str(matchup_address))
                
        elif dataList[0] == 'Disconnect':
            break
                
        elif dataList[0] == 'Challenge':
            print 'challenge'

            for x in matchup_sockets:
                if str(x[1]) == str(dataList[1])[1:-1]:
                    print str(x[0])
                    x[0].send(":CHALLENGED:"+str(un))

        elif dataList[0] == 'Accept':
            print 'accepted'
            print dataList
            for x in matchup_sockets:
                if str(x[1]) == dataList[1]:
                    x[0].send(':ACCEPTED:'+str(un))

        elif dataList[0] == 'ExitSetup':
            print 'ExitSetup'

            exiter = dataList[1]
            print exiter
            for x in connections:
                print x[1],exiter
                if(str(x[1]) ==  str(exiter)):
                    x[0].send('ExitSetup')
            oppAddr = ''
            oppSock = ''
            
        elif dataList[0] == 'Ready':
            oppAddr = dataList[1]
            for x in connections:
                print (str(x[1])) , str(oppAddr)

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
        elif dataList[0] == 'Repair':
            oppSock.send('Repair:'+dataList[1])
            
            
        
 
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
