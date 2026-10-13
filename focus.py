import cv2
import time  
from ultralytics import YOLO

#opens and loads everything :)
cap = cv2.VideoCapture(0)
model = YOLO("yolo11n.pt")

#colors, blue and red
BLUE = (255, 180, 60)
RED = (80, 60, 255)

#event log memory   
phoneBefore = False   # check if phone was in last frame
pickups = 0           # how many times the phone appeared
missingFrames = 15    # frames in a row with no phone (starts at 15 = "no phone yet")

#show frames until quit (press q)
while True:
	#reads if frame exists, it reads it
	success, frame = cap.read()
	
	if not success:
		break
	#flips frame so its in mirror mode
	flipFrame = cv2.flip(frame, 1)
	
	#detect people (0) and phones (67), ignore anything under 50% sure   # confidence info so it will only flag sure cases
	results = model(flipFrame, classes=[0,67], conf=0.5, verbose = False)

	#check for phone in frame
	ifPhone = False
	for box in results[0].boxes:
		class_id = int(box.cls[0]) 
		x1, y1, x2, y2 = map(int, box.xyxy[0]) 

		if class_id == 67:
			ifPhone = True
			color = RED        
			label = "PHONE"   
		else:                  
			color = BLUE
			label = "PERSON"

		cv2.rectangle(flipFrame, (x1, y1), (x2, y2), color, 3)   
		cv2.putText(flipFrame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

	#ignore short dropouts: phone only counts as gone after 15 frames missing
	if ifPhone:
		missingFrames = 0
	else:
		missingFrames += 1
	phoneNow = ifPhone or missingFrames < 15

	#event log: only when phone appears or goes away  
	if phoneNow and not phoneBefore: #if camera sees phone and no phone was detected before
		pickups += 1
		print(time.strftime("%H:%M:%S"), "PHONE DETECTED (pickup", pickups, ")")
	if not phoneNow and phoneBefore:
		print(time.strftime("%H:%M:%S"), "PHONE PUT AWAY")
	phoneBefore = phoneNow

	#shows focus state on camera screen
	if phoneNow:
		status = "PHONE DETECTED"
		color = RED
	else: 
		status = "FOCUSED"
		color = BLUE
	
	#shows text
	cv2.putText(flipFrame, status, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
	cv2.putText(flipFrame, "PICKUPS: " + str(pickups), (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, BLUE, 2)   

	cv2.imshow("FIVES FOCUS", flipFrame)  
	
	if cv2.waitKey(1) & 0xFF ==ord("q"):
		break

#shut it all down hehe
cap.release()
cv2.destroyAllWindows()