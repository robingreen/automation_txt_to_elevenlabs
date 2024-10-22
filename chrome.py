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

# Fonction pour ouvrir Google Chrome
def ouvrir_chrome():
    try:
        # Essayer d'ouvrir Google Chrome sans URL pour éviter un nouvel onglet
        if sys.platform.startswith('win'):
            subprocess.Popen(['start', 'chrome'], shell=True)  # Windows
        elif sys.platform.startswith('darwin'):
            subprocess.Popen(['open', '-a', 'Google Chrome'])  # macOS
        elif sys.platform.startswith('linux'):
            subprocess.Popen(['google-chrome'])  # Linux
    except Exception as e:
        print(f"Erreur lors de l'ouverture de Chrome : {e}")

# Fonction pour copier la première ligne du texte de l'encart et lancer l'automatisation
def copier_et_automatiser():
    texte = texte_encart.get("1.0", "end-1c")  # Obtenir tout le texte de l'encart
    premiere_ligne = texte.split('\n')[0]  # Extraire la première ligne
    pyperclip.copy(premiere_ligne)  # Copier la première ligne dans le presse-papiers
    ouvrir_chrome()  # Ouvrir Google Chrome sans URL
    time.sleep(2)  # Attendre que Chrome s'ouvre
    automatisation_chrome()  # Appeler la fonction d'automatisation dans Chrome

# Fonction pour automatiser la frappe clavier dans Chrome
def automatisation_chrome():
    # Placer le focus sur la barre d'adresse et taper "elev"
    pyautogui.hotkey('ctrl', 'l')  # Focus sur la barre d'adresse
    pyautogui.typewrite('elev')  # Taper "elev"
    time.sleep(1)  # Attendre pour que le menu se déploie

    # Simuler un appui sur "Passer à cet onglet"
    pyautogui.press('down')  # Descendre d'une option
    pyautogui.press('enter')  # Valider avec ENTER
    time.sleep(2)  # Attendre que l'onglet s'ouvre

    # Automatiser la sélection, le collage et les frappes clavier
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
bouton_run = tk.Button(root, text="Run Task", command=copier_et_automatiser)
bouton_run.pack(padx=20, pady=10)

# Ajouter un encart pour le texte
texte_encart = tk.Text(root, wrap="word", height=20, width=80, padx=10, pady=10)
texte_encart.pack(padx=20, pady=20)

# Lancer la boucle principale Tkinter
root.mainloop()
