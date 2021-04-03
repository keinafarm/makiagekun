import time
import threading


class ThreadBase:
    def __init__(self):
        self.thread = threading.Thread(target=self.onThread)
        self.call_back = None
        self.process = None

    def onThread(self):
        if self.process:
            self.process()
        if self.call_back:
            self.call_back()

    def start(self, process=None, call_back=None):
        self.process = process
        self.call_back = call_back
        self.thread.start()

    def wait_end(self):
        self.thread.join()


class udon(ThreadBase):
    pass


class tuyu(ThreadBase):
    pass


def udon_end():
    print("うどんがゆであがりました")


def tuyu_end():
    print("つゆが出来あがりました")


def procUdon():
    print('  うどんを茹でます。')
    time.sleep(3)
    print('  うどんが茹であがりました。')


def procTuyu():
    print('  ツユをつくります。')
    time.sleep(2)
    print('  ツユができました。')

if __name__ == "__main__":
    print('うどんを作ります。')
    obj1 = udon()
    obj2 = tuyu()
    print("process 1")
    obj1.start(procUdon)
    print("process 2")
    obj2.start(procTuyu, tuyu_end)
    print("process 3")
    obj1.wait_end()
    print("process 4")
    obj2.wait_end()
    print("process 5")
    print('盛り付けます。')
    print('うどんができました。')
