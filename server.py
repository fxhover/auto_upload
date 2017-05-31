#!/usr/bin/env python
#encoding=utf-8

'''
自动同步上传server端
'''

#接收到文件，将文件按路径写入
from optparse import OptionParser
import SocketServer, time  
import os
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')
try:
    import cjson
except:
    import json
  
class MyServer(SocketServer.BaseRequestHandler):    
  
    def handle(self):   
        print 'Connected from', self.client_address   
        
        
        while True: 
            try:
                data = self.request.recv(1000000)
                if data == 'Hi, server':
                    self.request.sendall('hi, client')
                else:
                    data = json.loads(data)
                    #print 'data:', data 
                    if not data['file']:
                        self.request.sendall('file empty, break')
                        continue
                    filename = os.path.join(PATH, data['file'])
                    if data['type'] == 'created':
                        if data['is_dir']:
                            print 'created', filename
                            os.mkdir(filename)
                            self.request.sendall("dir %s created." % data['file'])
                        else:
                            with open(filename, 'wb') as f :
                                f.write(data['content'])
                            self.request.sendall("file %s writed." % data['file'])
                    elif data['type'] == 'modified':
                        if data['is_dir']:
                            self.request.sendall("dir %s modified." % data['file'])
                        else:
                            with open(filename, 'wb') as f :
                                f.write(data['content'])
                            self.request.sendall("file %s writed." % data['file'])
                    elif data['type'] == 'deleted': 
                        if data['is_dir']:
                            os.rmdir(filename)
                        else:
                            os.remove(filename)
                        self.request.sendall("file %s deleted." % data['file'])
                    elif data['type'] == 'moved':
                        os.rename(data['file'], data['new_file'])
                        self.request.sendall("file %s moved." % data['file'])
                    else:
                        self.request.sendall("hello world")

            except KeyboardInterrupt:
                sys.exit(0)
            except Exception, e:
                print 'server exception: %s' % str(e)
        
        self.request.close()  

        '''   
        while True:   
            receivedData = self.request.recv(8192)   
            if not receivedData:   
                continue  
               
            elif receivedData == 'Hi, server':   
                self.request.sendall('hi, client')   
                   
            elif receivedData.startswith('name'):   
                self.clientName = receivedData.split(':')[-1]   
                if MyServer.userInfo.has_key(self.clientName):   
                    self.request.sendall('valid')   
                else:   
                    self.request.sendall('invalid')   
                       
            elif receivedData.startswith('pwd'):   
                self.clientPwd = receivedData.split(':')[-1]   
                if self.clientPwd == MyServer.userInfo[self.clientName]:   
                    self.request.sendall('valid')   
                    time.sleep(5)   
  
                    sfile = open('PyNet.pdf', 'rb')   
                    while True:   
                        data = sfile.read(1024)   
                        if not data:   
                            break  
                        while len(data) > 0:   
                            intSent = self.request.send(data)   
                            data = data[intSent:]   
  
                    time.sleep(3)   
                    self.request.sendall('EOF')   
                else:   
                    self.request.sendall('invalid')   
                       
            elif receivedData == 'bye':   
                break  
        self.request.close()   
           
        print 'Disconnected from', self.client_address   
        '''
  
if __name__ == '__main__':   
    opt = OptionParser()
    opt.add_option('-d', '--path', dest='path', type='str', help='directory path')
    opt.add_option('-a', '--address', dest='address', type='str', help='server listen addr')
    opt.add_option('-p', '--port', dest='port', type='int', help='server listen port')
    options, args = opt.parse_args()
    path = options.path 
    address = options.address 
    port = options.port 
    if not path:
        path = '.'
    PATH = path 
    if not address:
        address = '0.0.0.0'
    if not port:
        port = 8000
    print 'Server is started/nwaiting for connection.../n'   
    srv = SocketServer.ThreadingTCPServer((address, port), MyServer)   
    srv.serve_forever()    



