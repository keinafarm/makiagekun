##################################################
#
#   Parameter管理クラス
#   https://www.magata.net/memo/index.php?python%A4%C7%A5%B7%A5%EA%A5%A2%A5%E9%A5%A4%A5%BA%A4%C8%A5%C7%A5%B7%A5%EA%A5%A2%A5%E9%A5%A4%A5%BA
#
##################################################
import pickle
import os


def PGet():
    return Parameter.Get()


PARAMETER_FILE = 'parameter.prm'


class Parameter:
    class_object = None

    @classmethod
    def Get(cls):
        if Parameter.class_object is None:
            if os.path.exists(PARAMETER_FILE):
                cls.parameter_load()
                return Parameter.class_object
            Parameter.class_object = Parameter()
        return Parameter.class_object

    def __init__(self):
        self.__port_motorOn = 4  # Motor:Motor 駆動ポート
        self.__port_motorDir = 27  # Motor:Motor 方向ポート
        self.__port_status1 = 22  # Sequencer:起動ステータスLEDポート
        self.__port_status2 = 23  # Motor:モータ駆動中LEDポート
        self.__port_error = 24  # Motor:エラーLEDポート
        self.__port_warning = 25  # Sequencer:警告LEDポート
        self.__port_buzzer = 18  # Buzzer:ブザーポート
        self.__port_upper_sw = 5  # Sequencer:上端スイッチ
        self.__port_lower_sw = 6  # Sequencer:下端スイッチ
        self.__timer_status_led_blink = 0.5  # Motor:モータ駆動中LEDの点滅間隔(sec)
        self.__timer_stop_control = 3  # Motor:モーター停止後のインターバル(sec)
        self.__timer_chattering = 1  # Switch:スイッチのチャタ除去時間(sec)
        self.__timer_camera_interval = 2.0  # Sequence:モニター時の撮影間隔(sec)
        self.__timer_camera_stop = 5  # Sequence : モーターがOFFになってからキャプチャーを停止するまでの時間
        self.__timer_motor_on_sense = 100  # Motor:ONにしてからスイッチが入るまでの監視(sec)
        self.__timer_motor_off_sense = 4  # Motor:ONにしてからスイッチが切れるまでの監視(sec)
        self.__camera_resolution = (320, 240)  # カメラの解像度
        self.__mqtt_password = "token:token_3KgDgo0nTlZAPJbO"  # Sequence:Beebote MQTT password

    @property
    def port_motorOn(self):
        return self.__port_motorOn

    @property
    def port_motorDir(self):
        return self.__port_motorDir

    @property
    def port_status1(self):
        return self.__port_status1

    @property
    def port_status2(self):
        return self.__port_status2

    @property
    def port_error(self):
        return self.__port_error

    @property
    def port_warning(self):
        return self.__port_warning

    @property
    def port_buzzer(self):
        return self.__port_buzzer

    @property
    def port_upper_sw(self):
        return self.__port_upper_sw

    @property
    def port_lower_sw(self):
        return self.__port_lower_sw

    @property
    def timer_status_led_blink(self):
        return self.__timer_status_led_blink

    @property
    def timer_stop_control(self):
        return self.__timer_stop_control

    @property
    def timer_chattering(self):
        return self.__timer_chattering

    @property
    def timer_camera_interval(self):
        return self.__timer_camera_interval

    @property
    def timer_camera_stop(self):
        return self.__timer_camera_stop

    @property
    def timer_motor_on_sense(self):
        return self.__timer_motor_on_sense

    @property
    def timer_motor_off_sense(self):
        return self.__timer_motor_off_sense

    @property
    def camera_resolution(self):
        return self.__camera_resolution

    @property
    def mqtt_password(self):
        return self.__mqtt_password

    def parameter_save(self):
        with open(PARAMETER_FILE, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def parameter_load(cls):
        with open(PARAMETER_FILE, "rb") as f:
            Parameter.class_object = pickle.load(f)

    def debug_param_break(self):
        self.__port_motorOn = 0  # Motor:Motor 駆動ポート
        self.__port_motorDir = 1  # Motor:Motor 方向ポート
        self.__port_status1 = 2  # Sequencer:起動ステータスLEDポート
        self.__port_status2 = 3  # Motor:モータ駆動中LEDポート
        self.__port_error = 4  # Motor:エラーLEDポート
        self.__port_warning = 5  # Sequencer:警告LEDポート
        self.__port_buzzer = 6  # Buzzer:ブザーポート
        self.__port_upper_sw = 7  # Sequencer:上端スイッチ
        self.__port_lower_sw = 8  # Sequencer:下端スイッチ
        self.__timer_status_led_blink = 9  # Motor:モータ駆動中LEDの点滅間隔(sec)
        self.__timer_stop_control = 10  # Motor:モーター停止後のインターバル(sec)
        self.__timer_chattering = 11  # Switch:スイッチのチャタ除去時間(sec)
        self.__timer_camera_interval = 12  # Sequence:モニター時の撮影間隔(sec)
        self.__timer_camera_stop = 13  # Sequence : モーターがOFFになってからキャプチャーを停止するまでの時間
        self.__timer_motor_on_sense = 14  # Motor:ONにしてからスイッチが入るまでの監視(sec)
        self.__timer_motor_off_sense = 15  # Motor:ONにしてからスイッチが切れるまでの監視(sec)
        self.__camera_resolution = 16  # カメラの解像度
        self.__mqtt_password = 17  # Sequence:Beebote MQTT password


"""
if __name__ == "__main__":
    print("port_motorOn={0}".format(PGet().port_motorOn))
    print("port_motorDir={0}".format(PGet().port_motorDir))
    print("port_status1={0}".format(PGet().port_status1))
    print("port_status2={0}".format(PGet().port_status2))
    print("port_error={0}".format(PGet().port_error))
    print("port_warning={0}".format(PGet().port_warning))
    print("port_buzzer={0}".format(PGet().port_buzzer))
    print("port_upper_sw={0}".format(PGet().port_upper_sw))
    print("port_lower_sw={0}".format(PGet().port_lower_sw))
    print("timer_status_led_blink={0}".format(PGet().timer_status_led_blink))
    print("timer_stop_control={0}".format(PGet().timer_stop_control))
    print("timer_chattering={0}".format(PGet().timer_chattering))
    print("timer_camera_interval={0}".format(PGet().timer_camera_interval))
    print("timer_camera_stop={0}".format(PGet().timer_camera_stop))
    print("timer_motor_on_sense={0}".format(PGet().timer_motor_on_sense))
    print("timer_motor_off_sense={0}".format(PGet().timer_motor_off_sense))
    print("camera_resolution={0}".format(PGet().camera_resolution))
    print("mqtt_password={0}".format(PGet().mqtt_password))

    PGet().parameter_save()
    PGet().debug_param_break()
    print("BREAK")
    print("port_motorOn={0}".format(PGet().port_motorOn))
    print("port_motorDir={0}".format(PGet().port_motorDir))
    print("port_status1={0}".format(PGet().port_status1))
    print("port_status2={0}".format(PGet().port_status2))
    print("port_error={0}".format(PGet().port_error))
    print("port_warning={0}".format(PGet().port_warning))
    print("port_buzzer={0}".format(PGet().port_buzzer))
    print("port_upper_sw={0}".format(PGet().port_upper_sw))
    print("port_lower_sw={0}".format(PGet().port_lower_sw))
    print("timer_status_led_blink={0}".format(PGet().timer_status_led_blink))
    print("timer_stop_control={0}".format(PGet().timer_stop_control))
    print("timer_chattering={0}".format(PGet().timer_chattering))
    print("timer_camera_interval={0}".format(PGet().timer_camera_interval))
    print("timer_camera_stop={0}".format(PGet().timer_camera_stop))
    print("timer_motor_on_sense={0}".format(PGet().timer_motor_on_sense))
    print("timer_motor_off_sense={0}".format(PGet().timer_motor_off_sense))
    print("camera_resolution={0}".format(PGet().camera_resolution))
    print("mqtt_password={0}".format(PGet().mqtt_password))

    PGet().parameter_load()
    print("RESTORE")
    print("port_motorOn={0}".format(PGet().port_motorOn))
    print("port_motorDir={0}".format(PGet().port_motorDir))
    print("port_status1={0}".format(PGet().port_status1))
    print("port_status2={0}".format(PGet().port_status2))
    print("port_error={0}".format(PGet().port_error))
    print("port_warning={0}".format(PGet().port_warning))
    print("port_buzzer={0}".format(PGet().port_buzzer))
    print("port_upper_sw={0}".format(PGet().port_upper_sw))
    print("port_lower_sw={0}".format(PGet().port_lower_sw))
    print("timer_status_led_blink={0}".format(PGet().timer_status_led_blink))
    print("timer_stop_control={0}".format(PGet().timer_stop_control))
    print("timer_chattering={0}".format(PGet().timer_chattering))
    print("timer_camera_interval={0}".format(PGet().timer_camera_interval))
    print("timer_camera_stop={0}".format(PGet().timer_camera_stop))
    print("timer_motor_on_sense={0}".format(PGet().timer_motor_on_sense))
    print("timer_motor_off_sense={0}".format(PGet().timer_motor_off_sense))
    print("camera_resolution={0}".format(PGet().camera_resolution))
    print("mqtt_password={0}".format(PGet().mqtt_password))
"""
