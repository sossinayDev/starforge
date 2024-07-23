class space_object:
    def __init__(self, name: str, data: dict):
        self.name = name
        self.data = data
    def export(self):
        return self.data
    def set_texture(self, path:str, ms_per_frame:int):
        if not path.endswith("/"):
            path+="/"
        self.data["texture-animated"] = path+self.name
        self.data["texture"] = path+self.name+"/"+self.name+".png"
        self.data["mllspf"] = ms_per_frame

class system:
    def __init__(self, name):
        self.name = name
        self.objects=[]
    
    def add_object(self, object: space_object):
        self.objects.append(object)
    
    
    def export(self, debug=False):
        data = {}
        if debug:
            print(f"Started exporting of system {self.name} with a total of {len(self.objects)} objects")
        for object in self.objects:
            print(object.name)
            data[object.name]= object.data
        
        return data


class marker:
    def __init__(self, name: str, x: int, y: int):
        self.x = x
        self.y = y
        self.name = name
    def export(self):
        return space_object(self.name, {"type": "marker", "movement": "static", "position": {"x": self.x, "y": self.y}})


class star:
    def __init__(self, name: str, size: int, orbits: bool = False, parent: space_object = marker("System center", 0, 0).export(), orbit_distance: int = 2000):
        self.name = name
        self.size = size
        if not orbits:
            self.movement="static"
            self.position = {"x": 0, "y": 0}
        else:
            self.movement="orbit"
            self.position = {"parent": parent.name, "distance": orbit_distance, "speed": 100/orbit_distance}
    def export(self):
        data = {"type": "star", "size": self.size, "movement": self.movement, "position": self.position}
        return space_object(self.name, data)

class body:
    def __init__(self, name: str, body_type: str, parent: space_object, distance: int, size: int, env: str = "unset"):
        self.name = name
        self.parent = parent.name
        self.distance = distance
        self.size = size
        self.type = body_type
        self.env = env
    def export(self):
        obj = {"type": self.type, "movement": "orbit", "position": {"parent": self.parent, "distance": self.distance, "speed": 100/self.distance}, "size": self.size, "surface": self.env}
        return space_object(self.name, obj)