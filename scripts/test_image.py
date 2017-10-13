from time import sleep
from picamera import PiCamera
import boto3

camera = PiCamera()
camera.resolution = (1440, 1080)
camera.start_preview()
# Camera warm-up time
sleep(2)
camera.capture('test.jpg')

boto3.resource('s3').Bucket('jakechen').upload_file('test.jpg', 'projects/nvcam/test.jpg')
