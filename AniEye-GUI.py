import cv2
import tkinter as tk
from PIL import Image
from PIL import ImageTk

import src.dog_vision as dog
import src.bee_vision as bee
import src.fly_vision as fly
import src.cow_vision as cow
import src.cat_vision as cat
import src.shark_vision as shark
import src.horse_vision as horse
import src.bird_vision as bird

def convert(filter):
    image = filter(src)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    imgtk = ImageTk.PhotoImage(image=image)

    label = tk.Label(window, image=imgtk)
    label.image = imgtk
    label.grid(row=0, column=1, rowspan=9)

def make_button(text, row, col, fileName, filter):
    button = tk.Button(window, width=40, height=2, text=text, command=lambda: make_label(fileName, filter))
    button.grid(row=row, column=col)

def make_label(fileName, filter):
    global src
    src = cv2.imread(fileName)
    src = cv2.resize(src, (640, 360))
    img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    label = tk.Label(window, image=imgtk)
    label.image = imgtk
    label.grid(row=0, column=1, rowspan=9)
    button = tk.Button(window, width=20, text="See on AniEye", command=lambda: convert(filter))
    button.grid(row=8, column=0)

window=tk.Tk()
window.title("AniEye")
window.geometry("1100x500+100+100")

make_button("dog", 0, 0, "image/dog.png", dog.see)
make_button("bee", 1, 0, "image/bee.png", bee.see)
make_button("cow", 2, 0, "image/cow.png", cow.see)
make_button("fly", 3, 0, "image/fly.png", fly.see)
make_button("cat", 4, 0, "image/cat.jpg", cat.see)
make_button("shark", 5, 0, "image/underwater.jpg", shark.see)
make_button("horse", 6, 0, "image/horse.jpg", horse.see)
make_button("bird", 7, 0, "image/bird.png", bird.see)

window.mainloop()