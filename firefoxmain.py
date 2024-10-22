import tkinter as tk
import pyperclip
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

# Chemin vers GeckoDriver
GECKO_DRIVER_PATH = 'votre_chemin_vers_geckodriver'  # Remplacez par le chemin vers GeckoDriver

# Créer un profil Firefox pour maintenir la même session
options = Options()
options.add_argument("-profile")
options.add_argument("votre_chemin_vers_profil_firefox")  # Chemin vers un profil Firefox existant

# Message initial
message_initial = """Colle ton texte ici formaté avec des sauts de ligne après chaque point.
Assure-toi d'avoir Firefox connecté à ton compte et l'application ElevenLabs connectée.
Assure-toi aussi que tous tes réglages sont faits dans ElevenLabs."""

# Fonction pour copier la première ligne du texte de l'encart et utiliser Selenium
def copier_et_utiliser_selenium():
    texte = texte_encart.get("1.0", "end-1c")  # Obtenir tout le texte de l'encart
    premiere_ligne = texte.split('\n')[0]  # Extraire la première ligne
    pyperclip.copy(premiere_ligne)  # Copier la première ligne dans le presse-papiers

    try:
        # Démarrer le navigateur avec GeckoDriver
        driver = webdriver.Firefox(service=Service(GECKO_DRIVER_PATH), options=options)

        # Aller sur la page ElevenLabs
        driver.get("https://elevenlabs.io/app/speech-synthesis/text-to-speech")
        
        # Attendre que la page soit complètement chargée
        time.sleep(6)

        # Automatiser la sélection, le collage et les frappes clavier
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.CONTROL + 'a')  # Sélectionner tout le texte
        body.send_keys(Keys.CONTROL + 'v')  # Coller le texte
        body.send_keys(Keys.TAB * 3)  # Appuyer sur TAB trois fois
        body.send_keys(Keys.SHIFT + Keys.ENTER)  # Appuyer sur SHIFT + ENTER
    except Exception as e:
        print(f"Erreur lors de l'automatisation avec Selenium et Firefox : {e}")

# Créer la fenêtre Tkinter
root = tk.Tk()
root.title("Instructions")

# Ajouter le message initial en haut de la fenêtre
label_message = tk.Label(root, text=message_initial, padx=10, pady=10, justify="left")
label_message.pack(padx=20, pady=10)

# Ajouter le bouton "Run Task"
bouton_run = tk.Button(root, text="Run Task", command=copier_et_utiliser_selenium)
bouton_run.pack(padx=20, pady=10)

# Ajouter un encart pour le texte
texte_encart = tk.Text(root, wrap="word", height=20, width=80, padx=10, pady=10)
texte_encart.pack(padx=20, pady=20)

# Lancer la boucle principale Tkinter
root.mainloop()
