import threading
import random
import time

lock = threading.Lock()
COUNTER = 0

def get_lock(thread_number):
    global COUNTER
    r = random.random()
    time.sleep(r)
    with lock:
        COUNTER += 1
        print("lock acquired by thread {} counter = {} r = {}".format(thread_number, COUNTER, r))

thread_list = []
if __name__ == "__main__":
    for i in range(10000):
        thread = threading.Thread(target=get_lock, args=(i,))
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()
