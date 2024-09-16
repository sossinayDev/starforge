# Station orbits
object = "Byish" 
# in system
system = "Byish"

# At a distance of
distance = 2000 #default: 50
# And a speed of
speed = 15 # default: 40
# The size of this station is: (%)
size = 10

# This station is angeled by: (Deg)
rotation = 0

# This stations name is:
name = "Motob"

# This station has following facilities:
facilities = {
    
    "build": False,
    "repair": False,
    "refuel": True,
    "guild": False,
    "market": False
    
}
# Additional:
cost_per_fuel_unit = 5















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
    s_type = "refueling station"

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

if facilities_final == ["refuel"]:
  data["cost_per_fuel_unit"] = cost_per_fuel_unit

pyperclip.copy(dumps(data))
print("\n\n\n\n")
print(data)
print("\n\n\n\n")