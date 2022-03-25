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


# ----tableau de bord du joueur----
class Dashboard:
    def __init__(self, gameb):
        # attributs déclarations
        self.gameboard = gameb

        # palette
        self.interface = Frame(window, bg='#4a8ecc')
        self.interface.pack(expand=YES, padx=20, pady=20)

        # ajout texte
        l1 = Label(self.interface, text="Le personnage possède-t-il", bg='#4a8ecc')
        l1.grid(row=0, column=0, sticky=N + S + E + W)

        # ajouter liste déroulante des critères
        list_attr = []
        for key, value in data["personnages"][0].items():
            if key != "fichier" and key != "prenom":
                list_attr.append(key)
        list_combo = Combobox(self.interface, values=list_attr, state="readonly")
        list_combo.current(0)
        list_combo.bind("<FocusIn>", defocus)
        list_combo.grid(row=0, column=1, sticky=N + S + E + W)

        # bouton submit
        button = Button(self.interface, text="CONFIRMER", bg='#70d562', borderwidth=1,
                        relief="raised", highlightthickness=0)
        #button.configure(command=lambda b=button: self.submitChoice(b, list_combo.get()))
        button.configure(command=lambda: self.submitChoice(list_combo.get()))
        button.grid(row=0, column=2, padx=30)

        # label résultat
        self.result = Label(self.interface, text="", bg='#4a8ecc')
        self.result.grid(row=0, column=3, padx=30)

        # bouton mode facile
        checkbtn_facile = Checkbutton(self.interface, text="MODE FACILE", variable=modefacile, onvalue=1,
                                   offvalue=0, command=self.disabled_buttons)
        checkbtn_facile.grid(row=0, column=4, padx=30)

    def disabled_buttons(self):
        for x in self.gameboard.personnages:
            if modefacile.get() == 1:
                self.gameboard.personnages[x][1].configure(state=DISABLED)
            else:
                self.gameboard.personnages[x][1].configure(state=NORMAL)
        print("le mode facile est à", modefacile.get())

    def submitChoice(self, current):
        print(gameb.personnage_quiestce[current])
        self.result.configure(text=gameb.personnage_quiestce[current])
        if modefacile.get() == 1:
            for i in range(len(data['personnages'])):
                answer = data['personnages'][i][current]
                if answer != gameb.personnage_quiestce[current]:
                    self.gameboard.eliminate(data['personnages'][i]["prenom"])


# ----plateau de jeu----
class Gameboard:
    def __init__(self, rows, columns):
        # plateau
        self.interface = Frame(window, bg='#4a8ecc')
        self.interface.pack(expand=YES, padx=20, pady=20)

        # attributs déclarations
        nb_rand = random.randint(0, rows * columns - 1)
        self.personnage_quiestce = data['personnages'][nb_rand]
        self.personnages = {}

        # initialisation plateau
        i = 0
        for row in range(rows):
            for column in range(columns):
                # boutons
                prenom = data["personnages"][i]["prenom"]
                image = PhotoImage(file=data['images'] + data["personnages"][i]["fichier"])
                button = Button(self.interface, image=image, bg='#ffef00', border=10,
                                highlightthickness=0, relief="raised", cursor="X_cursor", highlightbackground="#4a8ecc",
                                highlightcolor="#4a8ecc")
                button.configure(command=lambda p=prenom: self.eliminate(p))
                button.grid(row=row, column=column, sticky=N + S + E + W, padx=10, pady=10)
                # dictionnaire
                self.personnages[prenom] = [False, button, data["personnages"][i], image]
                # incr
                i += 1

    def eliminate(self, prenom):
        elimine = self.personnages[prenom][0]
        file = data['images'] + self.personnages[prenom][2]["prenom"].lower()
        if (elimine and modefacile.get() == 0) or (not elimine):
            self.personnages[prenom][0] = not elimine
            if not elimine:
                file += "_cross.png"
                bg = '#D1007A'
            else:
                file += ".png"
                bg = '#ffef00'
            img = PhotoImage(file=file)
            widget = self.personnages[prenom][1]
            widget.configure(bg=bg, image=img)
            self.personnages[prenom][3] = img


# ----afficher la fenêtre---
if __name__ == "__main__":
    # création Gameboard + Dashboard
    gameb = Gameboard(int(data["ligne"]), int(data["colonne"]))
    dashb = Dashboard(gameb)

    print("je suis le personnage à trouver : " + gameb.personnage_quiestce["prenom"])

    # MAJ taille fenêtre
    window.update()
    w = window.winfo_reqwidth()
    h = window.winfo_reqheight()
    window.geometry(f"{w}x{h}")
    window.minsize(w, h)

    # ouvre la fenêtre
    window.mainloop()
