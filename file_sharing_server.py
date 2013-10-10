#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import socket
import pickle
afile=[]
bfile=[]
c=len(bfile)
for subdir, dirs, files in os.walk('c:/xampp/htdocs/file_transfer/'):
  for file in files:
    if(len(afile)<25):
     file_size=os.path.getsize('c:/xampp/htdocs/file_transfer/'+file)
     afile.append(str(file))
     bfile.append(str(file_size))

#s=socket.socket()         # Create a socket object
#host=socket.gethostname() # Get local machine name
#port=12345                # Reserve a port for your service.
#s.bind((host, port))

#s.listen(5)

#while True:
 #c, addr = s.accept() 
 #print "\n".join(afile)
 
 #c.send(pickle.dumps(afile))
 #c.close()

#Create custom HTTPRequestHandler class
class KodeFunHTTPRequestHandler(BaseHTTPRequestHandler):
    
    #handle GET command
    def do_GET(self):
        rootdir = 'c:/xampp/htdocs/file_transfer/' #file location
        try:
         print self.path
         if self.path.endswith('.html') or self.path.endswith('.txt'):
          f = open(rootdir + self.path) #open requested file
          #file_size=os.path.getsize('rootdir + self.path')
          #print file_size
          self.send_response(200)
          self.send_header('Content-type','text-html')
          self.end_headers()
          self.wfile.write(f.read())
          f.close()
          return
         elif self.path.endswith('.jpg') or self.path.endswith('.jpeg') or self.path.endswith('.jpe'):
          f = open(rootdir + self.path,'rb') #open requested file
          self.send_response(200)
          self.send_header('Content-type','image/jpeg')
          self.end_headers()
          self.wfile.write(f.read())
          f.close()
          return
         elif self.path.endswith('.avi'):
          f = open(rootdir + self.path,'rb') #open requested file
          self.send_response(200)
          self.send_header('Content-type','video/x-msvideo')
          self.end_headers()
          self.wfile.write(f.read())
          f.close()
          return
         elif self.path == "list":
          self.send_response(200)
          self.send_header('Content-type','text-html')
          self.end_headers()
          self.wfile.write("\n".join(afile))
          #self.wfile.write("\n".join(bfile))
          return
         elif self.path == "update":
          uafile=""
          for subdir, dirs, files in os.walk('c:/xampp/htdocs/file_transfer/'):
           for file in files: 
             file_size=os.path.getsize('c:/xampp/htdocs/file_transfer/'+file)
             uafile = uafile + str(file) + ";" + str(file_size) + "\n"
          self.send_response(200)
          uafile = uafile.rstrip("\n")
          #print uafile		  
          self.send_header('Content-type','text-html')
          self.end_headers()
          self.wfile.write(uafile)
          return		  
            
        except IOError:
            self.send_error(404, 'file not found')
    
def run():
    print('http server is starting...')

    
    server_address = ('0.0.0.0', 82)
    httpd = HTTPServer(server_address, KodeFunHTTPRequestHandler)
    print('http server is running...')
    httpd.serve_forever()
    
if __name__ == '__main__':
    run()
