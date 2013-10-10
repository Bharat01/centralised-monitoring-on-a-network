#!/usr/bin/env python

import httplib
import sys
import socket
import pickle
import thread
import os.path
cfile=[]
dfile=[]
#from c import performance_client 


#s=socket.socket()         # Create a socket object
#host=socket.gethostname() # Get local machine name
#port=12345

#s.connect((host, port))
#while True:
 #data=s.recv(1024)
 #if not data:
  #break
 #data=pickle.loads(data)
 #print "The available files are:"
 #print "\n".join(data)
 
#s.close() 
"""thread.start_new_thread(performance_client,())"""
#get http server ip
http_server = sys.argv[1]
#create a connection
conn = httplib.HTTPConnection(http_server,82)
conn1 = httplib.HTTPConnection(http_server,82)
while 1:
    cmd = raw_input('input command (ex. GET filename.html): ')
    cmd = cmd.split()
	
    print cmd

    if cmd[0] == 'exit': #tipe exit to end it
        break
    
    #request command to server
    conn.request(cmd[0], cmd[1])

    #get response from server
    rsp = conn.getresponse()
    
    #print server response and data
    #print(rsp.status, rsp.reason)
    data_received = rsp.read()
    if(rsp.status==200):
     #print(data_received)
     #save_path = 'C:/filetransfer/'
     #completeName = os.path.join(save_path, cmd[1]+".html")
     a=cmd[1]
     if(a=="list"):
        print data_received
        #break
     elif(a=="update"):
       #print data_received
       sfiles={}
       cfiles={}
       files_revd_from_server = data_received.split("\n")
       for a in files_revd_from_server:
         a = a.split(";")
         #print a
         sfiles[a[0]] = a[1]
       for subdir, dirs, files in os.walk('c:/xampp/htdocs/minor/files/'):
          for file in files:
             file_size=os.path.getsize('c:/xampp/htdocs/minor/files/'+file)
             cfiles[str(file)] = str(file_size)
       #print sfiles
       #print cfiles
       for c in cfiles:
         if(cfiles[c] != sfiles[c]):
           print c + ' has changed'
           conn1.request('GET', str(c))
           print c + ' has been updated now'
     elif(a.split('.')[1]== 'jpg'):
       target = open('./files/'+cmd[1],'wb')
       target.write(data_received)
       target.close()
     elif(a.split('.')[1]== 'avi'):
       target = open('./files/'+cmd[1],'wb')
       target.write(data_received)
       target.close()
     else:
       target = open('./files/'+cmd[1],'w')
       target.write(data_received)
       target.close()
    else:
      print(rsp.status, rsp.reason)	
	  
    #cmd1 = raw_input('input command (GET Update): ')
    
    #rsp = conn.getresponse()	
    
conn.close()
