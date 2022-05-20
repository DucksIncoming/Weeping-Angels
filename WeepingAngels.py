# Weeping Angels v1.0
# by DucksIncoming
# 5/17/22
# https://github.com/DucksIncoming/weeping-angels

# Thank god cv2 exists this literally took 10 minutes to implement lmaooo
import cv2
import time
from pyfirmata import Arduino, SERVO

# Arduino config
port = "COM7" # Set to the USB port of your arduino device
servoPin = 4 # Set to your servo pin (digital only)
debugMode = False
NoFaceFound = True

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)

if (not debugMode):
  try:
    board = Arduino(port)
  except:
    print("Arduino board not plugged in! (Or not accessible on specified port)")
    time.sleep(5000)
    quit()

  board.digital[servoPin].mode = SERVO
  board.digital[servoPin].write(0)


lastFace = [0, 0]
TimeSinceLastFace = 0
rotationMemory = 0.0
targetRotation = 0.0

running = 0
  
while True:
  _, img = capture.read()
  face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, 1.1, 8)

  # This is sketchy but im bored lol
  i = 0
  for (x, y, w, h) in faces:
    if (i == 0):
      NoFaceFound = False
      TimeSinceLastFace = 0
      faceFound = True
      cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)
      i += 1
      lastFace = 320 - x+(w/2)
      print("X: " + str(x))
      print("W: " + str(x+(w/2)))

  cv2.imshow('Weeping Angels GUI', img)
  TimeSinceLastFace += 1

  print(TimeSinceLastFace)

  if (TimeSinceLastFace > 15 and NoFaceFound == False):
    print("LastFace X Pos: " + str(lastFace))
    targetRotation += rotationMemory
    targetRotation = 60 * ((lastFace - 160) / 160)
    board.digital[servoPin].write(targetRotation % 180)
    rotationMemory = targetRotation
    NoFaceFound = True
    
  # Maybe make this work? I'll consider it
  k = (cv2.waitKey(30) & 0xff)
  if (k==27):
    break

capture.release()
board.exit()
