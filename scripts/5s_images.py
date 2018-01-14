#
# Takes a photo every ~5 second
# depending on transfer time
# 
# Keeps 10 minutes worth locally, then loops
#

# Libraries
import argparse
from time import sleep, gmtime, strftime
from picamera import PiCamera
import boto3
import os
import logging
logging.basicConfig(filename='out.log',level=logging.INFO)

def main(s3_bucket, s3_prefix, wait, keep_minutes):

    keep_count = (keep_minutes*60)/wait

    i = 0

    while i<keep_count:
        camera.capture('./image_latest.jpg')
        camera.capture('./image_'+str(i)+'.jpg')

        cur_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        logging.info('photo taken at {}'.format(cur_time))

        s3.upload_file(
            './image_latest.jpg',
            s3_bucket, 
            s3_prefix+'image_latest.jpg',
            ExtraArgs = {
              'StorageClass': 'STANDARD_IA'
            }
        )

        sleep(wait-2) # accoutn for transfer time

        i+=1

        if i == keep_count:
            i = 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('s3_bucket', help='bucket to send photos to')
    parser.add_argument('s3_prefix', help='key to save photos as')
    parser.add_argument('-w', '--wait', help='interval between photos, default=5', type=int, default=5)
    parser.add_argument('-keep', '--keep_minutes', help='how many minutes to keep, default=10', type=int, default=10)
    args = parser.parse_args()
    
    # Initiate and warm-up camera
    camera = PiCamera()
    camera.resolution = (1440, 1080)
    camera.start_preview()
    # Camera warm-up time
    sleep(2)

    # Main loop
    s3 = boto3.client('s3')

    main(args.s3_bucket, args.s3_prefix, args.wait, args.keep_minutes)
