import argparse
import websocket

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", required=False, help="Websocket URL")
    return parser.parse_args()

if __name__ == '__main__':
    args=  parse_args()
    if args.url is None:
        ws = websocket.create_connection("ws://echo.websocket.org/")
        print("Sending 'Hello, World'...")
        ws.send("Hello, World")
        print("Sent")
        print("Receiving...")
        result =  ws.recv()
        print("Received '%s'" % result)
        ws.close()
