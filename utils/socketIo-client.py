import os
import sys
import time
import json
import queue
import signal
import threading
import websocket
from urllib.parse import urlparse

pingInterval = 1000
backgroundThreads = []
messageQueue = queue.Queue()
pid = os.getpid()
currentWS = None

def send(msg):
    if currentWS is None:
        print('No Active socket')
        return
    wrap = ['msg', msg]
    currentWS.send('42'+json.dumps(wrap))

def ping(cls):
    while True:
        cls.send('2')
        time.sleep(pingInterval / 1000.0)
    print('stop pinging')

def on_open(cls):
    global currentWS
    print('open', cls)
    t = threading.Thread(target=ping, args=(cls,))
    backgroundThreads.append(t)
    t.start()
    currentWS = cls

def on_close(cls):
    print('close', cls)
    os.kill(pid, signal.SIGTERM)

def on_message(cls, message):
    global pingInterval
    if message.startswith('0{'):
        # initial handshake
        config = json.loads(message[1:])
        pingInterval = int(config['pingInterval'])
        print('change interval to %d' % pingInterval)
    elif message == '3':
        pass # ignore pong
    elif message.startswith('42'):
        action, data = json.loads(message[2:])
        #print(action, data)
        messageQueue.put((action, data))

if __name__ == '__main__':

    print('='*10+'\nThis client is compatible with Socket.IO <= 2.3.0\n'+'='*10)
    
    if len(sys.argv) < 2:
        print("Usage: python3 %s ws://<target>" % sys.argv[0])
        exit(0)

    url = sys.argv[1]
    purl = urlparse(url.rstrip('/'))
    url = "%s://%s%%s/" % (purl.scheme, purl.netloc)
    if purl.path == "":
        url %= "/socket.io"
    else:
        url %= purl.path

    url += '?EIO=4&transport=websocket'
    app = websocket.WebSocketApp(url,
        on_open=on_open,
        on_message=on_message,
        on_close=on_close,
        )
    t = threading.Thread(target=app.run_forever, kwargs=dict(sslopt={"check_hostname": False}))
    t.start()
    backgroundThreads.append(t)
    try:
        time.sleep(1.)
        while True:
            c = input("> ").strip()
            send(c)
            (action, response) = messageQueue.get()
            print(response)
    except KeyboardInterrupt:
        os.kill(pid, signal.SIGTERM)
