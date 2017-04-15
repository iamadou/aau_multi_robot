#!/usr/bin/python
import fileinput
import rospkg
import os

rospack = rospkg.RosPack()
package_path = rospack.get_path("map_merger")
print package_path
map_merger_file = "mapmerger.cpp"
folder = "src"
map_merger_path = os.path.join(package_path, folder, map_merger_file)

i = 0
found = False
count_curly = 0
LEVEL = "ERROR"
for line in fileinput.FileInput(map_merger_path,inplace=1):
    if "{" in line:
        count_curly = count_curly + 1
        
    if "}" in line:
        count_curly = count_curly - 1
        if count_curly == 0:
            line=line.replace(line,"\tROS_" + LEVEL + "(\"end " + str(i) + "\");\n}\n")      

    if found == True:
        i = i+1
        line=line.replace(line,"{\n\tROS_" + LEVEL + "(\"" + str(i) + "\");\n")
        
        found = False
    elif "MapMerger::" in line:
        if "&" not in line:
            if "{" in line:
                i = i+1
                line=line.replace(line,line+"{\n\tROS_" + LEVEL + "(\"" + str(i) + "\");\n")
            else:
                found = True
                

    if "return" in line:
        line=line.replace(line,"\t{ROS_" + LEVEL + "(\"end " + str(i) + "\");\n\t"+line+"}")
        count_curly=count_curly+2
    print line,
