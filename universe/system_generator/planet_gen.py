import name_generation as ngen
import starforge_systems as ss
from random import randint, choice
from json import dumps
from colorama import Fore


DISTRICT = "Testing"



rst = Fore.RESET
grn = Fore.GREEN
blu = Fore.CYAN
red = Fore.RED

life_envs = ["Wet", "Islands"]
water_envs = ["Ocean"]
deadly_envs = ["Gas", "Gas & rings", "Lava"]

system_types = {"Double-star system": {"rarity": 10, "stars": 2, "center": ss.marker("System center", 0, 0).export(), "distance": 1000}, "Single-star system": {"rarity": 1, "stars": 1}}

planet_types = {500: {"Lava": 1}, 1000: {"No atmosphere": 3, "Dry": 3, "Lava": 1}, 1400: {"Islands": 4, "Ocean": 2, "Wet": 1}, 2500: {"Ice": 4, "Dry": 6, "No atmosphere": 3, "Gas": 1}, 9999: {"Gas & rings": 4, "Ice": 3, "Dry": 3, "Gas": 1}}
big_planet_types = ["Gas", "Gas & rings"]

roman_numbers = ["I", "II", "III", "IV", "V", "VI", "VII", "IIX", "IX", "X"]

ngen.init()


def add_render_task(object_name: str, type: str):
    open("things_to_render.txt", "a+").write("\n"+dumps({"url": path+object_name, "name": object_name, "env": type}))

def characterize(distance, size):
    if distance > 2000 and size > 300:
        return choice(big_planet_types)
    for dis in planet_types:
        if distance < dis:
            for typee in planet_types[dis]:
                if randint(1, planet_types[dis][typee]) == 1:
                    return typee
        

def generate_system():
    global path
    system_name = ngen.generate_name(randint(5,10),capitalize=True)
    path="universe/"+DISTRICT+"/"+system_name+"/"
    print("Generating system "+system_name)
    system_type = "Single-star system"
    for type in system_types:
        if randint(1,system_types[type]["rarity"]) == system_types[type]["rarity"]:
            system_type = type
            break
    print("System type: " + system_type)
    planet_amount = randint(5,10)
    print("Planets: "+str(planet_amount))
    if input("Press enter to continue")=="":
        print("Generation confirmed.\n")
        
        system = ss.system(system_name)
        
        sun_size = randint(1000,1800)
            
        
        try:
            suns = system_types[system_type]["stars"]
        except:
            suns = 1
        if suns > 1:
            center = system_types[system_type]["center"]
            system.add_object(center)
            for i in range(suns):
                star = ss.star(system_name+" "+roman_numbers[i], sun_size, True, ).export()
                star.set_texture(path, 0.5)
                system.add_object(star)
                add_render_task(system_name+" "+roman_numbers[i], "star")
                
        else:
            center = ss.star(system_name, sun_size).export()
            add_render_task(system_name, "star")
            center.set_texture(path, 0.5)
            system.add_object(center)
            
        
        
        
        for i in range(planet_amount):
            distance = (i+1)*randint(300,500)
            size = (i+1*randint(2,7))*randint(10,50)
            env = characterize(distance, size)
            if env in life_envs:
                print(grn)
            elif env in water_envs:
                print(blu)
            elif env in deadly_envs:
                print(red)
            name = ngen.generate_name(randint(5,10), True)
            
            print(name, "SZE:", size,"DST:", distance, end=" ")
            moon_count = randint(0,int(size/50))
            if size > 450:
                moon_count*= 4
                if distance > 3000:
                    moon_count = randint(20,40)
            if moon_count < int(size/50)/3:
                moon_count = 0
            moon_count = int(round(moon_count/2))
            
            if moon_count < 0:
                moon_count = 0
            
            if moon_count > 30:
                moon_count = randint(20,35)
            
            
            
            print(f"SFC: {env} MNS: ({moon_count})")
            planet = ss.body(name, "planet", center, distance, size, env).export()
            planet.set_texture(path, size*100)
            add_render_task(name, env)
            planet_dist = distance
            
            for j in range(moon_count):
                moon_name = ngen.generate_name(randint(4,7), True)
                distance = (j+3)*randint(100,150)
                size = randint(70,130)
                env = characterize(planet_dist, 100)
                if "ring" in env:
                    env = "Gas"
                print("   • " + moon_name, f" | DST: {distance} | SZE: {size} | SFC: {env}")
                moon = ss.body(moon_name, "moon", planet, distance, size, env).export()
                moon.set_texture(path, size*100)
                system.add_object(moon)
                add_render_task(moon_name, env)
                
        
            system.add_object(planet)
            print(rst)
        
        print("Export to json? (y/n")
        if input() == "y":
            print(f"Exporting to /exported/{system_name}.json")
                
            open("./exported/"+system_name+".json", "w+").write(dumps(system.export(True)))
            
            
    else:
        print("Generation canceled.")
    
    print("\n")


while 1:
    generate_system()