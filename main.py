import tkinter as tk
from tkinter import filedialog as tkfd
from PIL import Image
import pytesseract
import csv

window = tk.Tk()

img_path_jpg = tkfd.askopenfilename()
img_jpg = Image.open(img_path_jpg)

width = img_jpg.size[0]
height = img_jpg.size[1]
scale_factor = 5
scaled_width = round(width / scale_factor)
scaled_height = round(height / scale_factor)

img_path_png = "./temp.png"
resized_png = img_jpg.resize((scaled_width, scaled_height)).save(img_path_png, "png")

window.geometry(str(scaled_width) + "x" + str(scaled_height))
canvas = tk.Canvas(window, width=scaled_width, height=scaled_height)
background_image = tk.PhotoImage(file=img_path_png)
canvas.create_image(0, 0, image=background_image, anchor='nw')
canvas.pack()

selections = []
rectangles = []


def left_click(event):
    global rectangles
    coord = (event.x, event.y)
    selections.append(coord)
    if not len(selections) % 2:
        rectangles.append(
            canvas.create_rectangle(selections[-1][0], selections[-1][1], selections[-2][0], selections[-2][1]))
    return coord


def right_click(event):
    global rectangles
    if not len(selections) % 2:
        selections.pop()
        selections.pop()
        canvas.delete(rectangles.pop())
    else:
        selections.pop()


window.bind("<Button-1>", left_click)
window.bind("<Button-3>", right_click)
window.mainloop()



file = open("./output.csv", "a", newline='')
writer = csv.writer(file)

content = []


def checks_orientation(one, two):
    orientation = [[one[0], one[1]], [two[0], two[1]]]
    if one[0] > two[0]:
        orientation[0][0] = two[0]
        orientation[1][0] = one[0]
    if one[1] > two[1]:
        orientation[0][1] = two[1]
        orientation[1][1] = one[1]           
    return orientation

def scales_tuple(target):
    return tuple(scale_factor*coord for coord in target)


if len(selections) % 2:
    selections.pop()

for i in range(0, len(selections), 2):

    points = checks_orientation(selections[i], selections[i + 1])
    one = scales_tuple(points[0])
    two = scales_tuple(points[1])
    
    crop = img_jpg.crop((one[0], one[1], two[0], two[1]))
    ts_out = pytesseract.image_to_string(crop).strip()
    content.append(ts_out)
    crop.show()

writer.writerow(content)

file.close()


