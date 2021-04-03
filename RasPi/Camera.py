from io import BytesIO
from picamera import PiCamera
from Parameter import PGet


class CameraController:
    def __init__(self):
        self.camera = PiCamera()  # カメラオブジェクト
        self.camera.resolution = PGet().camera_resolution  # 解像度
        self.camera.start_preview()  # カメラ起動

    def one_shot(self):
        my_stream = BytesIO()  # 撮影データを保存するストリーム
        self.camera.capture(my_stream, 'jpeg')  # 撮影
        return my_stream.getvalue()


if __name__ == "__main__":
    count = 0


    def save_proc(data):
        global count
        name = "image{0}.jpg".format(count)
        with open(name, "wb") as f:
            f.write(data)
        count += 1
        print("Capture:{0}".format(name))


    obj = CameraController()
    buffer = obj.one_shot()
    save_proc(buffer)
    buffer = obj.one_shot()
    save_proc(buffer)
    buffer = obj.one_shot()
    save_proc(buffer)
