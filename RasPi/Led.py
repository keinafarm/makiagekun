##################################################
#
#   LED制御クラス
#
#   LEDのON/OFF制御を行う
#
#
##################################################

from Parameter import PGet
from gpiozero import LED
import time


class LedController(LED):
    error_obj = None
    warning_obj = None
    status1_obj = None
    @classmethod
    def init(cls):
        cls.error_obj = LedController(PGet().port_error)
        cls.warning_obj = LedController(PGet().port_warning)
        cls.status1_obj = LedController(PGet().port_status1)

    @classmethod
    def error(cls):
        if cls.error_obj is None:
            LedController.init()
        return cls.error_obj

    @classmethod
    def warning(cls):
        if cls.warning_obj is None:
            LedController.init()
        return cls.warning_obj

    @classmethod
    def status1(cls):
        if cls.status1_obj is None:
            LedController.init()
        return cls.status1_obj

    def __init__(self, port_no):
        super().__init__(port_no)

if __name__ == "__main__":

    error = LedController.error()
    warning = LedController.warning()
    status1 = LedController.status1()

    error.on()
    time.sleep(2)
    warning.on()
    time.sleep(2)
    status1.on()
    time.sleep(2)

    warning.off()
    time.sleep(2)
    error.off()
    time.sleep(2)
    status1.off()
