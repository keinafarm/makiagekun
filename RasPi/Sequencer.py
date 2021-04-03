##################################################
#
#   Sequence制御クラス
#
##################################################

from MqttThread import MqttThread
from Motor import MotorController
from Parameter import PGet
from Timer import Timer
from Buzzer import BuzzerController
from Camera import CameraController
from Led import LedController
import json
import time
import base64


class Sequencer:
    def __init__(self):
        self.motor = MotorController(self.motor_status, self.motor_error)
        self.control_obj = MqttThread("mqtt_broker/message_ctrl")
        self.control_obj.set_receive_callback(self.order_receive)

        self.mqtt_status = MqttThread("mqtt_broker/status")
        self.mqtt_image = MqttThread("mqtt_broker/image")

        self.mqtt_capture = MqttThread("mqtt_broker/capture")
        self.mqtt_capture.set_receive_callback(self.capture_order)

        self.capture_timer = Timer()
        self.capture_stop_timer = Timer()
        self.capture = False

        self.buzzer = BuzzerController()
        self.camera = CameraController()
        self.led_error = LedController.error()
        self.led_warning = LedController.warning()
        self.led_wakeup = LedController.status1()

        self.status = {"motorOn": False, "motorDir": False, "error": False}
        self.last_status = {"motorOn": False, "motorDir": False, "error": False}

    def order_receive(self, mqtt_msg):
        print("order_receive {0}".format(mqtt_msg))
        msg_json = mqtt_msg.payload.decode("utf-8", "ignore")
        print("msg_json{0}:{1}".format(type(msg_json), msg_json))
        msg = json.loads(msg_json)
        print("msg{0}:{1}".format(type(msg), msg))
        operation = msg["operation"]
        if operation == "UP":
            self.capture = True
            self.capture_stop_timer.stop()
            self.capture_timer.start(PGet().timer_camera_interval, self.capture_loop)
            self.motor.on(True)
        elif operation == "DOWN":
            self.capture = True
            self.capture_stop_timer.stop()
            self.capture_timer.start(PGet().timer_camera_interval, self.capture_loop)
            self.motor.on(False)
        elif operation == "STOP":
            self.motor.off()
        elif operation == "CANCEL":
            self.error_cancel()

    def capture_stop(self):
        self.capture = False
        self.capture_timer.stop()

    def capture_loop(self):
        if self.capture:
            self.capture_order("Status Capture")
            self.capture_timer.start(PGet().timer_camera_interval, self.capture_loop)

    def capture_order(self, msg):
        print("capture_order {0}".format(msg))
        buffer = self.camera.one_shot()
        data = buffer
        base64_data = base64.b64encode(data).decode('utf-8')
        self.mqtt_image.send(base64_data)

    def motor_status(self, msg):
        self.status.update(msg)
        print("motor_status {0}".format(msg))
        self.mqtt_status.send(self.status)

        if self.last_status["motorOn"] == True and self.status["motorOn"] == False:
            # モーター状態がONからOFFに変わったら、キャプチャー終了タイマーを開始する
            self.capture_stop_timer.start(PGet().timer_camera_stop, self.capture_stop)
        self.last_status = self.status.copy()

    def motor_error(self):
        print("motor_error")
        self.status.update({"error": True})
        self.buzzer.on(BuzzerController.PATTERN[0])
        self.led_error.on()
        self.mqtt_status.send(self.status)

    def error_cancel(self):
        print("error_cancel")
        self.buzzer.off()
        self.led_error.off()
        self.status.update({"error": False})
        self.mqtt_status.send(self.status)

    def run(self):
        self.led_wakeup.on()
        print("START SEQUENCE")
        while True:
            print("LOOP")
            time.sleep(3)
        self.led_wakeup.off()


if __name__ == "__main__":
    obj = Sequencer()
    obj.run()
