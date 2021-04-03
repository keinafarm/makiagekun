# https://docs.python.org/ja/3/library/threading.html

import time
import threading
import inspect

locked_object = None


class ThreadBase:
    threading_lock = None

    @classmethod
    def lock_init(cls):
        if ThreadBase.threading_lock is None:
            ThreadBase.threading_lock = threading.Lock()

    @classmethod
    def lock(cls):
        global locked_object
        ThreadBase.threading_lock.acquire()
        locked_object = inspect.stack()[1].filename + " : "+ inspect.stack()[1].function

    @classmethod
    def unlock(cls):
        ThreadBase.threading_lock.release()

    def __init__(self):
        ThreadBase.lock_init()
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


if __name__ == "__main__":
    class udon(ThreadBase):
        def __init__(self):
            super(udon, self).__init__()
            self.flag = False

        def start(self):
            self.flag = True
            super().start(self.procUdon)

        def procUdon(self):
            while self.flag:
                print('  うどんを茹でます。')
                time.sleep(1)
                print('  うどんが茹であがりました。')

        def stop(self):
            self.flag = False
            print("うどんゆでるのやめます")


    class tuyu(ThreadBase):
        pass


    def tuyu_end():
        print("つゆが出来あがりました")


    def procTuyu():
        print('  ツユをつくります。')
        time.sleep(2)
        print('  ツユができました。')


    print('うどんを作ります。')
    obj1 = udon()
    obj2 = tuyu()
    print("process 1")
    obj1.start()
    print("process 2")
    obj2.start(procTuyu, tuyu_end)
    print("process 3")

    time.sleep(4)
    obj1.stop()
    obj1.wait_end()
    print("process 4")
    obj2.wait_end()
    print("process 5")
    print('盛り付けます。')
    print('うどんができました。')

    obj1.start()
    print("process 6")
    time.sleep(4)
    print("process 7")
    obj1.stop()
    print("process 8")
    obj1.wait_end()
    print("process 9")
