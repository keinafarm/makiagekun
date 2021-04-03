#! env python
# -*- coding: utf-8 -*-

import wx
from MainPanelBase import MainPanelBase
from ImageTest import ImageRead, StatusRead
from MqttThread import MqttThread
import cv2


class Gui(MainPanelBase):
    def __init__(self, parent):
        super(Gui, self).__init__(parent)
        self.status = {"motorOn": 0, "motorDir": 0, "error": 0}

        self.image_obj = ImageRead()
        self.image_obj.set_receive_callback(self.display_image)
        self.status_obj = StatusRead()
        self.capture_obj = MqttThread("mqtt_broker/capture")
        self.control_obj = MqttThread("mqtt_broker/message_ctrl")
        self.status_obj.set_receive_callback(self.display_status)
        self.Bind(wx.EVT_CLOSE, self.onQuit)

    def display_image(self, image):
        """
        https://nippori30.hatenablog.com/entry/2017/10/03/111424
        https://amdkkj.blogspot.com/2017/06/converting-opencv-python-images-into-wxpython-images_17.html

        :param image:
        :return:
        """
        print("Capture")
        height, width = image.shape[:2]
        cv2_image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        data = wx.Bitmap.FromBuffer(width, height, cv2_image_rgb)
        self.m_bitmap_image.SetBitmap(data)

    def display_status(self, msg):
        print("display_status {0}".format(msg))
        print("msg{0}:{1}".format(type(msg), msg))

        convert_table = {"1": True, "0": False}
        print(msg)
        if "motorOn" in msg:
            self.status["motorOn"] = msg["motorOn"]

        if "motorDir" in msg:
            self.status["motorDir"] = msg["motorDir"]

        if "error" in msg:
            self.status["error"] = msg["error"]

        print(self.status)
        text = "Motor ON:{0} Motor Dir={1} Error={2}".format(self.status["motorOn"], self.status["motorDir"],
                                                             self.status["error"])
        self.m_text_message.SetValue(text)

        if self.status["motorOn"]:
            image = wx.Bitmap("MotorOn.png")
            self.m_bitmap_motorOn.SetBitmap(image)
            if self.status["motorDir"]:
                image = wx.Bitmap("MotorUp.png")
                self.m_bitmap_motorDir.SetBitmap(image)
            else:
                image = wx.Bitmap("MotorDown.png")
                self.m_bitmap_motorDir.SetBitmap(image)
        else:
            image = wx.Bitmap("MotorOff.png")
            self.m_bitmap_motorOn.SetBitmap(image)
            image = wx.Bitmap("MotorStop.png")
            self.m_bitmap_motorDir.SetBitmap(image)

        if self.status["error"]:
            image = wx.Bitmap("Error.png")
            self.m_bitmap_Error.SetBitmap(image)
        else:
            image = wx.Bitmap("ErrorOff.png")
            self.m_bitmap_Error.SetBitmap(image)

    def onCaptureButton(self, event):
        self.capture_obj.send("CAPTURE")

    def onCancelButton(self, event):
        self.control_obj.send({"operation": "CANCEL"})

    def onUpButton(self, event):
        self.control_obj.send({"operation": "UP"})

    def onStopButton(self, event):
        self.control_obj.send({"operation": "STOP"})

    def onDownButton(self, event):
        self.control_obj.send({"operation": "DOWN"})

    def onQuit(self, event):
        wx.GetTopLevelParent(self).Destroy()


if __name__ == '__main__':
    app = wx.App(False)
    frame = Gui(None)
    frame.Show(True)

    app.MainLoop()
