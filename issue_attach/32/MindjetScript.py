#Your currently selected node will be replaced with the outline you are importing.
#Replace the path with the path of your file:

file_path = 'D:/exmample/mymindmap.csv'

max_chars_in_header = 80 #Nodes with more characters than that (or with line jumps) will be inserted as bodies instead of as header.

#INSTRUCTIONS FOR EXPORTING FROM MINDJET: You need a csv file exported from MindJet. When exporting, make sure you:
# - Use the layout "outline"
# - Tick all the options but "inlcude topic properties"


import csv

def get_row_level(row):
    count = 0
    while count<=len(row):
        if row[count]:
            return count+1
        else:
            count = count+1
    return -1

def get_row_string(row):
    count = 0
    while count<=len(row):
        if row[count]:
            return row[count]
        else:
            count = count+1
    return None

f = open(file_path)

reader = csv.reader(f)
f.close()
initial_level = c.p.level()
last_created_level = c.p.level()
last_created_node = c.p.copy()


for row in list(reader)[1:]:
    new_level = get_row_level(row) + initial_level
    get_row_string(row)
    if new_level > last_created_level:
        last_created_node = last_created_node.insertAsLastChild().copy()
        last_created_node.b = get_row_string(row)
        last_created_level = last_created_level+1
    elif new_level == last_created_level:
        last_created_node = last_created_node.insertAfter().copy()
        last_created_node.b = get_row_string(row)
    elif new_level < last_created_level:
            
        for item in last_created_node.parents():
            if item.level() == new_level-1:
                last_created_node = item.copy()
                break

        last_created_node = last_created_node.insertAsLastChild().copy()
        last_created_node.b = get_row_string(row)
        last_created_level = last_created_node.level()
        
for p in c.p.unique_subtree():
    if len(p.b.splitlines())==1:
        if len(p.b.splitlines()[0])<max_chars_in_header:
            p.h = p.b.splitlines()[0]
            p.b = ""
        else:
            p.h = "@node_with_long_text"
    else:
        p.h = "@node_with_long_text"

c.redraw()