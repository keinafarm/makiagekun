##################################################
#
#   MOTOR制御クラス
#
#   モータのON/OFF、巻取り方向、状態表示LED制御、モータ状態の通知を行う
#
#
##################################################

from gpiozero import LED
from Parameter import PGet
from ThreadBase import ThreadBase
from Timer import Timer
from Switch import SwitchController
import time
import datetime


class MotorController:
    class StopControl(ThreadBase):
        """
        停止制御
        """

        def __init__(self, timer, done):
            """
            停止制御
            :param timer: 停止確認時間
            :param done: 停止確認コールバック
            """
            super().__init__()
            self.done = done
            self.timer = timer
            super().start(self.stop_timer)  # スレッド起動

        def stop_timer(self):
            time.sleep(self.timer)
            self.done()

    def __init__(self, status_callback, error_callback):
        """
        モータ制御クラス
        :param status_callback: 状態通知コールバック
        :param error_callback: エラー発生時のコールバック
        """
        self.motor_control = LED(PGet().port_motorOn)
        self.motor_direction = LED(PGet().port_motorDir)
        self.status_callback = status_callback
        self.error_callback = error_callback
        self.status_led_port = LED(PGet().port_status2)
        self.request_status = None  # 保留中の指示
        self.stop_timer = None  # 完全停止待ちタイマー
        self.switch_on_sense_timer = Timer()
        self.switch_off_sense_timer = Timer()
        self.upper_switch = SwitchController.upper_sw()
        self.lower_switch = SwitchController.lower_sw()
        self.upper_switch.set_callback(self.switch_event_upper)
        self.lower_switch.set_callback(self.switch_event_lower)

        self.motor_control.off()
        self.motor_direction.off()

        self.status = {"motorOn": False, "motorDir": False, "pending": False}

    def on(self, direction):
        """
        モータをONにする
        :param direction: 方向(True=上向き False=下向き)
        :return:
        """

        # 完全に停止していない時は指示を保留にする
        if self.stop_timer is not None:  # 完全停止待ち中
            self.request_status = {"motorOn": True, "motorDir": direction}
            return

        self.request_status = None
        # モータの方向をセットして駆動
        if direction:
            if self.upper_switch.state():       # 上端に達していたら受け付けない
                print("これ以上上げられません")
                return
            if self.lower_switch.state():       # 下端に達していたらモーターを動かした後OFFになるのを監視する
                print("Start lower off timer")
                self.switch_off_sense_timer.start(PGet().timer_motor_off_sense, self.switch_sense_timeout)

            self.motor_direction.on()
        else:
            if self.lower_switch.state():       # 下端に達していたら受け付けない
                print("これ以上下げられません")
                return
            if self.upper_switch.state():       # 上端に達していたらモーターを動かした後OFFになるのを監視する
                print("Start upper off timer")
                self.switch_off_sense_timer.start(PGet().timer_motor_off_sense, self.switch_sense_timeout)
            self.motor_direction.off()

        self.motor_control.on()
        # 監視タイマー開始
        self.switch_on_sense_timer.start(PGet().timer_motor_on_sense, self.switch_sense_timeout)

        # ステータスLED点滅開始
        self.status_led_port.blink(PGet().timer_status_led_blink, PGet().timer_status_led_blink)

        # 内部状態:Motor 駆動中
        self.status["motorOn"] = True
        self.status["motorDir"] = direction

        # 状態通知
        self.status_callback(self.status)

    def switch_sense_timeout(self):
        """
        時間になっても、スイッチが入らなかった
        もしくは、時間になってもスイッチが切れなかった
        :return:
        """
        self.off()
        self.error_callback()

    def switch_event_upper(self, state, port_no):
        if state:
            print("Upper SW ON{0}".format(port_no))
            if self.status["motorDir"] is True:
                self.switch_on_sense_timer.stop()
                self.off()  # switchによる停止

        else:
            self.switch_off_sense_timer.stop()
            print("Upper SW OFF")
            return

    def switch_event_lower(self, state, port_no):
        if state:
            print("LOWER SW ON{0}".format(port_no))
            if self.status["motorDir"] is False:
                self.switch_on_sense_timer.stop()
                self.off()  # switchによる停止

        else:
            self.switch_off_sense_timer.stop()
            print("LOWER SW OFF")
            return

    def off(self):
        # 完全に停止していない時は無視する
        if self.stop_timer is not None:  # 完全停止待ち中
            return

        # モーター駆動停止
        self.motor_direction.off()
        self.motor_control.off()
        self.switch_on_sense_timer.stop()  # 監視タイマー停止

        # ステータスLED消灯
        self.status_led_port.off()

        # 内部状態:Motor 停止中
        self.status["motorOn"] = False
        self.status["motorDir"] = False
        # 状態通知
        self.status_callback(self.status)

        # 完全停止待ち
        self.status["pending"] = True
        self.stop_timer = self.StopControl(PGet().timer_stop_control, self.complete)

    def complete(self):
        """
        停止確認処理
        :return:
        """
        self.stop_timer = None
        self.status["pending"] = False
        if self.request_status is not None:
            self.on(self.request_status["motorDir"])


if __name__ == "__main__":
    import json


    def callback(msg):
        json_data = json.dumps(msg)
        print("{0}:STATUS:{1}".format(datetime.datetime.now(), json_data))


    def error_process():
        print("{0}:ERROR".format(datetime.datetime.now()))


    obj = MotorController(callback, error_process)
    print("{0}:UP ON".format(datetime.datetime.now()))
    obj.on(True)
    time.sleep(5)
    print("{0}STOP".format(datetime.datetime.now()))

    obj.off()
    time.sleep(2)
    print("{0}:DOWN ON".format(datetime.datetime.now()))

    obj.on(False)
    time.sleep(3)
    print("{0}STOP".format(datetime.datetime.now()))

    obj.off()
    print("{0}:UP ON".format(datetime.datetime.now()))

    obj.on(True)
    print("{0}:DOWN ON".format(datetime.datetime.now()))

    obj.on(False)
    print("{0}:UP ON".format(datetime.datetime.now()))

    obj.on(True)
    print("{0}:DOWN ON".format(datetime.datetime.now()))

    obj.on(False)
    print("{0}:UP ON".format(datetime.datetime.now()))

    obj.on(True)
    print("{0}:DOWN ON".format(datetime.datetime.now()))

    obj.on(False)
    time.sleep(4)
    print("{0}STOP".format(datetime.datetime.now()))

    obj.off()
    print("{0}:UP ON".format(datetime.datetime.now()))

    time.sleep(3)

    obj.on(True)
    time.sleep(5)
    print("====== Press Upper Switch")
    time.sleep(6)

    print("{0}:DOWN ON".format(datetime.datetime.now()))

    obj.on(False)
    time.sleep(5)
    print("====== Press Lower Switch")
    time.sleep(6)

    print("{0}:UP ON".format(datetime.datetime.now()))

    obj.on(True)
    time.sleep(10)
    print("====== Error?")
