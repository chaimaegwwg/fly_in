from parsing import make_a_dictionary
import re
#parsing hub is the first because i will need here info
#mission is make 2 array and display the place 
#mission tomorrow is for make sure for parsing also add attribuite like the cost 
#mission make sure u understand the dijikstra and do it 
# the finale parsing for the part of connection

class Cell:
    def __init__(self,zone,visit):
        pass

def make_arr(position,end)-> list:
    inside_lst = []
    extra_lst = []
    row, col = end
    for row in range(row):
        for col in range(col):
            Ce
    

def main():
    dic = make_a_dictionary()
    position = []
    lst_position = []
    for key, value in dic.items():
        if key.strip() == "hub":
            key = key.strip()
            # v = value.split()
            for x in value:
                v = x.split()
                position.append((key,(int(v[1]),int(v[2]))))
        if key.strip() == "end_hub":
            for x in value:
                v = x.split()
                end = (int(v[1]),int(v[2]))
    print(end)
    make_arr(position, end)


main()
