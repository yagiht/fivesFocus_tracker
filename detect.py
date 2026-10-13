#Load pretrained YOLO model
from ultralytics import YOLO
model = YOLO("yolo11n.pt")
results = model("test.jpg")

#Run detection on image/webcam

#prints name and confidence

for box in results[0].boxes:
	class_id = int(box.cls[0])
	name = model.names[class_id]
	print(name)

results[0].save("out.jpg")

