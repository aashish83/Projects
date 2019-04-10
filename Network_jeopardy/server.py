import socket
import sys
import collections
import time
import Queue
import threading
import random
import operator

from threading import Thread, Event,Semaphore
from SocketServer import ThreadingMixIn

event=Event()
COLLECT_SUBSCRIPTIONS = 1
CM_SUBSCRIBE =''
SM_NEW_GAME = 'GAME STARTED !!'
GAME_IN_PROGRESS = 0
START_ROUND = 0
RINGING = 0
trial = 0
checker=0

checker1=0

lock = threading.Lock()  
global command
global max_users
global points_dict
points_dict={}
max_users=2
command = ""     
threads =[]     
masterName = ''

dummy = 0
dummy2 = 0
dummy3 = 0 
key=0   
checker=0  

class Barrier:
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.mutex = Semaphore(1)
        self.barrier = Semaphore(0)

    def wait(self):
        self.mutex.acquire()
        self.count = self.count + 1
        self.mutex.release()
        if self.count == self.n: self.barrier.release()
        self.barrier.acquire()
        self.barrier.release()
bar_list=[]
b=Barrier(max_users)
c=Barrier(max_users)
d=Barrier(max_users)
e=Barrier(max_users)
f=Barrier(max_users)
g=Barrier(max_users)
i=Barrier(max_users)
j=Barrier(max_users)
bar_list.append(b)
bar_list.append(c)
bar_list.append(d)
bar_list.append(e)
bar_list.append(f)
bar_list.append(g)
bar_list.append(i)
cat1 = 0
cat =''


sendqueues = {}     #dictionary      
categories = ['Politics ','Science ','Computer ']
ques_dict={}
list_of_questions=[]
q11=(1,("Who is the prime minister of russia? ","putin"))
q12=(1,("Who is the president of America? ","trump"))
q21=(2,("Diamond is made of? ","carbon"))
q22=(2,("What is the Boiling temperature of water in celsius? ","100"))
q31=(3,("What is the measure of a battery? ","mah"))
q32=(3,("Connectionless protocol is? ","udp"))
list_of_questions.append(q11)
list_of_questions.append(q12)
list_of_questions.append(q21)
list_of_questions.append(q22)
list_of_questions.append(q31)
list_of_questions.append(q32)

#years_dict[category#][question#][1,answer]
for line in list_of_questions:
    if line[0] in ques_dict:
       
        ques_dict[line[0]].append(line[1])
       
    else:
        
        ques_dict[line[0]] = [line[1]]

