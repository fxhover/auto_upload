#auto_upload

一个简单的监听本地目录修改，然后同步到服务器的工具

##使用场景

本地目录有修改，将修改自动同步到服务器目录

##安装运行

```
python -r requirements.txt

运行server端：

python server.py [options]

Options:
  -h, --help            show this help message and exit
  -d PATH, --path=PATH  directory path
  -a ADDRESS, --address=ADDRESS    server listen addr
  -p PORT, --port=PORT  server listen port

运行client端：

python client.py [options]

Options:
  -h, --help            show this help message and exit
  -d WATCH_DIR, --path=WATCH_DIR    watch directory
  -s SERVER_HOST, --server=SERVER_HOST    the server host
  -p SERVER_PORT, --port=SERVER_PORT     the server port

```

