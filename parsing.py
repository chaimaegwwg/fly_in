import re
import sys
def make_a_dictionary():
    dic = {}
    check_prefix = 0
    with open("configuration.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.split('#')[0].strip()
            if not line or ":" not in line:
                if ":" not in line and line:
                    check_prefix +=1
                continue
            key , value= line.split(":", 1)
            key = key.lower()
            #prefix    
            if key != "start_hub" and key != "end_hub" and key != "hub" and key != "connection" and key != "nb_drones":
                check_prefix += 1
            if key in dic:
                dic[key].append(value)
            else:
                dic[key] = [value]
    dic["prefix_v"] = [check_prefix]
    return dic
def check_connection(connection, names):
    dic = {}
    # n = 0
    try:
        for x in connection:
            x = x.strip().split("-")
            x[0] = x[0].strip()
            if x[0] not in names:
                raise ValueError("Invalid name")
            if x[1] not in names:
                if "[" not in x[1] and "]" not in x[1]:
                    raise ValueError("Entre the [ ]")
                c = x[1].count("]")
                c1 = x[1].count("[")
                if c1 != 1 or c != 1:
                    raise ValueError("Please check the [ ] if it correct")
                pairs = re.findall(r'(\w+)\s*=\s*(\w+)', x[1])
                if len(pairs[0]) != 2:
                    raise ValueError("enter like this the values max_link_capacity = value")
                max_name = pairs[0][0].strip()
                if max_name != "max_link_capacity":
                    raise ValueError("Invalid name [max_link_capacity=....] like that")
                value_max = pairs[0][1].strip()
                v = int(value_max)
                if v < 0:
                    raise ValueError("the value must be up than 0 (max_link_capacity)")
                second_name = x[1].split("[")
                x[1] = second_name[0].strip()
                if x[1] not in names:
                    raise ValueError("invalid second name")
                # dic[x[0]] = [x[1],v]
                dic.setdefault(x[0],[]).append([x[1],v])
                dic.setdefault(x[1],[]).append([x[0],v])
            else:
                if x[1] not in names:
                    raise ValueError("Invalid second name")
                # dic[x[0]] = [x[1]]
                dic.setdefault(x[0],[]).append([x[1],1])
                dic.setdefault(x[1],[]).append([x[0],1])
            # n+=1
    except ValueError as e:
        print("Error",e)
        return False    
    return dic




def check_start_end(start_hub):
    all_arg = []
    arg = start_hub.split()
    lst_color = ["green", "yellow", "red", "blue", "gray"]
    lst_zones = ["restricted","normal","priority","blocked"]
    try:
        name = arg[0].strip().replace('"','')
        if not name.isalpha():
            raise ValueError("please inter name as string :)")
        elif "-" in name:
            raise ValueError("Don't write dashes on the name is forbids :)")
        start = arg[1].strip().replace('"','')
        start = int(start)
        # if start < 0:
        #     raise ValueError("Number must be positive")
        end = arg[2].strip().replace('"','')
        end = int(end)
        # if start < 0:
        #     raise ValueError("Number must of be positive")
        if "[" not in start_hub and "]" not in start_hub or start_hub.count('[') > 1 or start_hub.count(']') > 1:
            raise ValueError("Please enter the form between [ ]")
        check = 0
        temp = ""
        for x in start_hub:
            if x =="[":
                check = 1
            elif x == "]":
                check = 0
            elif check:
                temp +=x
            
        temp = temp.split("=")
        if len(temp) != 2:
            raise ValueError("Please enter the form like that  metadata = value")
        if temp[0].lower().strip() == "color":
            value = temp[1].lower().strip()
            metadata = temp[0].lower().strip()
        else:
            raise ValueError("Please enter the color")
        if not isinstance(value, str) or not isinstance(metadata,str):
            raise ValueError("Enter the color and the value as string")
        if metadata == "color" and value not in lst_color:
            raise ValueError("Please enter one of this colors green or yellow, red, blue, gray")
        index = start_hub.find(']')
        if index != -1:
            for n in start_hub[index+1:]:
                raise ValueError("Stop there")

    except ValueError as e:
        print('\033[91m',"Error", e)
def check_hub(lines):
    dic = make_a_dictionary()
    the_same_name = []
    dic_info = {}
    
    for key in ["start_hub", "end_hub"]:
        if key in dic:
            for entry in dic[key]:
                the_same_name.append(entry.strip().split()[0])

    for line in lines:
        line = line.strip()
        if not line: continue
        
        try:
            parts = re.findall(r'[^ \[]+|\[[^\]]*\]', line)
            if len(parts) < 3:
                raise ValueError(f"Missing information in hub: {line}")

            name = parts[0].strip()
            if "-" in name: raise ValueError("Don't write dashes on the name :)")
            if name in the_same_name: raise ValueError("don't use the same name")
            the_same_name.append(name)

            hub_data = {
                "name": name,
                "position": (parts[1], parts[2]),
                "zone": "normal", "color": "none", "max_drones": 1
            }

            if len(parts) > 3 and "[" in parts[3]:
                meta_content = parts[3].strip("[]")

       
                if ":" in meta_content:
                    raise ValueError(f"Invalid character ':' in metadata: [{meta_content}]")
                
                pairs = re.findall(r'(\w+)\s*=\s*([\w-]+)', meta_content)

                if meta_content.count('=') != len(pairs):
                    raise ValueError(f"Metadata syntax error in: [{meta_content}]. Check your '=' usage.")
              

                for k, v in pairs:
                    k, v = k.lower().strip(), v.lower().strip()
                    if k == "zone":
                        if v not in ["priority", "normal", "blocked", "restricted"]:
                            raise ValueError("Invalid zone type")
                        hub_data["zone"] = v
                    elif k == "color":
                        hub_data["color"] = v
                    elif k == "max_drones":
                        v_int = int(v)
                        if v_int <= 0: raise ValueError("max_drones must be > 0")
                        hub_data["max_drones"] = v_int
            
            dic_info[name] = hub_data

        except ValueError as e:
            print("Error", e)
            return False

    connection = check_connection(dic["connection"], the_same_name)
    return (dic_info, connection) if connection else False
def check_validation():
    dic = make_a_dictionary()
    if dic["prefix_v"][0] > 0:
        print("Error")
    nb_drones = dic["nb_drones"][0]

    try:
        nb_drones = nb_drones.strip().replace('"','')
        nb_drones = int(nb_drones)
        if nb_drones < 0:
            raise ValueError("Number must of nb_drones be positive")
    except ValueError as e:
        print("Error", e)
    if len(dic["start_hub"]) > 1:
        print("You can't write start_hub more than one")
    if len(dic["nb_drones"]) > 1:
        print("You can't write nb_drones more than one")
    if len(dic["end_hub"]) > 1:
        print("You can't write end_hub more than one")

    start_hub = dic["start_hub"][0].strip()
    check_start_end(start_hub)
    end_hub = dic["end_hub"][0].strip()
    check_start_end(end_hub)
    info = check_hub(dic["hub"])
    if not info:
        return
    return nb_drones

check_validation()












# def check_hub(lines):
#     dic = make_a_dictionary()
#     the_same_name = []
#     dic_info = {}
#     for line in lines:
#         check = 0
#         c = 0
#         d = 0
#         zones = ["priority", "normal", "blocked","restricted"]
#         colors = ["green", "yellow","red", "blue","gray"]
#         try:
         
#             if "[" in line:
#                 if line.count("]") > 1 or line.count("[") > 1 or "]" not in line:
#                     raise ValueError("Please enter the form like that [   ] on hub") 
#                 line1, line2 = line.split("[")
#                 line = line1.split()
#                 line.append("["+line2)
#                 name = line[0]
#                 if not isinstance(name, str):
#                     raise ValueError("Please enter the name as string")
#                 if "-" in name:
#                     raise ValueError("Don't write dashes on the name is forbids :)")
#                 star_t = line[1]
#                 start = int(star_t)
#                 if not isinstance(start, int):
#                     raise ValueError("Please enter the start as int")
#                 en_d = line[2]
#                 end = int(en_d)
#                 if not isinstance(end, int):
#                     raise ValueError("Please enter the end as int")
#                 # print(line)
#                 # print(name)
#                 if name in the_same_name:
#                     raise ValueError("don't use the same name")
#                 the_same_name.append(name)
#                 if name not in dic_info:
#                     dic_info[name] = {}
#                 meta = str(line[3])
#                 # print(len(metadata))
#                 che_k = meta.split("=")
                
#                 chek = che_k[-1]
#                 chek = chek.split()
#                 for i in chek:
#                     if not i.isspace():
#                         if isinstance(i ,str) and i != "]":
#                             d = 1 
#                     if d == 1 and isinstance(i ,str) and (i != "]"):
#                         c += 1
#                 if c > 1:
#                     raise ValueError("don't do more than 2 value")
                
                
#                 # print(name)
#                 dic_info[name]["name"] = name
#                 dic_info[name]["position"] =(star_t, en_d)
#                 if len(meta.split("=")) == 2:
#                     metadata = meta.split("=")
#                     value = metadata[1].strip()
#                     metadata = metadata[0].strip()
#                     if metadata != "zone" and  metadata !="color" and metadata !="max_drones":
#                         raise ValueError("Please enter one of this value zone or color or max_drones")
#                     if metadata == "zone":
#                         if value not in zones:
#                             raise ValueError("Please enter one of this zone priority, normal, blocked, restricted")
#                     if metadata == "color":
#                             if value not in colors:
#                                 raise ValueError("Please enter one of this colors : green , yellow, red , blue, gray")
#                     if metadata == "max_drones":
#                         value = int(value)
#                         if value <= 0:
#                             raise ValueError("Please the value must be up to the 0")
#                     dic_info[name][metadata] = value


#                 if len(meta.split("=")) == 3:
#                     metadata = meta
#                     metadata = metadata.strip().replace("[", "").replace("]", "")
#                     pairs = re.findall(r'(\w+)\s*=\s*(\w+)', metadata)
#                     for x in pairs:
#                         metadata = x[0].strip()
#                         value = x[1].strip()
#                         if metadata != "zone" and  metadata !="color" and metadata !="max_drones":
#                             raise ValueError("Please enter one of this value zone or color or max_drones")
#                         if metadata == "zone":
#                             if value not in zones:
#                                 raise ValueError("Please enter one of this zone priority, normal, blocked, restricted")
#                         if metadata == "color":
#                             if value not in colors:
#                                 raise ValueError("Please enter one of this colors : green , yellow, red , blue, gray")
#                         if metadata == "max_drones":
#                             mvalue = int(value)
#                             if mvalue <= 0:
#                                 raise ValueError("Please the value must be up to the 0")
#                         dic_info[name][metadata] = value
#                     if len(pairs) !=2:
#                         raise ValueError("don't take the value empty")
#                 if len(meta.split("=")) == 4:
#                     metadata = meta
#                     metadata = metadata.strip().replace("[", "").replace("]", "")
#                     pairs = re.findall(r'(\w+)\s*=\s*(\w+)', metadata)
#                     for x in pairs:
#                         metadata = x[0].strip()
#                         value = x[1].strip()
#                         if metadata != "zone" and  metadata !="color" and metadata !="max_drones":
#                             raise ValueError("Please enter one of this value zone or color or max_drones")
#                         if metadata == "zone":
#                             if value not in zones:
#                                 raise ValueError("Please enter one of this zones : priority, normal, blocked, restricted")
#                         if metadata == "color":
#                             if value not in colors:
#                                 raise ValueError("Please enter one of this colors : green , yellow, red , blue, gray")
#                         if metadata == "max_drones":
#                             mvalue = int(value)
#                             if mvalue <= 0:
#                                 raise ValueError("Please the value must be up to the 0")
                            
#                         dic_info[name][metadata] = value 
#                     if len(pairs) != 3:
#                             raise ValueError("don't take the value empty")
#                 line = " ".join(line)
#                 if line.count("]") > 1:
#                     raise ValueError("you need to enter the form of meta like that [...]")
#                 for x in line:
#                     if x == "]":
#                         check = 1
#                     if check == 1 and x == "]" :
#                         continue
#                     if(x and check) and not x.isspace():
#                         raise ValueError("please don't write after ]")    
#             else:
#                 name = line
#                 if not isinstance(name, str):
#                     raise ValueError("Please enter the name as string")
#                 if "-" in name:
#                     raise ValueError("Don't write dashes on the name is forbids :)")
#                 start = line[1]
#                 start = int(start)
#                 if not isinstance(start, int):
#                     raise ValueError("Please enter the start as int")
#                 end = line[2]
#                 end = int(end)
#                 if not isinstance(end, int):
#                     raise ValueError("Please enter the end as int")
#                 #this i don't need this check
  
#         except ValueError as e:
#             print("Error", e)
#             return False
#     the_same_name.extend(["hub","goal"])
#     connection = check_connection(dic["connection"],the_same_name)
#     if not connection:
#         sys.exit()
#         return False
#     return dic_info,connection
    
#zone=restricted color=red 