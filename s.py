from socket import *
#import numpy as np
#import matplotlib.pyplot as plt
import pickle
import json
from file_sharing_server import run as run_sharingserver

import thread

myHost='0.0.0.0'
myPort=81
sock=socket()
sock.bind((myHost,myPort))
sock.listen(5)
br = []

global_data = []

def savetofile(username,index):
    global global_data
    f=open("bharat.txt",'rb')
    br=global_data[index]
    print br
    fjson=json.loads(f.read())
    f.close()
    if username in fjson:
        fjson[username].extend(br)
    else:
        fjson[username]=br

    fdata=json.dumps(fjson)
    f=open("bharat.txt",'w')
    f.write(fdata)
    f.close()
    

"""def plot(param):
    data = []
    for i in range(0, len(param)):
        data.append((10*i, int(param[i])))
    #print data
    N = len( data )
    x = np.arange(1, N+1)
    y = [ num for (s, num) in data ]
    labels = [ s for (s, num) in data ]
    width = 1
    
    #bar1 = plt.bar( x, y, width, color="y" )
    plt.ylabel( 'Updated RAM' )
    plt.xlabel('Time')
    #plt.xticks(x, labels)
    plt.plot(x, y)
    plt.show()"""

def handle_client(conn,index):
    username = ''
    global global_data
    br=global_data[index]
    while True:
        data=conn.recv(1024)
        if len(data) != 0:
            data=pickle.loads(data)
            print('Receiving data from: ',address[0])
            if(data[0]=="initial"):
              print("Processor Speed is: "+data[1])
              print("Operating System: "+data[2])
              print("Computer Name: "+data[3])
              print("Machine: "+data[4])
              print("Processor: "+data[5])
              print("System Memory: "+data[6])
              print("Available System Memory: "+data[7]+"MB")
              print("Free Space in C: "+data[8]+"MB")
              print("Free Space in D: "+data[9]+"MB")
              print("Execution Time "+data[10])
              username = data[3]
            elif(data[0]=="updated"):
              print(" Updated RAM: "+data[1]+"MB")
              br.append(data[1])
              
              if len(br) % 2 == 0:
                savetofile(username,index)
                #plot(br)
                
            elif(data[0]=="updated1"):
             print(" Updated Free Space in C: "+data[1]+"MB")
            elif(data[0]=="updated2"):
              print(" Updated Free Space in D: "+data[1]+"MB")		  
            #conn.send(b'Echo=>'+data)
thread.start_new_thread(run_sharingserver,())

while True:
    conn,address=sock.accept()
    print('Server Connected by',address[0])
    ar= []
    global_data.append(ar)
    thread.start_new_thread(handle_client, (conn,len(global_data)-1,))
    

print('Client Closed - ',address)

sock.close()  
