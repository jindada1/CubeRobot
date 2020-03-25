from cv2 import VideoCapture, CAP_DSHOW, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT

class Camera:
    '''
        valid video frame size (width x height):
            640 x 480
            352 x 288
            320 x 240
            176 x 144
            160 x 120
    '''

    def __init__(self, camera=1, w=640, h=480):
        self.camera = camera
        self._video = None
        self.width =  w
        self.height = h

    def open(self):
        # Open the camera, 0 is the first camera device on you computer
        self._video = VideoCapture(self.camera, CAP_DSHOW)

        if not self._video.isOpened():
            if self.camera > 0:
                self.camera -= 1
                self.open()
                return
            else:
                raise ValueError("Unable to open camera", self.camera)

        self._video.set(CAP_PROP_FRAME_WIDTH, self.width)
        self._video.set(CAP_PROP_FRAME_HEIGHT, self.height)

    # get frame captured by camera
    def frame(self):
        if self._video:
            ret, frame = self._video.read()
            return frame if ret else None

    # release camera
    def close(self):
        if self._video and self._video.isOpened():
            self._video.release()

    # release camera when the object is destroyed
    def __del__(self):
        self.close()
