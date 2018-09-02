# i photo upload to s3
# change 'i' number you want
import cv2
import numpy as np
import boto3
from datetime import datetime

# Let's use Amazon S3
s3 = boto3.resource('s3',
         aws_access_key_id="AKIAIU4FDAJMV7QZZNCQ", 
         aws_secret_access_key="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")

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)


# Create a VideoCapture object
cap = cv2.VideoCapture(0)
 
# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")
 
# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
 
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
#out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
i = 0

while(True):
  t1 = datetime.now()
  ret, frame = cap.read()
  timestr = ''
  datestr = ''
  if ret == True:
      
    # read and write cctvlog.txt, cctvlog.txt = will save number
    #f = open("cctvfile/cctvlog.txt", "r+")
    count = i
    
    # filename
    s3filename = "cctv2_"+ str(count)+".jpg"
    filename =s3filename
    timestr = str(t1.hour).zfill(2)+":"+str(t1.minute).zfill(2)+":"+str(t1.second).zfill(2)+"."+str(t1.microsecond)[0:2]
    datestr = str(t1.year)+"/"+str(t1.month).zfill(2)+"/"+str(t1.day).zfill(2)
    
    # print text on display
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, timestr, (490, 470), font, 0.5, (0, 0, 0), 2)
    cv2.putText(frame, datestr, (490, 450), font, 0.5, (0, 0, 0), 2)
    # Write the frame into the file 'output.avi'
    #out.write(frame)
    cv2.imwrite(filename,frame)
    
    # Display the resulting frame    
    cv2.imshow('frame',frame)
 
    # Press Q on keyboard to stop recording
    if i==5:
        break
    else:
        # Upload a new file
        data = open(filename, 'rb')
        s3.Bucket('2018imtest').put_object(Key=s3filename, Body=data)
        print("save ", filename)
        
        # cctvlog update
        #number = ''+str(int(count)+1)
        #f = open("cctvfile/cctvlog.txt", "w")
        #f.write(number)
        #print("number = ",number)
        #f.close()
        
    i += 1
  # Break the loop
  else:
    break 
 
# When everything done, release the video capture and video write objects
cap.release()
#out.release()
 
# Closes all the frames
cv2.destroyAllWindows() 
