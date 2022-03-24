from tkinter import *
from tkinter.ttk import Combobox

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
window.title("Qui est-ce ?")
# window.iconbitmap("logo2.ico")
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

# ----variables globales----
modefacile = IntVar()

# ----palette de commandes du joueur----
class Paddle:
    def __init__(self, board):

        # attributs déclarations
        self.quiestce = board.quiestce
        self.brd = board

        # palette
        self.paddle = Frame(window, bg='#4a8ecc')
        self.paddle.pack(expand=YES, padx=20, pady=20)

        # ajout texte
        l1 = Label(self.paddle, text="Le personnage possède-t-il", bg='#4a8ecc')
        l1.grid(row=0, column=0, sticky=N + S + E + W)

        # ajouter liste déroulante des critères
        list_attr = []
        for key, value in data["personnages"][0].items():
            if key != "fichier" and key != "prenom":
                list_attr.append(key)
        list_combo = Combobox(self.paddle, values=list_attr, state="readonly")
        list_combo.current(0)
        list_combo.bind("<FocusIn>", defocus)
        list_combo.grid(row=0, column=1, sticky=N + S + E + W)

        # bouton submit
        button = Button(self.paddle, text="CONFIRMER", bg='#70d562', borderwidth=1,
                        relief="raised", highlightthickness=0)
        button.configure(command=lambda b=button: self.submitChoice(b, list_combo.get()))
        button.grid(row=0, column=2, padx=30)

        # label résultat
        self.result = Label(self.paddle, text="", bg='#4a8ecc')
        self.result.grid(row=0, column=3, padx=30)

        # bouton mode facile
        buttonfacile = Checkbutton(self.paddle, text="MODE FACILE", variable=modefacile, onvalue=1,
                                   offvalue=0, command=self.disabled_buttons)
        buttonfacile.grid(row=0, column=4, padx=30)


    def disabled_buttons(self):
        if modefacile.get()==1:
            for x in self.brd.personnages_board:
                self.brd.personnages_board[x][1].configure(state=DISABLED)
        else:
            for x in self.brd.personnages_board:
                self.brd.personnages_board[x][1].configure(state=NORMAL)
        print("le mode facile est à", modefacile.get())


    def submitChoice(self, widget, current):
        print(self.quiestce[current])
        self.result.configure(text=self.quiestce[current])
        if modefacile.get()==1:
            for i in range(len(data['personnages'])):
                answer = data['personnages'][i][current]
                if answer != self.quiestce[current]:
                    self.brd.eliminate(data['personnages'][i]["prenom"])



# def cross(self, number):

# file = data['images'] + perso["prenom"].lower()+"._cross.png"
# print(file)
# bg = '#D1007A'
# img = PhotoImage(file=file)
# widget.configure(bg=bg, image=img)
# self.personnages_board[widget][2] = img


# ----plateau de jeu----
class Board:
    def __init__(self, rows, columns):
        # plateau
        self.board = Frame(window, bg='#4a8ecc')
        self.board.pack(expand=YES, padx=20, pady=20)

        # attributs déclarations
        self.personnages_board = {}
        self.quiestce = ""

        # personnage qui-est-ce
        nb_rand = random.randint(0, rows * columns - 1)
        self.quiestce = data['personnages'][nb_rand]

        # initialisation plateau
        i = 0
        for row in range(rows):
            for column in range(columns):
                # boutons
                prenom = data["personnages"][i]["prenom"]
                image = PhotoImage(file=data['images'] + data["personnages"][i]["fichier"])
                button = Button(self.board, image=image, bg='#ffef00', border=10,
                                highlightthickness=0, relief="raised", cursor="X_cursor", highlightbackground="#4a8ecc",
                                highlightcolor="#4a8ecc")
                button.configure(command=lambda p=prenom: self.eliminate(p))
                button.grid(row=row, column=column, sticky=N + S + E + W, padx=10, pady=10)
                # dictionnaire
                self.personnages_board[prenom] = [False, button, data["personnages"][i], image]
                # incr
                i += 1

    def eliminate(self, prenom):
        # est éliminé
        if self.personnages_board[prenom][0]:
            if modefacile.get()==1:
                pass
            else:
                file = data['images'] + self.personnages_board[prenom][2]["prenom"].lower() + ".png"
                self.personnages_board[prenom][0] = False
                bg = '#ffef00'
                img = PhotoImage(file=file)
                widget = self.personnages_board[prenom][1]
                widget.configure(bg=bg, image=img)
                self.personnages_board[prenom][3] = img
        # pas éliminé
        else:
            file = data['images'] + self.personnages_board[prenom][2]["prenom"].lower() + "_cross.png"
            self.personnages_board[prenom][0] = True
            bg = '#D1007A'
            img = PhotoImage(file=file)
            widget = self.personnages_board[prenom][1]
            widget.configure(bg=bg, image=img)
            self.personnages_board[prenom][3] = img


# ----afficher la fenêtre---
if __name__ == "__main__":
    # création plateau + palette
    bd = Board(int(data["ligne"]), int(data["colonne"]))
    print("je suis le personnage à trouver : "+bd.quiestce["prenom"])
    pd = Paddle(bd)

    # MAJ taille fenêtre
    window.update()
    w = window.winfo_reqwidth()
    h = window.winfo_reqheight()
    window.geometry(f"{w}x{h}")
    window.minsize(w, h)

    # ouvre la fenêtre
    window.mainloop()