class ClientThread(Thread):      
    def __init__(self,socket,ip,port):
        Thread.__init__(self)
        self.socket = socket
        self.ip = ip
        self.port = port
        

    def run(self):
        global count 
        global CM_SUBSCRIBE
        global key
        global checker
        global round
        global checker1
        global thread2_run
        global max_users
        
        
        round=0
        
        status = 0   
        userpresent = 0    
        userdata = 0
        i = 0
        k = 0
        while True:
            if userdata not in curusers:            
                self.socket.send(str(TIME_OUT))
                
                CM_SUBSCRIBE = self.socket.recv(2048) #player name
                
                if CM_SUBSCRIBE == "logout":
                    max_users = max_users + 1
                    print"logout is received from a client"
                    del sendqueues[self.socket.fileno()]
                    del userlog[self.socket.fileno()]
                    curuser_conn.remove(self.socket)
                    self.socket.close()
                    
                    sys.exit()
                    break
                    
                data2 = "welcome to the game!!!! "
                self.socket.send(data2)  
                lock.acquire()        
                curusers.append(CM_SUBSCRIBE) #add player name to current users list
                lock.release()
               
               
                # mapping id to name
                fd = self.socket.fileno()
                userfd = CM_SUBSCRIBE + " " + str(fd)
                lock.acquire()
                userfdmap.append(userfd)
                points_dict[CM_SUBSCRIBE]=0
                lock.release()
                
                
                thread2_run=1
                
                
                
                #print "maxcount is"+max_users
                self.getData(userdata)
                # self.Ring()
                while(round < 6):
                    if(round>0):
                        if(checker1==0):
                            checker1+=1
                            self.selectMaster()
                            
                        
                   
                    #event here
                    if checker == 0:
                        checker+=1
                        event.wait()
                        event.clear()
                
                    #print "event is crossed for"+str(fd)
                    RingMsg = "Ring if you know the answer. "
                    self.socket.send(RingMsg)
                    
                    resp=self.socket.recv(1024)
                           
                       
                    #print"Resp is received from "+str(fd)
                    if key==0:
                       
                        key+=1
                        for z in userfdmap:
                            zi = z.partition(" ")
                            if zi[2] == str(self.socket.fileno()):
                                ringname = str(zi[0])
                        msgg2 = str(ringname) + " has sent a ring."
                        self.broadcast(msgg2)
                        msgg="What is the answer? "
                        self.socket.send(msgg)
                       
                        answer=self.socket.recv(1024)
                                

                        if(answer.lower() == question[1]):
                            he="Right answerr is entered!!!\n .The answer was "+str(question[1])+".\n"
                            print "Right answerr is entered!!!"
                            self.broadcast(he)
                            checker1=0
                            for z in userfdmap:
                               zi = z.partition(" ")
                               
                               if zi[2] == str(self.socket.fileno()):
                                   #masterfd = int(zi[2])
                                   username=zi[0]
                                   points_dict[username]+=5
                                   point_msg="Scores after this round are\n"+str(points_dict.items())
                                   self.broadcast(point_msg)
                            
                            
                            
                            last="End of round,press a key and enter to continue: "
                            last1="Wait for the next round to start, don't press any key. "
                            for z in userfdmap:
                                zi = z.partition(" ")
                               
                                if zi[2] == str(self.socket.fileno()):
                                    masterfd = int(zi[2])
                                    username=zi[0]
                                    
                                    lock.acquire()
                                    sendqueues[masterfd].put(last1)
                                    lock.release()
                                    
                                if zi[2] not in str(self.socket.fileno()) :
                                    masterfd = int(zi[2])
                                    lock.acquire()
                                    sendqueues[masterfd].put(last)
                                    lock.release()
                            round+=1
                        
                        else:
                            here="Wrong answer entered!!!\n.The answer enter by the player is " +str(answer.lower())+".\n The right answer is "+str(question[1])+".\n"
                            self.broadcast(here)
                            for z in userfdmap:
                                zi = z.partition(" ")
                               
                                if zi[2] == str(self.socket.fileno()):
                                   
                                    username=zi[0]
                                    points_dict[username]+=0
                                    point_msg="Scores after this round are\n"+str(points_dict.items())
                                    self.broadcast(point_msg)
                            checker1=0
                            last="End of round, enter a key to continue: "
                            last1="Wait for the next round to start, don't press any key. "
                            #self.broadcast(point_msg)
                            for z in userfdmap:
                                zi = z.partition(" ")
                                
                                if zi[2] == str(self.socket.fileno()):
                                    masterfd = int(zi[2])
                                    
                                    #time.sleep(5)
                                    lock.acquire()
                                    sendqueues[masterfd].put(last1)
                                    lock.release()
                                    
                                if zi[2] not in str(self.socket.fileno()) :
                                    masterfd = int(zi[2])
                                    lock.acquire()
                                    sendqueues[masterfd].put(last)
                                    lock.release()
                                
                            
                            round+=1

                    elif key == 1:
                          #print "next round"
                          
                          msgnew = "New Round"
                          self.broadcast(msgnew) 
                           
                    # todo: put a barrier and check
                    #print round
                    print "scores of the round are"
                    print points_dict.items()
                    bar_list[round].wait()
                    checker=0
                    key=0
                    
                winner=max(points_dict.iteritems(), key=operator.itemgetter(1))
                win_msg="The Game is over!\n Thank You For Playing\n The winner of the game is:"+str(winner)
               
                self.socket.send(win_msg)
                j.wait()
                time.sleep(1)
                #self.socket.close()
                sys.exit()
                
        
    def getData(self,userdata):
        global COLLECT_SUBSCRIPTIONS
        global GAME_IN_PROGRESS
        #print max_users,"Max users val is" from self.socket.fileno()
        if max_users > 0 | COLLECT_SUBSCRIPTIONS == 1:
            message = "Waiting for users to join."
            # self.socket.send(message)
        elif max_users == 0:
            print ("All players have joined. ")
            message_players = "The Players are : \n"
            for z in userfdmap:
                zi = z.partition(" ")
                message_players = message_players + str(zi[0]) +"\n"
            message_players = message_players + "The categories are : Politics, Science and Computer.\n Each category has 2 questions.\n 5 points obtained per right answer.\n"
            self.broadcast(SM_NEW_GAME)
            self.broadcast(message_players)
            
            COLLECT_SUBSCRIPTIONS = 0
            GAME_IN_PROGRESS = 1
            self.selectMaster()

        return 1
        

    
    def selectMaster(self):
        global START_ROUND
        global masterName
        global masterfd 
        masterfd = ''
        count = random.randint(0,(len(curusers)-1))
       
        i = 0
        messageMaster = ''
       
        for z in userfdmap:
            if i == count:
                zi = z.partition(" ")
                masterName = zi[0]
                masterfd = int(zi[2])
                lock.acquire()
                sendqueues[masterfd].put("You are the Game Master !!!\n")
                lock.release()
                messageMaster = masterName + " is the Game Master."
                game_msg="Wait till the game master chooses the category"
                print messageMaster
                self.broadcast(messageMaster)
                self.broadcast(game_msg)
                time.sleep(1)
                self.chooseCat(masterfd)
            i = i + 1
        if START_ROUND == 1:
            self.startRound()
        return 1   
    
    def chooseCat(self, mastervalue):
        global categories
        global cat1
        global cat
        print "category loop enter"
        categoryMessage = "To start the round \n Choose one of the category: 1. Politics  2. Science  3. Computer "
        catMes = ''
        for players in curuser_conn:
            if players.fileno() == mastervalue:
               
                
                while (True):
                    players.send(categoryMessage)
                    
                    cat = players.recv(BUFFER_SIZE)
                   
                    print cat
                    if (cat == '1'):
                        break
                    elif (cat == '2'):
                        break
                    elif (cat == '3'):
                        break
               
        catMes = "The category choosen was "+ str(categories[int(cat)-1])
        self.broadcast("ROUND BEGINS")
        self.broadcast(catMes) 
        self.questions(cat) 
        return 1
                #time.sleep(2)

    

    def questions(self, catNumber):
        global dummy
        global dummy2
        global dummy3
        global checker
        global question 
        global cat1
        global masterfd
        catMessage = str(categories[int(catNumber) - 1]) + "doesnot have anymore questions!!"
        if (catNumber == "1"):
            if (dummy == 0):
                question=ques_dict[1][0]
                dummy+=1
                self.broadcast(question[0])
            elif( dummy==1):
                question=ques_dict[1][1]
                dummy+=1
                self.broadcast(question[0])
            else :
                cat1 = 1
                self.broadcast(catMessage)
                time.sleep(0.5)
                self.chooseCat(masterfd)
                return
        
            
        elif(catNumber=="2"):
            if(dummy2==0):
                question=ques_dict[2][0]
                dummy2+=1
                self.broadcast(question[0])
            elif(dummy2==1):
                question=ques_dict[2][1]
                dummy2+=1
                self.broadcast(question[0])
            else : 
                cat1 = 2
                self.broadcast(catMessage)
                time.sleep(0.5)
                self.chooseCat(masterfd)
                return

    
        elif(catNumber=="3"):
            if(dummy3==0):
                question=ques_dict[3][0]
                dummy3+=1
                self.broadcast(question[0])
            elif(dummy3==1):
                question=ques_dict[3][1]
                dummy3+=1
                self.broadcast(question[0])
            else: 
                cat1 = 3
                self.broadcast(catMessage)
                time.sleep(0.5)
                self.chooseCat(masterfd)
                return

        time.sleep(0.2)
        event.set()
        
        return 1
       

  ##Should use this while handling exiting before game starts
    def remove(self,socketData):
        global COLLECT_SUBSCRIPTIONS
        global max_users
        message_exit="you are exiting the game"
        self.socket.send(message_exit)
        # self.socket.close()
        lock.acquire()    
        curusers.remove(socketData) 
        lock.release()       
        print (socketData+" logged off")
        max_users = max_users + 1
        COLLECT_SUBSCRIPTIONS = 1
        sys.exit()

    def broadcast(self, message):
        
        lock.acquire()
        for clients in sendqueues.values():
                clients.put(message)
                time.sleep(0.75)
        lock.release()
       # return 1
        #time.sleep(2)
        #print ("Game Started")

