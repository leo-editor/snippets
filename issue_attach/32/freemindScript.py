@language python
#Your currently selected node will be replaced with the outline you are importing.
#Replace the path with the path of your file:
    
file_path = 'D:/exmample/mymindmap.mm.html'

max_chars_in_header = 80 #Nodes with more characters than that (or with line jumps) will be inserted as bodies instead of as header.

#INSTRUCTIONS FOR EXPORTING FROM FREEMIND: Export your outline into html, then you can use this script.

import lxml.html

global outline_dict

outline_dict = {}

global count
count = 0

def element_to_node(parent_node, element ):
    global count
    global outline_dict
    count = count+1
    my_actual_count = int(count)

    if len(list(element.iterchildren())):
        # if len(list(list(element.iterchildren())[0].iterchildren())):

        outline_dict[str(my_actual_count)] = {}
        outline_dict[parent_node]['children'].append(str(my_actual_count))
        if len(list(list(element.iterchildren())[0].iterchildren())):
            outline_dict[str(my_actual_count)]['string'] = list(list(element.iterchildren())[0].iterchildren())[0].text
        else:
            outline_dict[str(my_actual_count)]['string'] = list(element.iterchildren())[0].text
        outline_dict[str(my_actual_count)]['children'] = list()
        if len(list(element.iterchildren()))>1:
            for child in list(element.iterchildren())[1].iterchildren():
                element_to_node(str(my_actual_count),child)

htmltree = lxml.html.parse(file_path)

root = htmltree.getroot()

body = root.findall('body')[0]
outline_dict[str(0)] = {}
outline_dict[str(0)]['children'] = list()
outline_dict[str(count)]['string'] = list(list(body.iterchildren())[0].iterchildren())[0].text
outline_dict[str(count)]['children'] = list()

for item in list(list(body.iterchildren())[1].iterchildren()):
    
    element_to_node(str(0), item )
    



#Up to here, the script was for importing into a dict. Now we export that dict into nodes:
    
def add_children_as_nodes(node_id_to_add, parent_id):

    global outline_dict
    if c.p.h == parent_id:
        my_parent = c.p.copy()
    else:
        for node in c.p.unique_subtree():
            if node.h == parent_id:
                my_parent = node.copy()

                
            
    newchild = my_parent.insertAsLastChild().copy()
    newchild.h = node_id_to_add
    newchild.b = outline_dict[node_id_to_add]['string']
    
    for child_id in outline_dict[node_id_to_add]['children']:
        add_children_as_nodes(child_id, node_id_to_add)
    

c.p.h = str(0)
c.p.b = outline_dict['0']['string']
for child_id in outline_dict['0']['children']:
    add_children_as_nodes(child_id, '0')

for p in c.p.unique_subtree():
    if len(p.b.splitlines())==1:
        if len(p.b.splitlines()[0])<max_chars_in_header:
            p.h = p.b.splitlines()[0]
            p.b = ""
        else:
            p.h = "@node_with_long_text"
    else:
        p.h = "@node_with_long_text"

if len(c.p.b.splitlines())==1:
    if len(c.p.b.splitlines()[0])<max_chars_in_header:
        c.p.h = c.p.b.splitlines()[0]
        c.p.b = ""
    else:
        c.p.h = "@node_with_long_text"
else:
    c.p.h = "@node_with_long_text"

c.redraw()