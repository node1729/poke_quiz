from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import time
import json
import random
import os
# import matplotlib as mpl
# import matplotlib.pyplot as plt

pokemon_list = open("poke_list.json")
pokemon_list = json.load(pokemon_list)
pokemon_list = pokemon_list["data"]

print("Pokemon Generation numbers:\nGen 1 [1,151]\nGen 2 [152,251]\nGen 3 [252,386]\nGen 4 [387,493]\nGen 5 [494,649]\nGen 6 [650,721]\nGen 7 [722,809]\nGen 8 [810,905]")
passed = False
while not passed:
    try:
        start = int(input("Input starting dex number: "))
        end = int(input("Input ending dex number: "))
        passed = True
        if start > end:
            print("starting number cannot be greater than ending number")
            passed = False
        if start < 1:
            print("starting number must be at least 1")
            passed = False
        if end > 905:
            print("ending number must be at most 905")
            passed = False
    except ValueError:
        print("Input must be a number")
        pass


if "prefs-{:03d}-{:03d}.json".format(start, end) not in os.listdir():
    poke_included = {}
    for i in range(start, end + 1):
        poke_included["{:03d}".format(i)] = 0
    prefs = open("prefs-{:03d}-{:03d}.json".format(start, end), "w")
    json.dump({"included": poke_included, "matchups": []}, prefs)
    prefs.close()
prefs = open("prefs-{:03d}-{:03d}.json".format(start, end))
prefs = json.load(prefs)

pokemon_files = os.listdir("art/")
pokemon_files.sort()
pokemon_files = pokemon_files[start-1:end] # cull requested start and end dex numbers
random.shuffle(pokemon_files) # shuffle pokemon


def display_image():
    global img_l, img_r,left_pokemon, right_pokemon

    # pokemon that are significantly behind in matchups will get prioritized
    if (max(prefs["included"].values()) - min(prefs["included"].values())) > 2:
        # print("min max rescuing?")
        min_count = min(prefs["included"].values())
        temp_list = []
        for item in prefs["included"]:
            if prefs["included"][item] == min_count:
                temp_list.append(item)
        left_pokemon = random.choice(temp_list) + ".png"
        right_pokemon = random.choice(temp_list) + ".png"
        while right_pokemon == left_pokemon:
            right_pokemon = random.choice(temp_list) + ".png"
            if len(temp_list) == 1:
                right_pokemon = random.choice(pokemon_files)
    else:
        left_pokemon = random.choice(pokemon_files)
        right_pokemon = random.choice(pokemon_files)
    while right_pokemon == left_pokemon:
        right_pokemon = random.choice(pokemon_files)
    img_l = ImageTk.PhotoImage(Image.open("art/" + left_pokemon))
    img_r = ImageTk.PhotoImage(Image.open("art/"+ right_pokemon))
    canvas.create_image(0, 0, anchor=NW, image=img_l)
    canvas.create_image(475, 0, anchor=NW, image=img_r)

def next_image(event): 
    if event.x < 475:
        prefs["matchups"].append([left_pokemon[:3], right_pokemon[:3], 0])
    else:
        prefs["matchups"].append([left_pokemon[:3], right_pokemon[:3], 1])
    prefs["included"][left_pokemon[:3]] += 1
    prefs["included"][right_pokemon[:3]] += 1
    display_image()


root = Tk()
canvas = Canvas(root, width=950, height=475)
canvas.pack(expand=YES)

left_pokemon = random.choice(pokemon_files)
right_pokemon = random.choice(pokemon_files)
while right_pokemon == left_pokemon:
    right_pokemon = random.choice(pokemon_files)

img_l = ImageTk.PhotoImage(Image.open("art/" + left_pokemon))
img_r = ImageTk.PhotoImage(Image.open("art/"+ right_pokemon))

canvas.create_image(0, 0, anchor=NW, image=img_l)
canvas.create_image(475, 0, anchor=NW, image=img_r)

root.bind("<Button-1>", next_image)

start_time = time.time()
prev_time = time.time()
root.mainloop()
# print(stats)

# save to json file
fp = open ("prefs-{:03d}-{:03d}.json".format(start, end), "w")
json.dump(prefs, fp)
