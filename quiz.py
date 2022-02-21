from email.policy import default
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageFont, ImageDraw
import time
import json
import random
import os
import matplotlib as mpl
import matplotlib.pyplot as plt

if "guesses" not in os.listdir():
    os.mkdir("guesses")

if len(os.listdir("guesses")):
    data = input("Data found in guesses folder, delete? (y/N): ")
    if data[0].lower() == "y":
        for item in os.listdir("guesses"):
            os.remove("guesses/{}".format(item))

idx = -1
correct = 0

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

pokemon_files = os.listdir("art/")
pokemon_files.sort()
pokemon_files = pokemon_files[start-1:end] # cull requested start and end dex numbers
random.shuffle(pokemon_files) # shuffle pokemon


stats = {"order": pokemon_files, "guesses": {}}
fnt = ImageFont.truetype("pokemon_fire_red.ttf", size=96) 

def check_dex(num):
    if isinstance(num, str):
        num = num[:3]
    return pokemon_list[int(num)-1]


def display_image():
    canvas.delete("all")
    global img
    img = ImageTk.PhotoImage(Image.open("art/" + pokemon_files[idx]))
    canvas.create_image(0, 0, anchor=NW, image=img)
    canvas.create_text(5, 0, anchor=NW, text="{}/{}".format(idx+1, len(pokemon_files)))
    try:
        canvas.create_text(5, 10, anchor=NW, text="{:.2f}% correct".format((correct / idx)*100))
    except ZeroDivisionError:
        pass

def next_image(event): # TODO: add proper handling for end of list
    global idx
    global correct
    global stats
    global prev_time
    try:
        if idx == -1:
            idx += 1
            display_image()
            e.delete(0, "end")
            prev_time = time.time()
        elif idx + 1 <= len(pokemon_files):
            # check guess
            guess = e.get()
            if guess.lower() != check_dex(pokemon_files[idx]).lower():
                # print("Guessed {}: correct answer was {}".format(guess, check_dex(pokemon_files[idx])))
                wrong_answer(guess)
                stats["guesses"][pokemon_files[idx]] = {"correct": False, "guess": guess}
            else:
                correct += 1
                stats["guesses"][pokemon_files[idx]] = {"correct": True,  "guess": guess}
            stats["guesses"][pokemon_files[idx]]["time"] = time.time() - prev_time
            idx += 1
            display_image()
            e.delete(0, "end")
            prev_time = time.time()
    except IndexError:
        end_of_quiz()

# if answer is wrong generate image
def wrong_answer(guess):
    img_in = Image.open("art/{}".format(pokemon_files[idx]))
    img_out = Image.new("RGB", (475, 575), (255,255,255))
    img_out.paste(img_in, (0,100,475,575), img_in)
    t = ImageDraw.Draw(img_out)
    width = t.textbbox((0,0), guess.upper(), font=fnt)[2] # centering
    t.text((((475 - width)//2),0), font=fnt, text=guess.upper(), fill=(0,0,0))
    img_out.save("guesses/{}".format(pokemon_files[idx]))

def end_of_quiz(): # TODO make this display stats
    # pass
    root.destroy()
    x_ax = []
    for x in stats["order"]:
        x_ax.append(int(x[:3]))
    x_ax.sort()
    y_ax = []
    c_ax = []
    for y in x_ax:
        y_ax.append(stats["guesses"]["{:03d}.png".format(y)]["time"])
        if stats["guesses"]["{:03d}.png".format(y)]["correct"]:
            c_ax.append("tab:blue")
        else:
            c_ax.append("tab:red")
    plt.axis([min(x_ax)-1,max(x_ax)+1,0,max(y_ax)])
    plt.bar(x_ax, height=y_ax, color=c_ax)
    plt.xlabel("Dex number")
    plt.ylabel("Time taken to guess (seconds)")
    plt.show()

    

root = Tk()
canvas = Canvas(root, width=475, height=475)
canvas.pack(expand=YES)
e = Entry(root, font=100)
e.pack()

# initial setup
# img = ImageTk.PhotoImage(Image.open("art/" + pokemon_files[idx]))
img = ImageTk.PhotoImage(Image.open("start_photo.png"))
canvas.create_image(0, 0, anchor=NW, image=img)
canvas.create_text(20, 0, anchor=NW, text="{}/{}".format(idx+1, len(pokemon_files)))

# upon completion display stats such as percentage correct, time taken

root.bind("<Return>", next_image)

start_time = time.time()
prev_time = time.time()
root.mainloop()
# print(stats)\

# save to json file
fp = open ("stats.json", "w")
json.dump(stats, fp, indent=4)
