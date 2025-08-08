from math import sin, radians
from random import randint, choice
from PIL import Image
from PIL.ImageTk import PhotoImage
from tkinter import Tk, Canvas
from time import sleep

root = Tk()
canvas = Canvas(bg="#880000", highlightthickness=0)
root.attributes("-fullscreen", True)
root.config(cursor="none")
root.title("Pavilon slepic ze ZOO Liberec")  # ZOO Liberec reference
canvas.obecna_rychlost = 250
canvas.change = False

X = root.winfo_screenwidth() // 2
Y = root.winfo_screenheight() // 2

pocet_snimku = 32  # nebo taky počet možných rotací stopy
pocet_slepic = 16

class Slepice:
    def __init__(self):
        self.x = randint(50, X * 2 - 50)
        self.y = randint(50, Y * 2 - 50)
        self.smer = randint(0, pocet_snimku - 1)
        self.display = 5
        self.rychlost = randint(3, 7)
        self.cisla = []
    
    def update(self):  # pohne se, přidá 5 stop dopředu a smaže 1 stopu ze všech ostatních
        for _ in range(10):
            if self.x < 0 or self.y < 0 or self.x + 30 > X * 2 or self.y + 30 > Y * 2:
                self.smer += pocet_snimku // 2
            elif randint(1, 10) == 1:
                self.smer += randint(-pocet_snimku // 8, pocet_snimku // 8)
            self.smer = (self.smer) % pocet_snimku

            self.x += self.rychlost * sin(radians(self.smer * 360 / pocet_snimku))
            self.y += self.rychlost * -sin(radians(self.smer * 360 / pocet_snimku + 90))

        self.cisla.append([canvas.create_image(self.x, self.y, image=img[self.smer]) for _ in range(5)])
        for i in range(len(self.cisla) - 1):
            canvas.delete(self.cisla[i].pop())
        if len(self.cisla) == 6:
            self.cisla.pop(0)
        
canvas.slepice = [Slepice() for _ in range(pocet_slepic)]

img = [
    PhotoImage(Image.open("noha.png").rotate(360 - i * (360 / pocet_snimku)))  # obrázky nejdou generovat dynamicky po spuštění okna
    for i in range(pocet_snimku)
]

def move():
    for s in canvas.slepice:
        s.update()
    root.after(canvas.obecna_rychlost, move)

def bg_change():
    canvas.configure(background="#" + choice(("800","080","008","880","808","088","840","480","804","408","084","048")))
    if canvas.change:
        canvas.obecna_rychlost = randint(250, 500)
    canvas.change = not canvas.change
    root.after(5000, bg_change)

move()
bg_change()

canvas.pack(fill="both", expand=True)
root.mainloop()
