# 웹캠 화면을 보여주다가 'q'를 누르면 사진이 해당하는 경로에 저장되고, s3에 저장되는 파일.
import cv2
import numpy as np
import boto3

# 당신의 aws계정과 각 변수를 설정해주세요.
access_key = "your access key id"
secret_key = "your secret access key id(write this)"
bucket_name = "your bucket name"
save_raspberry_filename = "test.jpg"                  # 라즈베리파이 자체에 저장하고싶은 파일 이름
save_s3_filename = "test.jpg"                         # s3에 저장하고싶은 파일 이름
# Amazon s3 사용하기
s3 = boto3.resource('s3',
         aws_access_key_id=access_key, 
         aws_secret_access_key=secret_key)

# 잘 연결됐는지 s3에 있는 버켓 이름 출력하기.
for bucket in s3.buckets.all():
    print(bucket.name)

# 비디오 캡쳐 object 만들기
cap = cv2.VideoCapture(0)
 
# 정상적으로 카메라가 열렸는지(인식됐는지) 확인
if (cap.isOpened() == False): 
  print("Unable to read camera feed")
 
# 프레임 크기 세팅하기.
frame_width = int(cap.get(3)) # 640
frame_height = int(cap.get(4)) # 480
print(frame_width,", ", frame_height)

# 사진에 출력될 문자
str = "Hello"

while(True):
  # 비디오에서 읽어오기.
  ret, frame = cap.read()
  
  if ret == True: 
    # 텍스트를 화면에 출력해주기.
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, str, (500, 430), font, 0.5, (0, 0, 0)

    # 1234.jpg 라는 이름으로 읽은 frame 저장하기(라즈베리파이에)
    cv2.imwrite(save_filename,frame)
                
    # 화면에 보여주기    
    cv2.imshow('frame',frame)
 
    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Upload a new file
        data = open(save_filename, 'rb')
        s3.Bucket(bucket_name).put_object(Key=save_filename, Body=data)
        break
  # Break the loop
  else:
    break 
 
# When everything done, release the video capture and video write objects
cap.release()
#out.release()
 
# Closes all the frames
cv2.destroyAllWindows() 


