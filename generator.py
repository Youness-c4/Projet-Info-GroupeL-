import json
import pprint
import string
from random import randint
from tkinter import *


# génération aléatoire d'un prénom de garçon et de fille
def generate_name_fille(entry):
    read_json = "prenoms_filles.json"
    with open(read_json, "r") as json_file:
        data = json.load(json_file)
        for x in range(randint(1, 5862)):
            fille = data[x]["prenom"]
        pprint.pprint(fille)
    entry.delete(0, END)
    entry.insert(0, fille)


def generate_name_garcon(entry):
    read_json = "prenoms_garcons.json"
    with open(read_json, "r") as json_file:
        data = json.load(json_file)
        for x in range(randint(1, 6528)):
            garcon = data[x]["prenom"]
        pprint.pprint(garcon)
    entry.delete(0, END)
    entry.insert(0, garcon)


def addToAttributes(var, res, label):
    var.set(res)
    label.configure(text=label.cget("text") + " " + var.get())
    affichageFrames(list_frames)


def affichageFrames(list_frames):
    global COUNT
    if COUNT < NBR_ATTRIBUTS - 1:
        list_frames[COUNT].grid_forget()
        list_frames[COUNT + 1].grid()
        COUNT += 1
    else:
        list_frames[COUNT].grid_forget()


def creer_fichier():
    ligne = 0
    colonne = 8
    for i in range(len(list_personnages_crees)):
        if i % colonne == 0 and i != len(list_personnages_crees) - 1:
            ligne += 1
    donnees['ligne'] = ligne
    donnees['colonne'] = colonne
    donnees['personnages'] = list_personnages_crees
    print(donnees)
    nbr_fichiers_crees.set(nbr_fichiers_crees.get() + 1)
    with open("génération" + str(nbr_fichiers_crees.get()) + ".json", "w") as file:
        json.dump(donnees, file)


# fonction générateur de frames pour attributs
def sousFrame(title, list_result, bool_input, var_control, label_to_complete):
    frame = Frame(frame_1, bg='#4a8ecc', bd=1)

    label = Label(frame, text=title + " :", font=("Courrier", 15), bg='#4a8ecc', fg="black")
    label.grid(row=0, sticky=W, pady=(0, 25))

    list_buttons = []
    cpt_col = 0
    for result in list_result:
        button = Button(frame, text=result, borderwidth=1, height=1, width=8, relief="raised", highlightthickness=0)
        button.configure(command=lambda b=button: addToAttributes(var_control, b['text'], label_to_complete))
        button.grid(row=2, column=cpt_col)
        list_buttons.append(button)
        cpt_col += 1

    if bool_input:
        entry = Entry(frame, justify=CENTER)
        entry.grid(row=1, column=0)
        button_entry = Button(frame, text="Entrer", borderwidth=1, height=1, width=8,
                              relief="raised", highlightthickness=0)
        button_entry.configure(command=lambda: addToAttributes(var_control, entry.get(), label_to_complete))
        button_entry.grid(row=1, column=1)

        if var_control == var_prenom:
            button_f = Button(frame, text="Générer prénom femme", font=("Courrier", 8),
                              command=lambda: generate_name_fille(entry))
            button_f.grid(row=3, column=0, padx=1, pady=5)
            button_g = Button(frame, text="Générer prénom homme", font=("Courrier", 8),
                              command=lambda: generate_name_garcon(entry))
            button_g.grid(row=3, column=1, padx=1, pady=5)
            # if var_genre.get() == "homme":
            #     button_g = Button(frame, text="Générer prénom homme", command=lambda: generate_name_garcon(entry))
            #     button_g.grid(row=4, column=0)
            # elif var_genre.get() == "femme":
            #     button_f = Button(frame, text="Générer prénom femme", command=lambda: generate_name_fille(entry))
            #     button_f.grid(row=3, column=0)

    return frame


# creer une premiere fenetre
window = Tk()

# personnaliser cette fenetre
window.title("Générateur")
window.geometry("1080x720")
window.iconbitmap("logo2.ico")
window.config(background='#4a8ecc')

# declarer les variables
list_personnages_crees = []
donnees = {"images": "personnages/"}

var_fichier = StringVar()

var_genre = StringVar()
var_prenom = StringVar()
var_chapeau = StringVar()
var_chauve = StringVar()
var_cheveux = StringVar()
var_barbe = StringVar()
var_lunettes = StringVar()
var_moustache = StringVar()

nbr_persos_crees = IntVar()
nbr_persos_crees.set(1)

