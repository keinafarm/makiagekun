##################################################
#
#   Buzzer制御クラス
#
#   ブザーのON/OFF制御を行う
#
#
##################################################

from gpiozero import Buzzer
from Parameter import PGet
import time

class   BuzzerController:
    PATTERN = [
        {"on": 1, "off": 0},         # なりっぱなし
        {"on": 1, "off": 1},         # 1秒周期
        {"on": 0.5, "off": 0.5},     # はやいの
        {"on": 0.3, "off": 0.3}      # もっとはやいの
    ]

    def __init__(self):
        """
        ブザー鳴動処理
        :param port_no:ブザー用のポート番号
        """
        self.buzzer_port = Buzzer(PGet().port_buzzer)

    def on(self, pattern):
        """
        ブザー鳴動
        :param pattern: ブザー鳴動パターンPATTERN[n]で指定
        :return:
        """
        self.buzzer_port.beep( pattern["on"], pattern["off"] )

    def off(self):
        self.buzzer_port.off()

if __name__ == "__main__":
    obj = BuzzerController()
    print("Pattern 1")
    obj.on(BuzzerController.PATTERN[0])
    time.sleep(3)
    obj.off()
    time.sleep(1)

    print("Pattern 2")
    obj.on(BuzzerController.PATTERN[1])
    time.sleep(3)
    obj.off()
    time.sleep(1)

    print("Pattern 3")
    obj.on(BuzzerController.PATTERN[2])
    time.sleep(3)
    obj.off()
    time.sleep(1)

    print("Pattern 4")
    obj.on(BuzzerController.PATTERN[3])
    time.sleep(3)
    obj.off()
