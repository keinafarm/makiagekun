##################################################
#
#   タイマー制御クラス
#
##################################################

import threading


class Timer:
    class TimerSeed:
        def __init__(self, time_value, callback, seq_no):
            self.seq_no = seq_no
            self.callback = callback

            self.t = threading.Timer(time_value, self.timeout_proc, args=seq_no)
            self.t.start()

        def timeout_proc(self, seq_no):
            self.callback(seq_no)

        def cancel(self):
            self.t.cancel()

    def __init__(self):
        self.seq_no = 0  # タイマー処理用のシーケンス番号
        self.callback = None
        self.seed = None

    def start(self, time_value, callback):
        self.seq_no += 1
        self.callback = callback
        if self.seed is not None:
            self.seed.cancel()
        self.seed = self.TimerSeed(time_value, self.timeout_proc, [self.seq_no])

    def stop(self):
        self.seq_no += 1
        if self.seed is not None:
            self.seed.cancel()
        self.seed = None

    def timeout_proc(self, seq_no):
        if seq_no == self.seq_no:
            self.seq_no += 1
            self.seed = None
            self.callback()


if __name__ == "__main__":
    import time


    class TestTimer(Timer):
        def __init__(self, no):
            super().__init__()
            self.no = no

        def __str__(self):
            text = ("Timer:{0}".format(self.no))
            return text

        def start(self, time_value):
            super(TestTimer, self).start(time_value, self.time_out)

        def time_out(self):
            print("{0} Timer:{1} TimeOut".format(time.time(), self.no))


    obj1 = TestTimer(1)
    obj2 = TestTimer(2)

    print("== obj1 start ==")
    obj1.start(1)
    print("== obj2 start ==")
    obj2.start(2)
    time.sleep(3)
    print("== obj1 start ==")
    obj1.start(3)
    print("== obj2 start ==")
    obj2.start(2)
    time.sleep(1)
    print("== obj1 start ==")
    obj1.start(3)
    print("== obj2 start ==")
    obj2.start(2)
    time.sleep(1)
    print("== obj1 start ==")
    obj1.start(3)
    print("== obj2 start ==")
    obj2.start(2)
    print("== obj2 stop ==")
    obj2.stop()
    time.sleep(4)
    print("== obj1 start ==")
    obj1.start(3)
    print("== obj2 start ==")
    obj2.start(2)
