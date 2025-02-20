import subprocess
from tkinter import Tk


def eog_display(path):
    # print("display")
    # subprocess.run(["C:/msys/mingw64/bin/eog.exe", path])
    subprocess.run(["eog", path])
    # print("/display")


def tk_display(path):
    import tkinter
    root = Tk()
    canvas = tkinter.Canvas(root, width=1280, height=720)
    canvas.pack()
    photo_img = tkinter.PhotoImage(file=path)
    canvas.create_image(20, 20, anchor=tkinter.NW, image=photo_img)
    tkinter.mainloop()
