
import sys
import socket
import time
import threading
from threading import Thread
from SocketServer import ThreadingMixIn
from socket import SHUT_RDWR

JOINING_GAME = 1
CM_SUBSCRIBE = 'Enter Player Name : '
SM_NEW_GAME = ''
GAME_IN_PROGRESS = 0
RINGED = 0
chat = ''
Ring_recieved=0

logs=1
logout=0
thread2_run=0
category=''

class ServerThread(Thread):
 
    def __init__(self,socket):
        Thread.__init__(self)
        self.socket = socket
        
     #   print "New thread started for write"
    def run(self):
        #print "send" 
        global JOINING_GAME
        global SM_NEW_GAME
        global GAME_IN_PROGRESS
        global CM_SUBSCRIBE
        global Ring_recieved
        #print "new first thread spawned"
        while True:
            #print GAME_IN_PROGRESS
            starttime = time.time()                
            if GAME_IN_PROGRESS == 1:
                #print GAME_IN_PROGRESS
                self.category()
                logout=1
                logs=0
                #socket.close()
                sys.exit()
                
            

    def category(self):
        global logout
        global category
        #if GAME_IN_PROGRESS == 1:
                #print "enter game in prog"
        
        while True:  
            try:
            
                category = self.socket.recv(BUFFER_SIZE)
                logout=0
                #threadmsg="run"
                
                catmsg = "To start the round \n Choose one of the category: 1. Politics  2. Science  3. Computer "
                check_ring="Ring if you know the answer. "
                check_ans="What is the answer? "
                checkfinal="End of round, enter a key to continue: "
            #print category
                
            
                if (category == catmsg) == True:
                    
                    cat = raw_input(category)
                        
                    self.socket.send(cat)
                    
                
                 
                elif category==check_ring:
                      
                    ring=raw_input(check_ring)
                         
                    self.socket.send(ring)
                
                elif category==check_ans:
                
                    answer=raw_input(check_ans)
                        
                    self.socket.send(answer)
               
                elif chat == checkfinal:
                     
                    k=raw_input(checkfinal)
                        
                    #self.socket.send(k)
               
                else :
                    
                    print category
                    logout=1
                    logs=1
                    break
        
            except KeyboardInterrupt: 
                
                continue
            except socket.error:
                
                logout=1
                logs=1
                sys.exit()
        return 1


class ServerThreadread(Thread):
 
    def __init__(self,socket):
        Thread.__init__(self)
        self.socket = socket
        
      #  print "New thread started for chat display"
      
    def run(self):
        global counter
        global logs
        #val = False
        global RINGED
        global GAME_IN_PROGRESS
        global s2
        global chat
        global thread2_run
        
        if counter==0:
            while True:
                try:
                
                   
                    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s2.connect((TCP_IP, TCP_PORT2))
                    break
                except :
                    continue
                
            

        
        while True:
            try:
                
            
            #checks for error
                if log == 0:
              #  print "inside loop"
                    #print "Listening inside second thread"
                    chat=s2.recv(BUFFER_SIZE)
                    
                    print chat

                    if (str(chat) == "GAME STARTED !!") == True:
                    #print GAME_IN_PROGRESS
                        GAME_IN_PROGRESS = 1
                    if(str(chat)=="Wait till the game master chooses the category"):
                    
                    #no use now, while making exitn before game to work, logs is used to notify game has started
                        logs=0
                        
            except KeyboardInterrupt:
                
                continue
            except:   # use this when exiting before game starts, no use now
                
                logs=1
                logout=1
                #s2.shutdown(SHUT_RDWR)
                s2.close()
                sys.exit()

             

TCP_IP = '127.0.0.1'
TCP_PORT = int(sys.argv[1])
TCP_PORT2 = 8816
BUFFER_SIZE = 1024
threads = []
global log
global logger
counter=0
logger=0
log = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
TIME_OUT = s.recv(BUFFER_SIZE)   #Server exchanges tmeout details with client at the start of every socket

status = 0
try:
    while status == 0:
        logout=1
        logs=1
        username = raw_input(CM_SUBSCRIBE)
        s.send(username)
        ack1 = s.recv(BUFFER_SIZE)
        print ack1
        logs=0
        status = 1
        JOINING_GAME = 0
except KeyboardInterrupt:
    #logger=1
    
    logout_mes="logout" 
    s.send(logout_mes)  #this to notfy server when a user exits
    
    s.close()
    #s2.close()
    #continue
    #s.close()
    #sys.exit()

while ( status == 1 ):
    #print "logged in"
    try:
        newthread = ServerThread(s)
        newthread.daemon = True
        newthread2 = ServerThreadread(s)
        newthread2.daemon = True
        newthread.start()
        newthread2.start()
        threads.append(newthread)
        threads.append(newthread2)
        while True:
            for t in threads:
                t.join(600)
                if not t.isAlive():
                    break
            break  
        break              
    except KeyboardInterrupt:
        if logs==0:
            counter=1
            exit = 'you cannot exit the game!!'
            print exit
            if chat == "End of round,press a key and enter to continue: ":
                print chat
            else:    
                print category
            continue
        elif logout==1:
            logger=1
            print "exiting the game"
            #s.shutdown(SHUT_RDWR)
            s.close()
            #s2.shutdown(SHUT_RDWR)
            #s2.close()
            
            sys.exit()
        elif(logout==0):  
            counter=1
            
            print exit
            print category
            continue
    
   
            
    

 

