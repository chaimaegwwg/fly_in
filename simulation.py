# import pygame
import sys
import random
from logic import main
from parsing import check_validation
class Zones:
    def __init__(self, 
                 name: str, 
                 row: int | str, 
                 col: int | str, 
                 max_link_capacity: int | float
                 ) -> None:
        self.name: str = name
        self.x: int = int(col) * 50 + 25
        self.y: int = int(row) * 50 + 25
        self.max_link_capacity: int | float = max_link_capacity
        self.current_drones: int = 0
class Drones:
    def __init__(self, 
                 id: int, 
                 info: dict[str, dict[str, Any]], 
                 path: list[str], 
                 cap_zones: dict[str, Any],  
                 connection_data: dict[str, list[tuple[str, int | float]]]
                 ) -> None:
        self.id: int = id
        self.connection_data: dict[str, list[tuple[str, int | float]]] = connection_data
        self.cap_zones: dict[str, Any] = cap_zones
        self.path: list[str] = path
        self.info: dict[str, dict[str, Any]] = info
        self.step: int = 0

    def move(self) -> str | None: 
        if self.step + 1 < len(self.path):
            current_z = self.cap_zones[self.path[self.step]]
            next_z    = self.cap_zones[self.path[self.step + 1]]

            current_name = self.path[self.step]
            next_name = self.path[self.step + 1]
            if next_name == self.path[-1] or current_name == self.path[0]:
                link_cap = float('inf')
            else:
                link_cap = 1
                for neighbor in self.connection_data[current_name]:
                    if neighbor[0] == next_name:
                        link_cap = neighbor[1]
                        break
            
            if next_z.current_drones < link_cap:
                current_z.current_drones -= 1
                next_z.current_drones    += 1
                self.step += 1
                if self.info[next_z.name].get("zone") == "restricted":
                    move_output = f"D{self.id}-{current_z.name}-{next_z.name}"
                else:
                    move_output = f"D{self.id}-{next_z.name}"
                return move_output
        return None
       
def func() -> None:
    info,connection,path = main()
    try:
        nb_drones = check_validation()
    except:
        sys.exit()
    start = path[0]
    row, col = info[start]["position"]
    drone_x = int(col)
    drone_y = int(row)

    index = 0
    target = path[index]
    row, col = info[target]["position"]
    target_x = int(col)
    target_y = int(row)
    index += 1

    max_row = max(int(value["position"][0]) for value in info.values())
    max_col = max(int(value["position"][1]) for value in info.values())

    i = (max_col+1)
    j = (max_row+1)

    zones = {}
    for name,data in info.items():
        x, y = data["position"]
        max_drones = data.get("max_drones",1)
        max_cap = max_drones
        if name == path[0] or name == path[-1]:
            max_cap = float('inf')
        zones[name] = Zones(name,x,y,max_cap)
    zones[path[0]].current_drones = nb_drones


    all_drones = []
    for inde_x in range(nb_drones):
        d = Drones(inde_x,info, path,zones,connection)
        d.id = inde_x
        all_drones.append(d)
    running = True
    while running:
        turn_list = []
        moved_any = False
        for d in all_drones:
            move_info = d.move()
            if move_info:
                turn_list.append(move_info)
                moved_any = True
        if turn_list:
            print(" ".join(turn_list))

        if not moved_any:
            running = False
       
            
   
func()
