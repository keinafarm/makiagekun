# https://pypi.org/project/paho-mqtt/
#

from ThreadBase import ThreadBase

import paho.mqtt.client as mqtt  # ライブラリのimport
import json
import pickle
import os

PARAMETER_FILE = 'mqtt_parameter.prm'


# MQTT Broker
class MqttParameter:
    class_object = None

    @classmethod
    def get(cls):
        if MqttParameter.class_object is None:
            if os.path.exists(PARAMETER_FILE):
                cls.parameter_load()
            else:
                MqttParameter.class_object = MqttParameter()
                MqttParameter.class_object.parameter_save()

        return MqttParameter.class_object

    @classmethod
    def parameter_load(cls):
        with open(PARAMETER_FILE, "rb") as f:
            MqttParameter.class_object = pickle.load(f)

    def parameter_save(self):
        with open(PARAMETER_FILE, "wb") as f:
            pickle.dump(self, f)

    def __init__(self):
        self.mqtt_host = "mqtt.beebotte.com"  # brokerのアドレス
        self.mqtt_port = 1883  # brokerのport
        self.mqtt_keep_alive = 60  # keep alive
        self.mqtt_password = "token:token_3KgDgo0nTlZAPJbO"


class MqttThread(ThreadBase):
    """
    MQTTをThreadで行うクラス
    """

    def __init__(self, topic):
        """
        MQTTブローカーに接続する
        :param topic: 接続するチャンネル/トピック
        """
        super().__init__()
        self.mqttc = mqtt.Client()  # clientオブジェクト作成
        self.mqttc.on_connect = self.on_connect  # 接続時に実行するコールバック関数設定
        self.topic = topic  # トピックを記憶

        # Set the username to 'token:CHANNEL_TOKEN' before calling connect
        self.mqttc.username_pw_set(MqttParameter.get().mqtt_password)
        # パスワードによる認証を設定
        self.mqttc.connect(MqttParameter.get().mqtt_host, MqttParameter.get().mqtt_port,
                           MqttParameter.get().mqtt_keep_alive)  # MQTT broker接続
        self.mqttc.on_message = self.on_message  # 受信に実行するコールバック関数設定
        self.receive_callback = None

        self.start(self.run)  # MQTTループ処理をThreadで開始する

    def run(self):
        """
        Thread処理
        MQTTの送受信処理を回す
        (disconnect()で終了)
        :return:
        """
        self.mqttc.loop_forever()  # MQTT処理ループ
        print("run2 {0}".format(self.topic))

    def on_connect(self, client, userdata, flags, rc):
        """
        接続時のコールバック
        :param client:the client instance for this callback
        :param userdata:the private user data as set in Client() or user_data_set()
        :param flags:response flags sent by the broker
        :param rc:the connection result
        :return:
        """
        print("rc: " + str(rc))  # 接続結果表示

    def send(self, msg):
        """
        MQTTブローカーに送信する
        :param msg: 送信するデータ(jsonに変換して送る)
        :return:
        """
        msg = json.dumps(msg)
        self.mqttc.publish(self.topic, msg)

    def on_message(self, client, userdata, msg):
        """
        メッセージ受診時のコールバック
        :param client:the client instance for this callback
        :param userdata:the private user data as set in Client() or user_data_set()
        :param msg:an instance of MQTTMessage. This is a class with members topic, payload, qos, retain.
        :return:
        """
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload[:50]))
        if self.receive_callback:
            self.receive_callback(msg)

    def disconnect(self):
        """
        切断
        :return:
        """
        self.mqttc.disconnect()

    def set_receive_callback(self, callback):
        if self.receive_callback is None:
            self.receive_callback = callback
            self.mqttc.subscribe(self.topic)  # Topic名を指定して受信開始
        else:
            self.mqttc.subscribe(self.topic)  # Topic名を指定して受信開始


"""
if __name__ == "__main__":
    import time

    obj2 = MqttThread("mqtt_broker/status")
    obj3 = MqttThread("mqtt_broker/image")
    obj4 = MqttThread("mqtt_broker/capture")
    for i in range(1, 5):
        data = {"direction": "status", "sample1": "test{0}".format(i), "sample2": "testYY"}
        jdata = json.dumps(data)
        obj2.send(jdata)
        data = {"direction": "image", "sample1": "test{0}".format(i), "sample2": "testYY"}
        jdata = json.dumps(data)
        obj3.send(jdata)
        data = {"direction": "capture", "sample1": "test{0}".format(i), "sample2": "testYY"}
        jdata = json.dumps(data)
        obj4.send(jdata)
        time.sleep(2)

    obj2.disconnect()
    obj3.disconnect()
    obj4.disconnect()

#    MqttParameter.get().parameter_save()
"""
