#
# Takes a photo every 5 second
# Keeps 10 minutes worth locally, then loops
#

# Vars
wait = 5
keep_minutes = 10

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
keep_count = (keep_minutes*60)/wait

i = 0

while i<keep_count:
    camera.capture('./images/latest/image_latest.jpg')
    camera.capture('./images/loop/image_'+str(i)+'.jpg')
 
    cur_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print('photo taken at {}'.format(cur_time))

    sleep(wait)

    i+=1

    if i == keep_count:
        i = 0
