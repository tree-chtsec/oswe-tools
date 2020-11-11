from __future__ import print_function

import time
try:
    import queue
except ImportError:
    import Queue as queue
import threading
from multiprocessing.pool import ThreadPool

stopSign = False

def run(task, values, thread_num=8, verb=False, max_retries=5):
    global stopSign
    threads = []
    stopSign = False

    valueQueue = queue.Queue()
    for v in values:
        valueQueue.put(v)

    def __inner_func():
        while not stopSign:
            _retry = max_retries
            try:
                arguments = valueQueue.get_nowait()
            except:
                break
            while _retry >= 0:
                try:
                    task(arguments)
                    _retry = -1
                except Exception as e:
                    verb and print(e)
                    verb and print("retrying... %d" % arguments)
                    _retry -= 1
                    time.sleep(0.3)
            valueQueue.task_done()

    for i in range(thread_num):
        t = threading.Thread(target=__inner_func)
        t.daemon = True
        t.start()
        threads.append(t)
    
    while not valueQueue.empty() and not stopSign:
        try:
            time.sleep(0.6)
        except KeyboardInterrupt:
            verb and print('ready to stop...')
            break
    stopSign = True
    verb and print('task done! remaining queue size: %d' % valueQueue.qsize())

    for t in threads:
        t.join()


if __name__ == '__main__':

    import requests
    try:
        print("launch test http server first")
        print("$ python3 -m http.server 3333")
        input("press [enter] to continue...")
    except SyntaxError:
        pass
    fn = lambda x: requests.get("http://localhost:3333/" + str(x))
    run(fn, range(1000), verb=True)
