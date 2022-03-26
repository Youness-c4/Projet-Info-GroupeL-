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

def gagne(dashb, gameb):
    dashb.interface.pack_forget()
    gameb.interface.pack_forget()
    l = Label(window, text="YOU WIN", bg='#4a8ecc')
    l.pack(expand=YES, padx=20, pady=20)


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
modefacile = BooleanVar()
modefacile.set(False)


# ----tableau de bord du joueur----
class Dashboard:
    def __init__(self, gameb):
        # attributs
        self.gameboard = gameb

        # Dashboard
        self.interface = Frame(window, bg='#4a8ecc')
        self.interface.pack(expand=YES, padx=20, pady=20)

        # label question
        l1 = Label(self.interface, text="Le personnage possède-t-il", bg='#4a8ecc')
        l1.grid(row=0, column=0, sticky=N + S + E + W)

        # liste déroulante question
        list_attr = []
        for key, value in data["personnages"][0].items():
            if key != "fichier" and key != "prenom":
                list_attr.append(key)
        list_combo = Combobox(self.interface, values=list_attr, state="readonly")
        list_combo.current(0)
        list_combo.bind("<FocusIn>", defocus)
        list_combo.grid(row=0, column=1, sticky=N + S + E + W)

        # bouton submit question
        button = Button(self.interface, text="CONFIRMER", bg='#4dbb69', borderwidth=1,
                        relief="raised", highlightthickness=0)
        button.configure(command=lambda: self.submitChoice(list_combo.get()))
        button.grid(row=0, column=2, padx=30)

        # label résultat question
        self.result_question = Label(self.interface, text="", bg='#4a8ecc')
        self.result_question.grid(row=0, column=3, sticky=N + S + E + W)

        # label selection personnage_quiestce
        l2 = Label(self.interface, text="Je pense que le personnage est", bg='#4a8ecc')
        l2.grid(row=1, column=0, sticky=N + S + E + W)

        # liste selection personnage_quiestce
        list_pers = []
        for elem in data["personnages"]:
            list_pers.append(elem["prenom"])
        list_combo2 = Combobox(self.interface, values=list_pers, state="readonly")
        list_combo2.current(0)
        list_combo2.bind("<FocusIn>", defocus)
        list_combo2.grid(row=1, column=1, sticky=N + S + E + W)

        # bouton submit selection perssonage_quiestce
        button2 = Button(self.interface, text="CONFIRMER", bg='#4dbb69', borderwidth=1,
                        relief="raised", highlightthickness=0)
        button2.configure(command=lambda: self.quiestceTrouve(list_combo2.get()))
        button2.grid(row=1, column=2, padx=30)

        # label résultat selection personnage_quiestce
        self.result_quiestce = Label(self.interface, text="", bg='#4a8ecc')
        self.result_quiestce.grid(row=1, column=3, sticky=N + S + E + W)

    def submitChoice(self, attribut):
        self.result_question.configure(text=self.gameboard.personnage_quiestce[attribut])
        if modefacile.get() == 1:
            for i in range(len(data['personnages'])):
                answer = data['personnages'][i][attribut]
                if answer != gameb.personnage_quiestce[attribut]:
                    self.gameboard.eliminate(data['personnages'][i]["prenom"])

    def quiestceTrouve(self, prenom):
        if self.gameboard.personnage_quiestce["prenom"] == prenom:
            gagne(self, self.gameboard)
        else:
            text = "NON"
            self.result_quiestce.configure(text=text)


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

    def disabledGameb(self):
        for x in self.personnages:
            if modefacile.get():
                self.personnages[x][1].configure(state=DISABLED)
            else:
                self.personnages[x][1].configure(state=NORMAL)


# ----afficher la fenêtre---
if __name__ == "__main__":
    # création Gameboard + Dashboard
    gameb = Gameboard(int(data["ligne"]), int(data["colonne"]))
    dashb = Dashboard(gameb)

    # mode facile
    modefacile_menu = Menu(menu_bar, tearoff=0)
    modefacile_menu.add_checkbutton(label="activer", onvalue=1, offvalue=0, variable=modefacile, command=gameb.disabledGameb)
    menu_bar.add_cascade(label="MODE FACILE", menu=modefacile_menu)

    print("je suis le personnage à trouver : " + gameb.personnage_quiestce["prenom"])

    # MAJ taille fenêtre
    window.update()
    w = window.winfo_reqwidth()
    h = window.winfo_reqheight()
    window.geometry(f"{w}x{h}")
    window.minsize(w, h)

    # ouvre la fenêtre
    window.mainloop()
