#
# Takes a photo every 5 seconds
# and pushes the photo to an S3 bucket
#

# Vars
wait = 5
s3_bucket = 'jakechen'

# Libraries
from time import sleep, gmtime, strftime
from picamera import PiCamera
import boto3

# Initiate and warm-up camera
camera = PiCamera()
camera.resolution = (1440, 1080)
camera.start_preview()
# Camera warm-up time
sleep(2)

# Main loop

time_lapsed = 0
while True:
    camera.capture('image.jpg')
 
    cur_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print('photo taken at {}'.format(cur_time))
   
    s3_key = 'projects/nvcam/image_'+str(time_lapsed)+'.jpg'
    bucket = boto3.resource('s3').Bucket(s3_bucket)
    bucket.upload_file('image.jpg', s3_key)

    print('photo uploaded to {}'.format(s3_key))

    sleep(wait)
    time_lapsed += wait

    if time_lapsed == 60:
        time_lapsed = 0
