import tkinter as tk
import pyperclip
import webbrowser
import os
import sys
import subprocess
import pyautogui
import time

# Message initial
message_initial = """Colle ton texte ici formaté avec des sauts de ligne après chaque point.
Assure-toi d'avoir Google Chrome connecté à ton compte et l'application ElevenLabs connectée, 
et de faire de Chrome ton navigateur par défaut.
Assure-toi aussi que tous tes réglages sont faits dans ElevenLabs."""

# Fonction pour copier la première ligne du texte de l'encart
def copier_et_ouvrir():
    texte = texte_encart.get("1.0", "end-1c")  # Obtenir tout le texte de l'encart
    premiere_ligne = texte.split('\n')[0]  # Extraire la première ligne
    pyperclip.copy(premiere_ligne)  # Copier la première ligne dans le presse-papiers
    ouvrir_chrome_et_taper()  # Appeler la fonction pour ouvrir Chrome et taper "elev"

# Fonction pour ouvrir Chrome et taper "elev"
def ouvrir_chrome_et_taper():
    try:
        # Ouvrir un nouvel onglet du navigateur par défaut
        webbrowser.open_new_tab("chrome://newtab")
        time.sleep(2)  # Attendre pour que le nouvel onglet s'ouvre
        pyautogui.typewrite("elev", interval=0.1)  # Taper "elev" dans la barre d'adresse
        pyautogui.press('enter')  # Appuyer sur Enter
        time.sleep(6)  # Attendre que la page se charge
        automatisation_actions()  # Appeler la fonction d'automatisation des actions
    except:
        # Si ça échoue, utiliser subprocess pour ouvrir Chrome et taper
        if sys.platform.startswith('win'):
            subprocess.run(['start', 'chrome', 'chrome://newtab'], shell=True)  # Pour Windows
        elif sys.platform.startswith('darwin'):
            subprocess.run(['open', '-a', 'Google Chrome', '--args', 'chrome://newtab'])  # Pour macOS
        elif sys.platform.startswith('linux'):
            subprocess.run(['google-chrome', 'chrome://newtab'])  # Pour Linux
        time.sleep(2)
        pyautogui.typewrite("elev", interval=0.1)
        pyautogui.press('enter')
        time.sleep(6)
        automatisation_actions()

# Fonction pour automatiser la sélection, le collage et les frappes clavier
def automatisation_actions():
    pyautogui.hotkey('ctrl', 'a')  # Sélectionner tout le texte
    pyautogui.hotkey('ctrl', 'v')  # Coller le texte
    pyautogui.press('tab', presses=3)  # Appuyer sur TAB trois fois
    pyautogui.hotkey('shift', 'enter')  # Appuyer sur SHIFT + ENTER

# Créer la fenêtre Tkinter
root = tk.Tk()
root.title("Instructions")

# Ajouter le message initial en haut de la fenêtre
label_message = tk.Label(root, text=message_initial, padx=10, pady=10, justify="left")
label_message.pack(padx=20, pady=10)

# Ajouter le bouton "Run Task"
bouton_run = tk.Button(root, text="Run Task", command=copier_et_ouvrir)
bouton_run.pack(padx=20, pady=10)

# Ajouter un encart pour le texte
texte_encart = tk.Text(root, wrap="word", height=20, width=80, padx=10, pady=10)
texte_encart.pack(padx=20, pady=20)

# Lancer la boucle principale Tkinter
root.mainloop()
