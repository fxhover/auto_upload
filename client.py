#!/usr/bin/env python
#encoding=utf-8

'''
自动同步上传文件client端
'''

#监听指定目录，发现文件有修改或者有新文件，自动将文件上传到server

"""
A simple directory watching script that will compute the checksum for all files
within a path and execute a change when the sum changes.
This will not work well with large files as it reads the entire file into
memory.
"""
import time  
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8')
import os, socket 
import struct
from optparse import OptionParser
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler #,  RegexMatchingEventHandler, FileSystemEventHandler
try:
    import cjson as json
except:
    import json 
  
class MyClient:   
  
    def __init__(self, server_host, server_port):   
        self.server_host = server_host
        self.server_port = server_port
        self.sock = None
        print 'Prepare for connecting...'   
        self.connect()
  
    def connect(self):   
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        self.sock.connect((self.server_host, self.server_port))   
        self.transfer('Hi, server')

        '''
        sock.sendall('Hi, server')   
        self.response = sock.recv(8192)   
        print 'Server:', self.response   
  
        self.s = raw_input("Server: Do you want get the 'thinking in python' file?(y/n):")   
        if self.s == 'y':   
            while True:   
                self.name = raw_input('Server: input our name:')   
                sock.sendall('name:' + self.name.strip())   
                self.response = sock.recv(8192)   
                if self.response == 'valid':   
                    break  
                else:   
                    print 'Server: Invalid username'   
  
            while True:   
                self.pwd = raw_input('Server: input our password:')   
                sock.sendall('pwd:' + self.pwd.strip())   
                self.response = sock.recv(8192)   
                if self.response == 'valid':   
                    print 'please wait...'   
  
                    f = open('b.pdf', 'wb')   
                    while True:   
                        data = sock.recv(1024)   
                        if data == 'EOF':   
                            break  
                        f.write(data)   
                           
                    f.flush()   
                    f.close()   
  
                    print 'download finished'   
                    break  
                else:   
                    print 'Server: Invalid password'   
                   
  
        sock.sendall('bye')   
        sock.close()   
        print 'Disconnected'  
        ''' 
    def transfer(self, data):
        msg = struct.pack('>I', len(data)) + data
        self.sock.sendall(msg)
        response = self.sock.recv(8192)
        print 'server reponse: ', response

    def close(self):
        self.sock.close()


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.py", "*.lxml", "*.txt", ".*"]

    def __init__(self, watch_dir, client):
        self.watch_dir = watch_dir
        self.client = client 
        super(MyHandler, self).__init__()

    def process(self, event):  
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        try:
            data = {}
            data['file'] = event.src_path[len(self.watch_dir):]
            data['is_dir'] = event.is_directory
            data['type'] = event.event_type
            data['content'] = None
            data['new_file'] = None 
            if event.event_type == 'moved':
                data['new_file'] = event.key[2][len(self.watch_dir):]
            if event.event_type in ['modified', 'created']:
                if not event.is_directory:
                    with open(event.src_path, 'rb') as f:
                        data['content'] = f.read()
            #print data 
            data = json.dumps(data)
            self.client.transfer(data)
        except Exception, e:
            print 'client exception: %s' % str(e)
            #self.client.close()

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def on_moved(self, event):
        self.process(event) 

    def on_deleted(self, event):
        self.process(event)

    #def on_any_event(self, event):
    #    self.process(event)


if __name__ == '__main__':
    opt = OptionParser()
    opt.add_option('-d', '--path', dest='watch_dir', type='str', help='watch directory')
    opt.add_option('-s', '--server', dest='server_host', type='str', help='the server host')
    opt.add_option('-p', '--port', dest='server_port', type='int', help='the server port')
    options, args = opt.parse_args()
    watch_dir = options.watch_dir
    server_host = options.server_host
    server_port = options.server_port 
    if not watch_dir:
        watch_dir = os.path.abspath(os.curdir)
    if not server_host:
        server_host = '127.0.0.1'
    if not server_port: 
        server_port = 8000
    print "watch directory: %s, server_host: %s, server_port: %s" % (watch_dir, server_host, server_port)

    #args = sys.argv[1:]
    observer = Observer()
    #observer.schedule(MyHandler(), path=args[0] if args else '.')
    client = MyClient(server_host, server_port)
    observer.schedule(MyHandler(watch_dir, client), path=watch_dir, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        client.close()

    observer.join()

