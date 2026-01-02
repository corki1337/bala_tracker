
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
import cv2 as cv
from .detector import detect_green


class CameraNode(Node):

    def __init__(self):
        super().__init__("vision_node")
        self.prev = [0.,0.]
        self.publisher_ = self.create_publisher(Point, 'kordy', 10)


        target_fps = 60
        #width = 1280
        #height = 720

        gst_pipeline = (
            "libcamerasrc ! "
            "video/x-raw, format=NV12, width=1280, height=720, framerate=60/1 ! "
            "videoconvert ! "
            "video/x-raw, format=BGR ! "
            "appsink drop=true max-buffers=1 sync=false"
        )

        self.cap = cv.VideoCapture(gst_pipeline, cv.CAP_GSTREAMER)

        if not self.cap.isOpened():
            self.get_logger().error("Nie udalo sie otworzyc kamery")
        #self.cap = cv.VideoCapture(0, cv.CAP_V4L2)
        #self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
        #self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
        #self.cap.set(cv.CAP_PROP_FPS, 90)


        timer_period = 1/target_fps
        self.timer = self.create_timer(timer_period, self.timer_callback)
        

    def destroy_node(self):
        self.get_logger().info("Zamykanie ")
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        super().destroy_node()
    

    def timer_callback(self):
        msg = Point()
        msg.x = self.prev[0]
        msg.y = self.prev[1]
        msg.z = 0.0
        

        ret, frame = self.cap.read()

        if ret:
            kordy = detect_green(frame)
            if kordy is not None:
                msg.x = float(kordy[0])
                msg.y = float(kordy[1])
                self.prev = [msg.x, msg.y]
        else:
            pass

        self.publisher_.publish(msg)
        self.get_logger().info(f"Publishing: {msg.x}, {msg.y}")

        

        

def main(args = None):
    rclpy.init(args = args)
    
    cam = CameraNode()

    try:
        rclpy.spin(cam)
    except KeyboardInterrupt:
        pass
    finally:
        cam.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
    

