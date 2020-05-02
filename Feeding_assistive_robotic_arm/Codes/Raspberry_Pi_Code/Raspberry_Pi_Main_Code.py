from imutils.video import VideoStream
from imutils import face_utils
from scipy.spatial import distance as dist
import argparse
import imutils
import time
import dlib
import cv2 
import RPi.GPIO as GPIO
import time
import os
import pyfirmata
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
board = pyfirmata.Arduino('/dev/ttyACM0')
green=board.get_pin('d:11:o')
red=board.get_pin('d:12:o')
red.write(1)
green.write(1)
counter=0
q=0
w=1

def eye_aspect_ratio(eye):
	A = dist.euclidean(eye[14], eye[18])
	B = dist.euclidean(eye[13], eye[19])
	C = dist.euclidean(eye[15], eye[17])
	X=(A+B+C)/3
	return X


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
args = vars(ap.parse_args())
FACIAL_LANDMARKS_IDXS = ("mouth", (61, 68))

print("loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])
print("loading complete")
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]						
print("camera sensor warming up...")
vs = VideoStream(src=0).start()
time.sleep(0.01)

while True:
	red.write(1)
	green.write(0)
	if(GPIO.input(11) == 1):
		q=1
		servo=board.get_pin('d:9:s')
		servo1=board.get_pin('d:8:s')
		servo2=board.get_pin('d:6:s')
		servo.write(90)
		servo1.write(130)
		servo2.write(95)
		
		p=90
		o=140
		l=100
		for i in range(90,180):
			servo.write(i)
			time.sleep(0.04)
		
		for i in range(130,140):
			servo1.write(i)
			time.sleep(0.04)
		
		for i in range(95,55,-1):
			servo2.write(i)
			time.sleep(0.04)
		time.sleep(2)
		for i in range(55,95):
			servo2.write(i)
			time.sleep(0.04)
		
		for i in range(140,130,-1):
			servo1.write(i)
			time.sleep(0.04)
		
		for i in range(180,90,-1):
			servo.write(i)
			time.sleep(0.04)

		time.sleep(2)
		for i in range(130,140):
			servo1.write(i)
			time.sleep(0.04)
		for i in range(95,100):
			servo2.write(i)
			time.sleep(0.04)
		green.write(1)
		red.write(0)
		time.sleep(3)
		os.system("espeak \"please eat\" -ven+f5 -g50")
		time.sleep(2)
	if(q==1):
		break
print("out of the loop")		

if(q==1):		
	while True:
		frame = vs.read()
		frame=cv2.flip(frame,1)
		frame=cv2.resize(frame,(320,240),interpolation=cv2.INTER_AREA)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		rects = detector(gray, 0)

		if len(rects) > 0:
			text = "{} face(s) found".format(len(rects))
			cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
				0.5, (0, 0, 255), 2)	
			for rect in rects:
				(bX, bY, bW, bH) = face_utils.rect_to_bb(rect)
				cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH+50),
					(0, 255, 0), 1)
			
				print(bX,bY,bW,bH)
				shape = predictor(gray, rect)
				shape = face_utils.shape_to_np(shape)
				leftEye = shape[lStart:lEnd]
				leftEAR = eye_aspect_ratio(leftEye)
				leftEyeHull = cv2.convexHull(leftEye)
				cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
				cv2.putText(frame, "EAR: {}".format(leftEAR), (10, 50), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
				
				
				if bX>130:
					p=p+3
					servo.write(p)
					time.sleep(0.2)
				
				if bX<60:
					p=p-3
					servo.write(p)
					time.sleep(0.2)
				
				if bX<130:
					if bX>60:
						servo.write(p)
						time.sleep(0.2)
				
				if bY>70:
					l=l-4
					servo2.write(l)
					time.sleep(0.2)
				
				if bY<35:
					l=l+4
					servo2.write(l)
					time.sleep(0.2)
				
				if bY<70:
					if bY>35:
						servo2.write(l)
						time.sleep(0.2)
				if bH<95:
					if o<160:
						o=o+3
						servo1.write(o)
						time.sleep(0.2)
				
				if leftEAR>8:
					w=0
					print("Mouth Opened")
					counter=counter+1
					cv2.putText(frame, "Mouth opened", (10, 120),	
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
					os.system("espeak \"mouth opened\" -ven+f5 -g50")
					time.sleep(0.5)

		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		if w==0:
			break
		if key == ord("q"):
			
			break

	if(p>90):
		for i in range(p,90,-1):
			servo.write(i)
			time.sleep(0.04)
	if(p<90):
		for i in range(p,90):
			servo.write(i)
			time.sleep(0.04)
	if(o>130):
		for i in range(o,130,-1):
			servo1.write(i)
			time.sleep(0.04)
	if(o<130):
		for i in range(o,130):
			servo1.write(i)
			time.sleep(0.04)
	if(l>85):
		for i in range(l,85,-1):
			servo2.write(i)
			time.sleep(0.04)
	if(l<85):
		for i in range(l,85):
			servo2.write(i)
			time.sleep(0.04)
	time.sleep(4)	

cv2.destroyAllWindows()
vs.stop()












	
	