class ClientThreadread(Thread):

    
    def __init__(self,sock):
        Thread.__init__(self)
        self.sock = sock
        
       
    def run(self):
         global trial
         global RINGING
         global thread2_run
        
         chec=0
         i = 0
        
         while True:
             #print thread2_run
             if thread2_run == 1:
                 
                 tcpsock2.listen(1)
                 (conn2, addr) = tcpsock2.accept()   #the previous broadcast(this) connection is not closed, should close it properly to make the exiting beofre game starts to work
                 
                 thread2_run=0
                 chec=1
                 break
             elif CM_SUBSCRIBE=="logout":
                 print"thread2 closing"
                 #self.sock.close()
                 break
         if chec==1:
             
             while True:
                 for p in userfdmap:           #userfdmap contains mapping between usernames and their socket's file despcriptor which we use as index to access their respective queue
                     if str(self.sock.fileno()) in p:
                         connectionpresent = 1
                     else:
                         connectionpresent = 0         
                     
                 try:
                     chat = sendqueues[self.sock.fileno()].get(False)
                 #print chat
                     conn2.send(chat) 
                
                 except Queue.Empty:
                     chat = "none" 
                     time.sleep(2)
                 except KeyError, e:
                     continue
                     
             #elif CM_SUBSCRIBE=="logout":
              #   print"thread2 closing"
               #  self.sock.close()
                    

