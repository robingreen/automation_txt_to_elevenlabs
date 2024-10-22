import tkinter as tk
import pyperclip
import pyautogui
import time

# Message initial
message_initial = """Colle ton texte ici formaté avec des sauts de ligne après chaque point.
Assure-toi d'avoir Google Chrome connecté à ton compte et l'application ElevenLabs connectée.
Assure-toi aussi que tous tes réglages sont faits dans ElevenLabs."""

# Fonction pour copier tout le texte de l'encart
def copier_texte():
    texte = texte_encart.get("1.0", "end-1c")  # Obtenir tout le texte de l'encart
    pyperclip.copy(texte)  # Copier le texte dans le presse-papiers

# Fonction pour taper "elev" et sélectionner "Passer à cet onglet"
def naviguer_vers_elev():
    # Amener la fenêtre Chrome au premier plan
    chrome_windows = pyautogui.getWindowsWithTitle('Google Chrome')
    if chrome_windows:
        chrome_windows[0].activate()  # Activer la fenêtre existante de Chrome
    time.sleep(1)  # Attendre que la fenêtre soit active

    # Sélectionner la barre d'adresse
    pyautogui.hotkey('ctrl', 'a')  # Sélectionner tout le texte
    pyautogui.hotkey('ctrl', 'v')  # Coller le texte copié
    time.sleep(0.1)  # Petite pause  
 

# Fonction principale exécutée lors du clic sur "Run Task"
def run_task():
    copier_texte()
    naviguer_vers_elev()

# Créer la fenêtre Tkinter
root = tk.Tk()
root.title("Instructions")

# Ajouter le message initial en haut de la fenêtre
label_message = tk.Label(root, text=message_initial, padx=10, pady=10, justify="left")
label_message.pack(padx=20, pady=10)

# Ajouter le bouton "Run Task"
bouton_run = tk.Button(root, text="Run Task", command=run_task)
bouton_run.pack(padx=20, pady=10)

# Ajouter un encart pour le texte
texte_encart = tk.Text(root, wrap="word", height=20, width=80, padx=10, pady=10)
texte_encart.pack(padx=20, pady=20)

# Lancer la boucle principale Tkinter
root.mainloop()
