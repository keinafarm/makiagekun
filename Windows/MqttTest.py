# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt  # ライブラリのimport
import json

# MQTT Broker
MQTT_HOST = "mqtt.beebotte.com"  # brokerのアドレス
MQTT_PORT = 1883  # brokerのport
MQTT_KEEP_ALIVE = 60  # keep alive


# broker接続時
def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))  # 接続結果表示

# メッセージ受信時
def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
# メッセージ受信時
def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def pub():
    mqttc = mqtt.Client()  # clientオブジェクト作成
    mqttc.on_connect = on_connect  # 接続時に実行するコールバック関数設定

    # Set the username to 'token:CHANNEL_TOKEN' before calling connect
    mqttc.username_pw_set("token:token_3KgDgo0nTlZAPJbO")

    mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEP_ALIVE)  # MQTT broker接続

    mqttc.loop_start()  # 処理開始
    data = {"sample1": "test1", "sample2":"test2"}
    jdata = json.dumps(data)

    mqttc.publish("mqtt_broker/status",jdata)  # topic名="Topic1"に "test1"というメッセージを送信


def sub():
    mqttc = mqtt.Client()
    mqttc.on_message = on_message  # メッセージ受信時に実行するコールバック関数設定
    mqttc.on_connect = on_connect

    mqttc.username_pw_set("token:token_3KgDgo0nTlZAPJbO")
    mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEP_ALIVE)

    mqttc.subscribe("mqtt_broker/status")  # Topic名："topic1"を購読

    mqttc.loop_forever()  # 永久ループ


pub()
sub()