nbr_fichiers_crees = IntVar()
nbr_fichiers_crees.set(0)


def enregistrer_perso():
    if len(var_genre.get()) == 0 or len(var_prenom.get()) == 0 or len(var_chapeau.get()) == 0 or len(var_chauve.get()) \
            == 0 or len(var_cheveux.get()) == 0 or len(var_barbe.get()) == 0 or len(var_lunettes.get()) == 0 \
            or len(var_moustache.get()) == 0:
        pass
    else:
        p = {'fichier': "inconnu.PNG", 'prenom': var_prenom.get(), 'genre': var_genre.get(),
             'cheveux': var_cheveux.get(), 'lunettes': var_lunettes.get(), 'chauve': var_chauve.get(),
             'chapeau': var_chapeau.get(), 'barbe': var_barbe.get(), 'moustache': var_moustache.get()}
        list_personnages_crees.append(p)
        # donnees["personnages"][nbr_persos_crees.get() - 1] = p
        label_droit_prenom.configure(text=label_droit_prenom.cget("text") + str(var_prenom.get() + ' '))

        # effacer les données écrites
        label_text_attribut1.configure(text=label_text_attribut1.cget("text").removesuffix(" " + var_genre.get()))
        var_genre.set('')
        label_text_attribut2.configure(text=label_text_attribut2.cget("text").removesuffix(" " + var_prenom.get()))
        var_prenom.set('')
        label_text_attribut3.configure(text=label_text_attribut3.cget("text").removesuffix(" " + var_chapeau.get()))
        var_chapeau.set('')
        label_text_attribut4.configure(text=label_text_attribut4.cget("text").removesuffix(" " + var_chauve.get()))
        var_chauve.set('')
        label_text_attribut5.configure(text=label_text_attribut5.cget("text").removesuffix(" " + var_cheveux.get()))
        var_cheveux.set('')
        label_text_attribut6.configure(text=label_text_attribut6.cget("text").removesuffix(" " + var_barbe.get()))
        var_barbe.set('')
        label_text_attribut7.configure(text=label_text_attribut7.cget("text").removesuffix(" " + var_lunettes.get()))
        var_lunettes.set('')
        label_text_attribut8.configure(text=label_text_attribut8.cget("text").removesuffix(" " + var_moustache.get()))
        var_moustache.set('')
        # incrementer nombre personnages créés
        label_text.configure(text=label_text.cget("text").removeprefix(str(nbr_persos_crees.get()) + "e "))
        if nbr_persos_crees.get() < 24:
            nbr_persos_crees.set(nbr_persos_crees.get() + 1)
        label_text.configure(text=str(nbr_persos_crees.get()) + "e " + label_text.cget("text"))
    createPers()


# declarer les frames
frame_title = Frame(window, bg='#4a8ecc')
frame_subtitle = Frame(window, bg='#4a8ecc')
frame_image = Frame(window, bg='#4a8ecc', bd=1, relief=SUNKEN)
frame_1 = Frame(window, bg='#4a8ecc', bd=1, relief=SUNKEN)
frame_2 = Frame(window, bg='#4a8ecc', bd=1, relief=SUNKEN)

# creation d'image
width = 874 * 0.3
height = 968 * 0.3
image = PhotoImage(file="inconnu.PNG").zoom(10).subsample(35)
canvas = Canvas(frame_image, width=width, height=height, bg='#4a8ecc')
canvas.create_image(width / 2, height / 2, image=image)
canvas.pack()

label_title = Label(frame_title, text="Choix des personnages", anchor='w', font=("Courrier", 20), bg='#4a8ecc',
                    fg="black")
label_title.pack(fill='both')
label_subtitle = Label(frame_subtitle, text="24 personnages à créer :", anchor='w', font=("Courrier", 15), bg='#4a8ecc',
                       fg="black")
label_subtitle.pack(fill='both')

