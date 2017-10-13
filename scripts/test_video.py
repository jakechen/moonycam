import picamera

camera = picamera.PiCamera()
camera.resolution = (1920, 1080)
camera.start_recording('test.h264')
camera.wait_recording(10)
camera.stop_recording()
