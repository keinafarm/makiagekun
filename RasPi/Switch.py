##################################################
#
#   Switch制御クラス
#
#   スイッチの監視を行う
#
#
##################################################

from Parameter import PGet
from gpiozero import Button
from ThreadBase import ThreadBase
import time


# https://www.ne.senshu-u.ac.jp/~iida/pc/?p=1562

class SwitchController(ThreadBase):
    upper_sw_obj = None
    lower_sw_obj = None
    @classmethod
    def init(cls):
        cls.upper_sw_obj = SwitchController(PGet().port_upper_sw, None, PGet().timer_chattering)
        cls.lower_sw_obj = SwitchController(PGet().port_lower_sw, None, PGet().timer_chattering)

    @classmethod
    def upper_sw(cls):
        if cls.upper_sw_obj is None:
            SwitchController.init()
        return cls.upper_sw_obj

    @classmethod
    def lower_sw(cls):
        if cls.lower_sw_obj is None:
            SwitchController.init()
        return cls.lower_sw_obj

    def __init__(self, port_no, callback, chattering=1):
        """
        スイッチ監視
        :param port_no: スイッチポート番号
        :param callback: スイッチ状態変化時通知関数
        :param chattering: チャタリング制御時間（この時間内は変化があっても無視される）
        """
        super().__init__()
        self.port = Button(port_no, pull_up=False)
        self.port_no = port_no
        self.callback = callback
        self.flag = True
        self.sampling_time = 0.2  # 200mSecで監視
        self.chattering = chattering / self.sampling_time

        super().start(self.scan_switch)  # スレッド起動

    def set_callback(self, callback):
        self.callback = callback

    def scan_switch(self):
        last_state = self.port.value
        counter = 0
        while self.flag:
            state = self.port.value
            if last_state != state:
                counter += 1
                if counter > self.chattering:
                    if state:
                        self.callback(True, self.port_no)
                    else:
                        self.callback(False, self.port_no)
                    last_state = state
            else:
                counter = 0
            time.sleep(self.sampling_time)

    def stop(self):
        self.flag = False
        self.port.close()

    def state(self):
        return self.port.value

if __name__ == "__main__":
    def switch_state(state, port_no):
        print("Button {1} is {0}".format(state, port_no))


    print("Process Start")
    obj1 = SwitchController.upper_sw()
    obj2 = SwitchController.lower_sw()
    obj1.set_callback( switch_state)
    obj2.set_callback( switch_state)

    count = 100
    while count > 0:
        time.sleep(1)

    print("Process End")
    obj1.stop()
    obj2.stop()
