# Station orbits
object = "Idus" 
# in system
system = "Abooga"

# At a distance of
distance = 100 #default: 50
# And a speed of
speed = 20 # default: 40
# The size of this station is: (%)
size = 50

# This station is angeled by: (Deg)
rotation = -5

# This stations name is:
name = "Bilow"

# This station has following facilities:
facilities = {
    
    "build": False,
    "repair": False,
    "refuel": True,
    "guild": False,
    "market": False
    
}
















########################################

import pyperclip
from json import dumps

size *= 0.1

texture = f"universe/Galaxentre/{system}/{name}/{name}.png"


facilities_final = []

for item in facilities:
    if facilities[item]:
        facilities_final.append(item)

s_type = "station"
if facilities_final == ["refuel"]:
    s_type = "refueling_station"

data = {
  "movement": "orbit",
  "position": {
    "distance": distance,
    "parent": object,
    "rotation": rotation,
    "speed": speed
  },
  "size": size,
  "station_data": {
    "facilities": facilities_final
  },
  "texture": texture,
  "type": s_type
}

pyperclip.copy(dumps(data))
print("\n\n\n\n")
print(data)
print("\n\n\n\n")