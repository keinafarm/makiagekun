###################################
#
#   MQTT経由で送られた画像データを表示する事を目指す
#   https://qiita.com/TsubasaSato/items/908d4f5c241091ecbf9b
#
#   MQTT(JPEG)->numpy->imdecode
###################################

from MqttThread import MqttThread
import cv2
import numpy as np
import json
import base64

MQTT_PASSWORD = "token:token_3KgDgo0nTlZAPJbO"


class ImageRead(MqttThread):
    def __init__(self):
        super().__init__("mqtt_broker/image")
        self.receive_callback = None

    def on_message(self, client, userdata, msg):
        print("Msg:{0}")
        #        print(msg.topic + " " + str(msg.payload))
        jpg = np.frombuffer(msg.payload, dtype=np.uint8)
        data = base64.b64decode(jpg)
        np_buffer = np.frombuffer(data, dtype=np.uint8)
        img = cv2.imdecode(np_buffer, cv2.IMREAD_COLOR)
        if self.receive_callback:
            self.receive_callback(img)


class StatusRead(MqttThread):
    def __init__(self):
        super().__init__("mqtt_broker/status")
        self.receive_callback = None

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        message = json.loads(msg.payload)

        if self.receive_callback:
            self.receive_callback(message)


obj1 = None
if __name__ == "__main__":
    import time

    obj2 = ImageRead()
    obj1 = MqttThread("mqtt_broker/capture")

    data = {"CAPTURE"}
    obj1.send("CAPTURE")
    while True:
        time.sleep(2)
    """
    img = cv2.imread( "0245840_P01.jpg" , 1 )
    cv2.imshow ( "Image Window" , img )

    cv2.waitKey(0)
#    time.sleep(10)
    cv2.destroyAllWindows()
    """