# frame de gauche
label_text = Label(frame_image, text="personnage", font=("Courrier", 15), bg='#4a8ecc', fg="black")
label_text.pack()
label_text.configure(text=str(1) + "e " + label_text.cget("text"))
label_text_attribut1 = Label(frame_image, text="Genre :", font=("Courrier", 10), bg='#4a8ecc', fg="black")
label_text_attribut1.pack(pady=(0, 2), padx=(10, 0), anchor='w')
label_text_attribut2 = Label(frame_image, text="Prénom :", font=("Courrier", 10), bg='#4a8ecc', fg="black")
label_text_attribut2.pack(pady=(0, 2), padx=(10, 0), anchor='w')
label_text_attribut3 = Label(frame_image, text="Chapeau :", font=("Courrier", 10), bg='#4a8ecc', fg="black")
label_text_attribut3.pack(pady=(0, 2), padx=(10, 0), anchor='w')
label_text_attribut4 = Label(frame_image, text="Chauve :", font=("Courrier", 10), bg='#4a8ecc', fg="black")
label_text_attribut4.pack(pady=(0, 2), padx=(10, 0), anchor='w')
label_text_attribut5 = Label(frame_image, text="Cheveux :", font=("Courrier", 10), bg='#4a8ecc', fg="black")
label_text_attribut5.pack(pady=(0, 2), padx=(10, 0), anchor='w')
label_text_attribut6 = Label(frame_image, text="Barbe :", font=("Courrier", 10), bg='#4a8ecc', fg="black")
label_text_attribut6.pack(pady=(0, 2), padx=(10, 0), anchor='w')
label_text_attribut7 = Label(frame_image, text="Lunettes :", font=("Courrier", 10), bg='#4a8ecc', fg="black")
label_text_attribut7.pack(pady=(0, 2), padx=(10, 0), anchor='w')
label_text_attribut8 = Label(frame_image, text="Moustache :", font=("Courrier", 10), bg='#4a8ecc', fg="black")
label_text_attribut8.pack(pady=(0, 12), padx=(10, 0), anchor='w')
button_enregistrer = Button(frame_image, text="Enregistrer le personnage", font=("Courrier", 12), bg='white', fg='black'
                            , command=enregistrer_perso)
button_enregistrer.pack(fill=X)

COUNT = 0
NBR_ATTRIBUTS = 8
list_frames = []


def createPers():
    # nombre attributs
    global COUNT
    COUNT = 0
    global list_frames
    list_frames = []

    # frame genre
    l1 = ["homme", "femme"]
    f1 = sousFrame("Genre", l1, False, var_genre, label_text_attribut1)
    list_frames.append(f1)
    f1.grid()

    # frame prenom
    l2 = []
    f2 = sousFrame("Prénom", l2, True, var_prenom, label_text_attribut2)
    list_frames.append(f2)

    # frame chapeau
    l3 = ["oui", "non"]
    f3 = sousFrame("Chapeau", l3, False, var_chapeau, label_text_attribut3)
    list_frames.append(f3)

    # frame chauve
    l4 = ["oui", "non"]
    f4 = sousFrame("Chauve", l4, False, var_chauve, label_text_attribut4)
    list_frames.append(f4)

    # frame cheveux
    l5 = ["blanc", "blond", "noir", "roux", "chatain", "brun"]
    f5 = sousFrame("Cheveux", l5, False, var_cheveux, label_text_attribut5)
    list_frames.append(f5)

    # frame barbe
    l6 = ["oui", "non"]
    f6 = sousFrame("Barbe", l6, False, var_barbe, label_text_attribut6)
    list_frames.append(f6)

    # frame lunettes
    l7 = ["oui", "non"]
    f7 = sousFrame("lunettes", l7, False, var_lunettes, label_text_attribut7)
    list_frames.append(f7)

    # frame moustache
    l8 = ["oui", "non"]
    f8 = sousFrame("Moustache", l8, False, var_moustache, label_text_attribut8)
    list_frames.append(f8)


createPers()

# frame droit
label_droit = Label(frame_2, text="Personnages créés :", font=("Courrier", 15), bg='#4a8ecc', fg="black")
label_droit.pack()
label_droit_prenom = Label(frame_2, text="", font=("Courrier", 10), bg='#4a8ecc', fg="black")
label_droit_prenom.pack(pady=(0, 2), padx=(10, 0), anchor='w')

button2 = Button(frame_2, text="Créer le fichier .json des personnages", font=("Courrier", 10), bg='white', fg='grey',
                 command=creer_fichier)
button2.pack()

frame_title.pack(fill='x', pady=(25, 10), padx=10)
frame_subtitle.pack(fill='x', pady=(0, 20), padx=10)
frame_image.pack(expand=False, fill='both', pady=20, side='left')
frame_1.pack(expand=YES, fill='both', padx=20, pady=20, side='left')
frame_2.pack(fill='both', padx=20, pady=20, side='left')

# # bouton générateur
# button_generateur = Button(frame_1, text="Générer un personnage", font=("Courrier", 20), bg='white', fg='grey',
#                            command=generer_personnage)
# button_generateur.grid(sticky='s')

window.mainloop()
