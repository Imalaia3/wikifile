#!/usr/bin/env python
"""
WIKIFILE (wf) FORMAT READER/DECODER.

@author:imalaia3
python ver: 3
THIS FALLS UNDER THE GNU LGPL LICENCE

(c) Imalaia3 2022-
"""
import base64 #why not make life a little easier ;)
import os
import html
import sys
try:
    file = sys.argv[1]
except IndexError as e:
    print("You didn't include the filename of the input!")
    print("exiting")
    exit()

file = open(file,"r")
lines = file.readlines()
linel = len(lines)

INFO = {
    "lines":0,
    "writers":[],
    "has_images":False,
    "images":[],
    "title":"",
    "short_desc":"",
    "comp":"",
    #REMOVED: "server":""
    "mail":"",
    "footer_msg":""
}
TEXT = {
}
IMAGE = {
}
ALIASES = {}

def argparse(string,deln=False):
    total = string
    total = total.split(",")
    out = []
    for c,arg in enumerate(total):
        if '"' in arg:
            if deln:
                if arg.count('"') == 1 and c != len(total)-1:
                    out.append(str(arg).replace('"',"")+str(total[c+1]).replace('"',""))
                else:
                    out.append(str(arg).replace('"',""))
            else:
                if arg.count('"') == 1 and c != len(total)-1:
                    out.append(str(arg).replace('"',"")+str(total[c+1]).replace('"',""))
                else:
                    out.append(str(arg).replace('"',""))
                
            continue
        if arg.isnumeric():
            out.append(int(arg))
            continue
        #Might add list support but this is turning into a json implementation lol
    
    return out

#--Text Block Vars--#
text_begin = False
curr_tb = None
#--Image Block vars--#
img_begin = False
curr_ib = None
for line in lines:
    token = line[0:7]
    contents = line[7::]
    
    if token == "T_TEXTS":
        curr_tb = None
        text_begin = False
        print("TEXT END")
        continue
    elif text_begin:
        TEXT[curr_tb] = TEXT[curr_tb] + line
        print("Line is in textblock. Ignoring...")
        continue
    elif token == "T_IMGEN":
        print("IMAGE END")
        curr_ib = None
        img_begin = False
        continue
    elif img_begin:    
        IMAGE[curr_ib] = IMAGE[curr_ib] + line
        print("Line is in image. Ignoring...")
        continue

    elif token == "T_WIKII":
        things = argparse(contents)
        INFO["title"] = things[0]
        INFO["short_desc"] = things[2]
        #TODO: Add 'other' arg
        continue
    elif token == "T_LSWRI":
        things = argparse(contents,True)
        INFO["writers"] = things
        continue
    elif token == "T_TEXTB":
        text_begin = True
        curr_tb = argparse(contents,True)[0]
        TEXT[curr_tb] = ""
        continue
    elif token == "T_HEADI":
        things = argparse(contents,True)
        INFO["comp"] = things[0]
        INFO["mail"] = things[1]
        INFO["footer_msg"] = things[2]
        #INFO["fake_size"] = things[3] //Not implemented. Will probably be added in the web transfer code
        #^^^ Basically it gives the comblete wiki size in bits, and sice this is a string based format, we
        #can catch many corruptions because some characters are different sizes than others.
        continue
    elif token == "T_IMREF":
        things = argparse(contents,True)
        ALIASES[things[0].strip("\n")] = things[1]
        
    elif token == "T_IMAGE":
        things = argparse(contents,True)
        curr_ib = things[0].strip("\n")
        img_begin = True
        IMAGE[curr_ib] = ""
        continue


    elif token == "T_ENDIN":
        print("Parsing END.")
        break
    else:
        print("unknown token:",token,"(non-critical)")

   



#print(argparse('"This is a string",23,"also a str1ng"'))

"""
print("-= Useful Data =-")
print("Wikifile has",len(IMAGE),"images and", len(TEXT), "text blocks.")


print("TITLE:", INFO["title"])
print("By:", INFO["writers"])
print("\nDescription:",INFO["short_desc"])

for key in TEXT:
    print('\033[1m',key,"\033[0m")
    print("\n")
    print(TEXT[key])
    print("\n\n")

print("Contact:", INFO["mail"], INFO["footer_msg"])
print()
print()
print()
imgdata = base64.b64decode(IMAGE['joe'])
filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
with open(filename, 'wb') as f:
    f.write(imgdata)"""

print("Wikifile has",len(IMAGE),"images and", len(TEXT), "text blocks.")

for alias in IMAGE:
    html.BareRender.build_image(alias,IMAGE[alias])
    pass
renderer = html.Render()
renderer.render_title(INFO["title"])
renderer.render_writers(INFO["writers"])
#v1 = "\nDescription: "+INFO["short_desc"] Reserved
if len(ALIASES) == 0:
    for t in TEXT:
        
        renderer.render_textblock(t,TEXT[t])

for a in ALIASES:
    v = ALIASES[a]
    
    renderer.render_textblock(v,TEXT[v],a)
"""for key in TEXT:
    renderer.render_textblock(key,TEXT[key])"""
for alias in IMAGE:
    
    renderer.render_image(alias)

try:
    outp=sys.argv[2]
except IndexError as e:
    print("You didn't include the filename of the output!")
    print("exiting")
    exit()

with open(outp,"w") as f:
    print("Trying to write to file '{}'...".format(outp))
    f.write(renderer.out())
    print("Write OK.")
