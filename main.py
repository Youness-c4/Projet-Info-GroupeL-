
#---------------------------------------------------------------------------------------------
#                                             jeu QUI EST CE ?
#
# Sylvain
# Mehdi
# Youness
# AMG
#----------------------------------------------------------------------------------------------
# date: février - mars
#-----------------------------------------------------------------------------------------------
# réalisation du jeu de societe Qui est ce
# PYTHON
#---------------------------------------------------------------------------------------------
# import des bib
# tkinter pour l'interface graphique
# scipy pour utiliser array
from tkinter import *
from scipy import * 
import json 
#----------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------
# Créer un tableau des personnages avec le JSON
list_nom_fichier_pers=[]

with open("BDD.json") as mon_fichier:
    data = json.load(mon_fichier)

for pers in data["personnages"]:
    list_nom_fichier_pers.append(pers["fichier"])

print(list_nom_fichier_pers)
#----------------------------------------------------


#----------------------------------------------------------------------------------------------------
# FONCTIONS

#fonctions déroulement de la partie
def debut():
    pass

def controleEtatPartie():
    pass

def quitter():
    pass
#fonction selection du personnage (random)

#fonction des questions généraliste avec critère en paramètre

#fonction des questions "est-ce le personnage ... ?" avec personnage en paramètre

#fonction éliminer un personnage
def elimine():
    pass
#----------------------------------------------------



#----------------------------------------------------------------------------------------------------
# GRAPHIQUE
    
window=Tk()
window.title('QUI EST CE ?')
window.geometry("700x350")

canvas = Canvas(window, width= 350)

def exit_program():
   win.destroy()
def my_command():
   text.config(text= "You have clicked Me...")

text= Label(canvas, text= "")
text.pack(pady=30)

click_btn= PhotoImage(file='personnages/samuel.png')
img_label= Label(image=click_btn)
for i in range(4):
    Button(canvas, image=click_btn, command= my_command, borderwidth=0).pack()
    
#Button(canvas, text="hello", command= exit_program).pack()
canvas.pack()  



window.mainloop()

#----------------------------------------------------------------------------------------------------