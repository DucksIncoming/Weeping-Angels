from pyfirmata import Arduino, SERVO
import time

PORT = "COM3"

try:
    board = Arduino(PORT)
except:
    print("Arduino not plugged in! (Or not accessible on specified port: '" + PORT + "')")
    time.sleep(3)
    quit()

