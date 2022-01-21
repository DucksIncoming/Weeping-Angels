# Weeping Angels v0.0
# by DucksIncoming
# 1/21/22
# https://github.com/DucksIncoming/weeping-angels

lastFace = 0 # Only need the X component.

def stopMovement():
  # If the statue is moving, stop it in place.
  # If not moving, this does nothing.

  return true

def lookForFace():
  # Code for facial detection

  # Returns true if face found and sets lastFace,
  # returns false if no face found

  lastFace = 100
  return true

if (lookForFace()):
  stopMovement()
else:
  # Rotate head until aligned with lastFace