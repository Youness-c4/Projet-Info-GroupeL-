from pprint import pprint
from tkinter import *
from tkinter.ttk import Combobox
import json

# ----données json----
with open("data.json") as mon_fichier:
    data = json.load(mon_fichier)


# ----def command----
def restart():
    pass


def defocus(event):
    event.widget.master.focus_set()


# ---fenêtre de l'app----
window = Tk()
window.title("Qui est-ce ?")
window.geometry("720x480")
window.minsize(480, 360)
window.iconbitmap("logo.ico")
window.config(background='#599d8a')

# ----barre de menu de la fenêtre----
menu_bar = Menu(window)
# créer un premier menu
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Nouvelle partie", command=restart)
file_menu.add_command(label="Quitter", command=window.quit)
menu_bar.add_cascade(label="Fichier", menu=file_menu)
# configurer la fenêtre pour ajouter le menu
window.config(menu=menu_bar)

# ----partie interraction de l'app----
frame = Frame(window, bg='#599d8a')
# ajouter liste déroulante des critères
list_attr = []
for key, value in data["personnages"][0].items():
    if key != "fichier" and key != "prenom":
        list_attr.append(key)
list_combo = Combobox(frame, values=list_attr, state="readonly")
list_combo.current(0)
list_combo.bind("<FocusIn>", defocus)
list_combo.pack()
# ajouter frame
frame.pack(expand=YES)


# ----plateau de jeu----
class Board:
    def eliminate(self, widget):
        widget.configure(bg='#ff0000')
        self.dict_elimines[widget] = True
        print(self.dict_elimines)

    def __init__(self, rows, columns, cellwidth=0, cellheight=0, ):

        self.width = columns * cellwidth
        self.height = rows * cellheight

        board = Frame(window, bg='#599d8a')
        board.pack(expand=YES)

        self.images = [[PhotoImage()] * columns for i in range(rows)]
        self.buttons = [[Button()] * columns for i in range(rows)]
        self.dict_elimines = {}

        i = 0
        couleur_bg = StringVar()
        couleur_bg.set('#599d8a')

        for row in range(rows):
            for column in range(columns):
                self.images[row][column] = PhotoImage(file="personnages/" + data["personnages"][i]["fichier"])
                self.buttons[row][column] = Button(board, image=self.images[row][column], bg='#599d8a',
                                                   highlightthickness=10, relief=GROOVE, cursor="X_cursor")
                self.buttons[row][column].configure(command=lambda b=self.buttons[row][column]: self.eliminate(b))
                self.buttons[row][column].grid(row=row, column=column, sticky=N + S + E + W)
                self.dict_elimines[self.buttons[row][column]] = False
                i += 1


# ----afficher la fenêtre---
if __name__ == "__main__":
    bd = Board(int(data["ligne"]), int(data["colonne"]))
    window.mainloop()
