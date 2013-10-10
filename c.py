from time import sleep
from socket import *
import sys
import os 
import ctypes
import time
import platform
import _winreg
import pickle
import math

serverHost='localhost'
serverPort=81
sock=socket()
sock.connect((serverHost,serverPort))

key = _winreg.OpenKey(
    _winreg.HKEY_LOCAL_MACHINE,
    r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")

value, type = _winreg.QueryValueEx(key, "~MHz")
Speed=float(value)/float(1000)
print 'Processor speed is:', Speed, 'GHz'

def sys1():
 return platform.system()
 
Operating_System=str(sys1())

def sys2():
 return platform.node()
 
computer_network=str(sys2())


def sys3():
 return platform.machine()
 
platform_machine=str(sys3())

def sys4():
 return platform.processor()
 
platform_processor=str(sys4())

print "Operating System: ",Operating_System
print "Computer Name: ",computer_network
print "Machine: ",platform_machine
print "Processor: ",platform_processor

class SysInfo:

    def __init__(self):

        self.totalRam, self.availRam = self.ram()
        self.totalRam = self.totalRam / (1048576)
        self.availRam = self.availRam / (1048576)



    def ram(self):
      try:
        kernel32 = ctypes.windll.kernel32
        c_ulong = ctypes.c_ulong
        class MEMORYSTATUS(ctypes.Structure):
            _fields_ = [
                ('dwLength', c_ulong),
                ('dwMemoryLoad', c_ulong),
                ('dwTotalPhys', c_ulong),
                ('dwAvailPhys', c_ulong),
                ('dwTotalPageFile', c_ulong),
                ('dwAvailPageFile', c_ulong),
                ('dwTotalVirtual', c_ulong),
                ('dwAvailVirtual', c_ulong)
            ]

        memoryStatus = MEMORYSTATUS()
        memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUS)
        kernel32.GlobalMemoryStatus(ctypes.byref(memoryStatus))
        return (memoryStatus.dwTotalPhys, memoryStatus.dwAvailPhys)
      except:
        print "No ram found"



    def get_free_space(self,folder, format="MB"):
      """
            Return folder/drive free space
      """
      try:
        fConstants = {"GB": 1073741824,
                      "MB": 1048576,
                      "KB": 1024,
                      "B": 1
                      }
        if platform.system() == 'Windows':
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
            #return (int(free_bytes.value/fConstants[format.upper()]), format)
            return (int(free_bytes.value/1048576), format)
        else:
            return (int(os.statvfs(folder).f_bfree*os.statvfs(folder).f_bsize/fConstants[format.upper()]), format)
      except:
        print "No hard disk found"

def test_speed():
    for x in range(0, 3000):
        v=0
		#print "We're on time %d" % (x)	
		
def get_cpu_load():
    """ Returns a list CPU Loads"""
    result = []
    cmd = "WMIC CPU GET LoadPercentage "
    response = os.popen(cmd + ' 2>&1','r').read().strip().split("\r\n")
    for load in response[1:]:
       result.append(int(load))
    return result[0]



#cpuusage=str(get_cpu_load())
#print cpuusage
 

def server_send(msg):
 sock.send(msg)

 
sys = SysInfo()
print "System Memory : %dMb total" % sys.totalRam
print "Available System Memory  : %dMb free" % sys.availRam
#sock.send(b"Hello")

space,size =  sys.get_free_space("C:", "MB")
space1,size1 =  sys.get_free_space("D:", "MB")

print "Free Space in C:",space,"MB"
print "Free Space in D:",space1,"MB"

start_time = time.clock()
test_speed()
final_time = (time.clock() - start_time)/1000
final_time=math.ceil(final_time*100)/100
print final_time, "ms"
var = raw_input("Press any key to exit: ")
#print "you entered ", var
var=[]

var.insert(0,"initial")
var.insert(1,str(Speed))
var.insert(2,str(Operating_System))
var.insert(3,str(computer_network))
var.insert(4,str(platform_machine))
var.insert(5,str(platform_processor))
var.insert(6,str(sys.totalRam))
var.insert(7,str(sys.availRam))
var.insert(8,str(space))
var.insert(9,str(space1))
var.insert(10,str(final_time))

server_send(pickle.dumps(var))

#data=sock.recv(1024)
#print('Client received:',repr(data))

def performance_client():
    global space,space1
    for x in range(0,1000):
         sleep(1)
         current_sys1=SysInfo()
         cur_space,cur_size =  current_sys1.get_free_space("C:", "MB")
         cur_space1,cur_size1 =  current_sys1.get_free_space("D:", "MB")
         if(current_sys1.availRam!=sys.availRam):
            print "Updated Available System Memory : %dMB free" % current_sys1.availRam
            sys.availRam=current_sys1.availRam
            var1=[]
            var1.insert(0,"updated")
            var1.insert(1,str(sys.availRam))
            server_send(pickle.dumps(var1))
         if(cur_space!=space):	
            print "Updated Free Space : %dMB free" % cur_space
            space=cur_space
            var2=[]
            var2.insert(0,"updated1")
            var2.insert(1,str(cur_space))
            server_send(pickle.dumps(var2))
         if(cur_space1!=space1):	
            print "Updated Free Space : %dMB free" % cur_space1
            space1=cur_space1
            var3=[]
            var3.insert(0,"updated2")
            var3.insert(1,str(cur_space1))
            server_send(pickle.dumps(var3))	


 
    sock.close()
performance_client()
