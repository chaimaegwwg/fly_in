from parsing import make_a_dictionary,check_hub
import re
import sys
#mission is make 2 array and display the place 
#mission tomorrow is for make sure for parsing also add attribuite like the cost 
#mission make sure u understand the dijikstra and do it 
# the finale parsing for the part of connection

class Grid:
    def __init__(self,name, row, col, zone=0, color =0, max_drones = 0,visited=0,value=0):
        self.name = name 
        self.row = row
        self.col = col
        self.zone = zone
        self.color = color
        self.max_drones = max_drones
        self.place = 0
        self.value = value
        self.visited = False

def display(grid, start , end):
    start_row, start_col = start
    end_row, end_col = end
    end_col = end_col+1
    end_row = end_row+1
    for x in range(start_row, end_row):
        for y in range(start_col, end_col):
            if grid[x][y].place == 1:
                print(" + ",end="")
            else:
                print(" - ",end="")
 
        print()
    
def ft_info(info, start,end):
    start_row, start_col = start 
    end_row ,end_col = end
    grid = []
    max_r = max(start_row, end_row)
    max_c = max(start_col, end_col)
    for key, value in info.items():
        r, c = value["position"]
        max_r = max(max_r, int(r))
        max_c = max(max_c, int(c))
    for x in range(0, max_r + 1):
        row_list = []
        for y in range(0, max_c + 1):
            step = Grid("anonymous", x, y)
            row_list.append(step)
        grid.append(row_list)
  
    try:
        grid[start_row][start_col].name = "start_hub"
        grid[start_row][start_col].place = 0
        grid[end_row][end_col].name = "start_end"
        grid[end_row][end_col].place = 5
        grid[end_row][end_col].zone = 5
    except IndexError:
        # print(f"ERROR: Cannot access grid[{end_row}][{end_col}]. Max indices are [{max_r}][{max_c}]")
        sys.exit()
    
    for key , value in info.items():
        row , col =value["position"]
        row = int(row)
        col = int(col)
        name = value["name"]
        if row > end_row or col > end_col:
            continue
            
        try:
            zone = value["zone"]
            if zone == "priority":
                zone = 1
            elif zone == "normal":
                zone = 5
            elif zone == "restricted":
                zone = 20
            elif zone == "first":
                zone = 0
            else:
                zone = float('inf')
        except:
            zone = 0
        try:
            max_drone = value["max_drones"]
            max_drone = int(max_drone)
        except:
            max_drone = 0
        try:
            color = value["color"]
        except:
            color = 0
        grid[row][col].zone = zone
        grid[row][col].visited = False
        grid[row][col].place = 1
        grid[row][col].name = name
        grid[row][col].color = color
        grid[row][col].max_drones = max_drone
        
    return grid


def choice_the_path(places,info,grid,dic,visited,val,current_place,path):
    com = float('inf')
    name = None
    for i in places:
        key = i[0]
        row ,col= info[key]["position"]
        row = int(row)
        col = int(col)
        zone = grid[row][col].zone

        if key not in dic or (val + zone) < dic[key]:
            dic[key] = val + zone
            path[key] = current_place

    for node,v in dic.items():
        if node not in visited and v < com:
            com = v
            name = node
    return name,dic

def dijikstra(connection, info,grid):
    # place = next(iter(connection))
    place = "hub"
    total_v = len(info)-1
    path = {}
    visited = []
    value = 0
    visited_zones = 0
    dic = {"hub": 0}
    while place is not None:

        row ,col= info[place]["position"]
        row = int(row)
        col = int(col)

        if place not in visited:
            grid[row][col].visited =True
            visited.append(place)
    
        value = dic[place]
        neighbors = connection.get(place, [])
        name , dic = choice_the_path(neighbors,info,grid,dic,visited,value,place,path) 
        if name is None:
            break
        if name == "goal":
            lst = [v for k, v in dic.items() if k not in visited]
            if lst:
                m_min = min(lst)
            else:
                m_min = float('inf')

            if dic["goal"] <= m_min:
                place = "goal"
                break
        place = name
        value = dic[name]

    if name == "goal":
     
        route = []
        curr = "goal"
        while curr in path:
            route.append(curr)
            curr = path[curr]
        route.append("hub") 
        route.reverse() 
    
    return route


def main():
    dic = make_a_dictionary()
    position = []
    lst_position = []
    for key, value in dic.items():
        if key.strip() == "start_hub":
            for x in value:
                v = x.split()
                start = (int(v[1]),int(v[2]))
                v = start
        if key.strip() == "end_hub":
            for x in value:
                d = x.split()
                end = (int(d[1]),int(d[2]))
                d = end 
    dic = make_a_dictionary()
    info,connection = check_hub(dic["hub"])
    info["hub"] = {"name": "hub", "position": v, "zone": "first", "max_drones": dic["nb_drones"]}
    info["goal"] = {"name": "goal", "position": d, "zone": "normal", "max_drones": dic["nb_drones"]}
    grid = ft_info(info, start,end)
    path = dijikstra(connection,info,grid)
    return info,connection,path

main()
