import argparse
import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", required=False, help="Websocket URL")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    websocket.enableTrace(True)
    url = args.url
    if url is None:
        url = "ws://echo.websocket.org/"
        print("Use default echo server")
    ws = websocket.WebSocketApp(url,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
