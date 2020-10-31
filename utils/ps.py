import sys
from base64 import b64encode,b64decode

def encode(data):
    if isinstance(data, bytes):
        data = data.decode()
    return b64encode(data.encode('UTF-16LE')).decode()

def decode(data):
    return b64decode(data).decode('UTF-16LE')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print ("Usage: python3 ps.py enc <Command.txt>")
        print ("Usage: python3 ps.py dec <encodedCommand>")
        testCommand = b'Console.WriteLine("hello world");'
        print('plain:\n\t%s' % testCommand)
        print('base64:\n\t%s' % encode(testCommand))
        print('recovered-plain:\n\t%s' % decode(encode(testCommand)))
        sys.exit(-1)

    if sys.argv[1] == 'enc':
        command = open(sys.argv[2], 'r').read()
        print(encode(command))
    elif sys.argv[1] == 'dec':
        encodedCommand = sys.argv[2]
        print(decode(encodedCommand))
