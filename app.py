from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image, ImageTk, ImageFilter

import random
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
window.title("Qui est-tu ?")
window.iconbitmap("logo2.ico")
window.config(background='#4a8ecc')

# ----barre de menu de la fenêtre----
menu_bar = Menu(window)
# créer un premier menu
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Nouvelle partie", command=restart)
file_menu.add_command(label="Quitter", command=window.quit)
menu_bar.add_cascade(label="Fichier", menu=file_menu)
# configurer la fenêtre pour ajouter le menu
window.config(menu=menu_bar)


# ----palette du joueur----
class Paddle:
    def __init__(self):
        # palette
        self.paddle = Frame(window, bg='#599d8a')
        self.paddle.pack(expand=YES, padx=20, pady=20)

        # ajouter liste déroulante des critères
        list_attr = []
        for key, value in data["personnages"][0].items():
            if key != "fichier" and key != "prenom":
                list_attr.append(key)
        list_combo = Combobox(self.paddle, values=list_attr, state="readonly")
        list_combo.current(0)
        list_combo.bind("<FocusIn>", defocus)
        list_combo.pack()


# ----plateau de jeu----
class Board:
    def __init__(self, rows, columns):
        # plateau
        self.board = Frame(window, bg='#003696')
        self.board.pack(expand=YES, padx=20, pady=20)

        # personnage qui-est-ce
        nb_rand = random.randint(0, rows * columns - 1)
        prenom = data['personnages'][nb_rand]['prenom']
        print(prenom)

        # attributs déclarations
        self.personnages_board = {}

        # initialisation plateau
        i = 0
        for row in range(rows):
            for column in range(columns):
                # boutons
                image = PhotoImage(file=data['images'] + data["personnages"][i]["fichier"])
                button = Button(self.board, image=image, bg='#003696',
                                                   highlightthickness=10, relief=GROOVE, cursor="X_cursor")
                button.configure(command=lambda b=button: self.eliminate(b))
                button.grid(row=row, column=column, sticky=N + S + E + W)
                # dictionnaire
                self.personnages_board[button] = [False, data["personnages"][i], image]
                # incr
                i += 1

    def eliminate(self, widget):
        if self.personnages_board[widget][0]:
            file = data['images'] + self.personnages_board[widget][1]["prenom"].lower()+".png"
            self.personnages_board[widget][0] = False
            bg = '#003696'
        else:
            file = data['images'] + self.personnages_board[widget][1]["prenom"].lower() + "_cross.png"
            self.personnages_board[widget][0] = True
            bg = '#D1007A'
        img = PhotoImage(file=file)
        widget.configure(bg=bg, image=img)
        self.personnages_board[widget][2] = img


# ----afficher la fenêtre---
if __name__ == "__main__":
    # création plateau + palette
    bd = Board(int(data["ligne"]), int(data["colonne"]))
    pd = Paddle()

    # MAJ taille fenêtre
    window.update()
    w = window.winfo_reqwidth()
    h = window.winfo_reqheight()
    window.geometry(f"{w}x{h}")
    window.minsize(w, h)

    # ouvre la fenêtre
    window.mainloop()
