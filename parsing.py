import re
def make_a_dictionary():
    dic = {}
    check_prefix = 0
    with open("configuration.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
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
        if start < 0:
            raise ValueError("Number must be positive")
        end = arg[2].strip().replace('"','')
        end = int(end)
        if start < 0:
            raise ValueError("Number must of be positive")
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
        
def check_validation():
    dic = make_a_dictionary()
    # for key, value in dic.items:
    if dic["prefix_v"][0] > 0:
        print(dic["prefix_v"][0])
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
    check_hub = check_hub()
    # print(arg[0])

check_validation()
































# this is for check all metadata



        # if arg[3]:
        #     all_arg.append(arg[3])
        #     if arg[4]:
        #         all_arg.append(arg[4])
        #         # if arg[5]:
        #         #     all_arg.append(arg[5])
        # print(all_arg)
        # if re.search("color",arg[3]):
        #     pass
            
        #     all_arg = str(all_arg).replace('[','',1).replace(']','',1)
        #     # last_index = len(all_arg) -1 
        #     print(all_arg)
        #     if all_arg[0] != "[" and "]" != all_arg[-1] or all_arg.count('[') > 1 or all_arg.count(']') > 1:
        #         raise ValueError("Please enter the form between [ ]")
        #     all_arg = str(all_arg).replace('[','',1).replace(']','',1)
        #     arg = all_arg.split(",")

        #     if "," in arg[3]:
        #         arg = arg[3].split(",")
        #         print(arg)
 
            # if len(arg) > 3:
            #     raise ValueError("more than 3 please enter one of : zone, color or max_drones")
            # for n in arg:
            #     argument = n.split("=")
            #     if len(argument) != 2:
            #         raise ValueError("Please enter the form like that  metadata = value")
            #     metadata = argument[0].lower()
            #     if metadata == "color" or metadata == "zone":
            #         value = argument[1].lower().replace("'",'').strip()
            #     else:
            #         value = argument[1].replace("'",'').strip()
            #     metadata = metadata.replace("'",'').strip()
            #     if metadata != "color" and metadata != "zone" and metadata != "max_drones":
            #         raise ValueError("Please enter one of this color or zone or max_drones")
            #     if metadata == "color" and value not in lst_color:
            #         raise ValueError("Please enter one of this colors green or yellow, red, blue, gray")
            #     if metadata == "zone" and value not in lst_zones:
            #         raise ValueError ("Please enter one of this zones restricted,normal,priority,blocked")
            #     if metadata == "max_drones":
            #         try:
            #             value = int(value)
            #             if value < 0:
            #                 print("Please enter a positive number")
            #         except ValueError:
            #             print("Error: Please enter a int value en max_drones")

        #     else:
        #         arg[3] = arg[0].split("=")
        #         if len(arg[3]) != 2:
        #             raise ValueError("Please enter the form like that  metadata = value")
        #         metadata = arg[3][0].lower()
        #         if metadata == "color" or metadata == "zone":
        #             value = arg[3][1].lower()
        #         else:
        #             value = arg[3][1]
        #         if metadata != "color" and metadata != "zone" and metadata != "max_drones":
        #             raise ValueError("Please enter one of this color or zone or max_drones")
        #         if metadata == "color" and value not in lst_color:
        #             raise ValueError("Please enter one of this colors green or yellow, red, blue, gray")
        #         if metadata == "zone" and value not in lst_zones:
        #             raise ValueError ("Please enter one of this zones restricted,normal,priority,blocked")
        #         if metadata == "max_drones":
        #             try:
        #                 value = int(value)
        #                 if value < 0:
        #                     print("Please enter a positive number")
        #             except ValueError:
        #                 print("Error: Please enter a int value en max_drones")

        # if len(arg) > 4:
        #     raise ValueError("The arg is more then 4")  

        