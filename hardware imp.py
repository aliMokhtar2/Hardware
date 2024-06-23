from ultralytics import YOLO 
from picamera2 import Picamera2 
import cv2 
from datetime import datetime 
from time import sleep 
import os 
import pyrebase as pyrebase 
import firebase_admin 
from firebase_admin import credentials 
from firebase_admin import firestore 
import pygame.mixer 
# Firebase configuration 
firebaseConfig = { 
'apiKey': "AIzaSyAK-UJu80-3l6axKdM_07Frj-tWxQtLACA", 
'authDomain': "farm-land-ba606.firebaseapp.com", 
'databaseURL': "https://farm-land-ba606-default-rtdb.firebaseio.com", 
'projectId': "farm-land-ba606", 
'storageBucket': "farm-land-ba606.appspot.com", 
'messagingSenderId': "954938723219", 
'appId': "1:954938723219:web:e67df5b32e2300f22af666", 
'measurementId': "G-LWJT6J05WJ" 
} 
# Initialize Firebase services 
firebase = pyrebase.initialize_app(firebaseConfig) 
storage = firebase.storage() 
cred = credentials.Certificate('/home/hwteam/Desktop/farm-land-ba606-firebase-adminsdk-y40ex-4f45f54429.json') 
firebase_admin.initialize_app(cred) 
db = firestore.client() 
db1 = firebase.database() 
# Load YOLO model 
model = YOLO('/home/hwteam/Desktop/best.pt') 
# Initialize Picamera2 
picam2 = Picamera2() 
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (1280, 720)})) 
picam2.framerate = 60 
picam2.start() 
pygame.mixer.init() 
sound1 = pygame.mixer.Sound('/home/hwteam/Desktop/sounds/an an.wav') 
sound2 = pygame.mixer.Sound('/home/hwteam/Desktop/sounds/ehdaa.wav') 
sound3 = pygame.mixer.Sound('/home/hwteam/Desktop/sounds/reem.wav') 
sound4 = pygame.mixer.Sound('/home/hwteam/Desktop/sounds/ehdaa wish.wav') 
sound5 = pygame.mixer.Sound('/home/hwteam/Desktop/sounds/yy.wav') 
sound6 = pygame.mixer.Sound('/home/hwteam/Desktop/sounds/story tell.wav') 
sound7 = pygame.mixer.Sound('/home/hwteam/Desktop/sounds/an an.wav') 
sound8 = pygame.mixer.Sound('/home/hwteam/Desktop/sounds/s7.wav') 
sound9 = pygame.mixer.Sound('/home/hwteam/Desktop/sounds/sto ana.wav') 
sound10 = pygame.mixer.Sound('/home/hwteam/Desktop/sounds/spong.wav') 
while True: 
# Capture frame from Picamera2 
frame = picam2.capture_array() 
# Perform object detection 
results = model.track(source=frame, show=True ,tracker="bytetrack.yaml" ) # No tracking here 
# Iterate through detected objects 
for result in results: 
boxes = result.boxes 
for box in boxes: 
cls = int(box.cls[0]) # Class ID 
conf = box.conf[0] # Confidence score 
name = model.names[cls] # Class name 
# Check if detected object is a monkey (assuming your class ID for monkey is known) 
if name == "Horse" or "Monkey" or "Cattle" or "Deer" or "Rabbit" or "Goat" or "Spider" or "Mule" or "Hamster" or "Koala" and conf > 0.5: 
now = datetime.now() 
dt = now.strftime("%Y-%m-%d_%H-%M-%S") 
name = dt + ".jpg" 
if model.names[cls] == "Monkey": 
sound7.play() 
elif model.names[cls] == "Horse": 
sound7.play() 
elif model.names[cls] == "Cattle": 
sound7.play() 
elif model.names[cls] == "Deer": 
sound7.play() 
elif model.names[cls] == "Rabbit": 
sound7.play() 
elif model.names[cls] == "Goat": 
sound7.play() 
elif model.names[cls] == "Spider": 
sound7.play() 
elif model.names[cls] == "Mule": 
sound7.play() 
elif model.names[cls] == "Hamster" : 
sound7.play() 
elif model.names[cls] == "Koala": 
sound7.play() 
cv2.imwrite(name, frame) # Save the frame as an image 
print(name + " saved") 
# Upload image to Firebase Storage 
storage.child(name).put(name) 
print("Image sent") 
download_url = storage.child(name).get_url(None) 
# Store data in Firestore and Realtime Database 
# Replace with relevant data if needed 
data = {"photo_url": download_url, "dateTime": now.strftime("%Y-%m-%d"), "name": model.names[cls] , "Time": now.strftime("%r")} 
data1 = {"photo_url": download_url, "dateTime": now.strftime("%Y-%m-%d"), "name": model.names[cls] , "Time": now.strftime("%r")} 
db.collection("images").add(data) 
db1.child("Images").push(data1) 
print("URL saved to Firestore & realtime") 
print("done") 
while pygame.mixer.get_busy(): 
pygame.time.delay(100) 
# Remove local image file 
os.remove(name) 
print("File Removed") 
if cv2.waitKey(1) & 0xFF == ord('q'): 
break 
picam2.stop() 
cv2.destroyAllWindows()
