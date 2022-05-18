# Weeping Angels v1.0
# by DucksIncoming
# 5/17/22
# https://github.com/DucksIncoming/weeping-angels

# Thank god cv2 exists this literally took 10 minutes to implement lmaooo
import cv2
import time
from pyfirmata import Arduino, SERVO

# Arduino config
port = "COM6" # Set to the USB port of your arduino device
servoPin = 9 # Set to your servo pin (digital only)
debugMode = True
NoFaceFound = True

if (not debugMode):
  try:
    board = Arduino(port)
  except:
    print("Arduino board not plugged in! (Or not accessible on specified port)")
    time.sleep(5000)
    quit()

  board.digital[servoPin].mode = SERVO
  board.digital[servoPin].write(0)

capture = cv2.VideoCapture(0)
lastFace = [0, 0]
TimeSinceLastFace = 0
rotationMemory = 0.0
targetRotation = 0.0

while True:
  _, img = capture.read()
  face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, 1.1, 8)

  targetRotation = ((lastFace[0] - 160.0) / 160.0) * 30.0

  # This is sketchy but im bored lol
  i = 0
  for (x, y, w, h) in faces:
    if (i == 0):
      NoFaceFound = False
      TimeSinceLastFace = 0
      faceFound = True
      cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)
      i += 1
      lastFace = [(x + w) / 2, (y + h) / 2]

  cv2.imshow('Weeping Angels GUI', img)
  TimeSinceLastFace += 1

  print(TimeSinceLastFace)

  if (TimeSinceLastFace > 15 and NoFaceFound == False):
    print(lastFace)
    if (not debugMode):
      board.digital[servoPin].write(rotationMemory + targetRotation)
    rotationMemory += targetRotation
    print(targetRotation)
    NoFaceFound = True
    TimeSinceLastFace = 0
  
  k = (cv2.waitKey(30) & 0xff)
  if (k==27):
    break

capture.release()