TCP_IP = '0.0.0.0'
TCP_PORT = int(sys.argv[1])
TCP_PORT2 = 8816
BUFFER_SIZE = 1024  
TIME_OUT = 1800000

global conn
global thread2_run
thread2_run=0
thread1=0

curr_users=0 #

curusers = []
curuser_conn = []  #connected clients 
offlineusers = []
blockusers = []
userlog = {}
userfdmap = [] # maps clients to ports


#get initial connection 
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#host = socket.gethostname()
tcpsock.bind(('', TCP_PORT))


tcpsock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock2.bind(('', TCP_PORT2))

while True:
    
    if max_users != 0:
        tcpsock.listen(6)
        print "Waiting for players... "
        (conn, (ip,port)) = tcpsock.accept()
        CM_SUBSCRIBE=''
        #tcpsock.send(CM_SUBSCRIBE)
        
        if max_users == 0:
            COLLECT_SUBSCRIPTIONS = 0
        q = Queue.Queue()
        lock.acquire()
        curuser_conn.append(conn)
        userlog[conn.fileno()] = conn
        sendqueues[conn.fileno()] = q
        max_users = max_users - 1
        lock.release()
        newthread = ClientThread(conn,ip,port)
        newthread.daemon = True
        newthread.start()
        thread1=1
        
        newthread2 = ClientThreadread(conn)
        newthread2.daemon = True
        newthread2.start()

        threads.append(newthread)
        threads.append(newthread2)


for t in threads:
    t.join()