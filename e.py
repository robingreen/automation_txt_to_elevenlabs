import tkinter as tk
import pyperclip
import pyautogui
import time
import os
import sys

# Message initial et avertissement
message_initial = """Colle ton texte ici formaté avec des sauts de ligne après chaque point.
Assure-toi d'avoir Google Chrome connecté à ton compte et l'application ElevenLabs connectée.
Assure-toi aussi que tous tes réglages sont faits dans ElevenLabs."""

message_avertissement = "Assure-toi que ElevenLabs est le dernier onglet ouvert, et rien d'autre."

# Fonction pour copier tout le texte de l'encart
def copier_texte():
    texte = texte_encart.get("1.0", "end-1c")  # Obtenir tout le texte de l'encart
    return [ligne for ligne in texte.split('\n') if ligne.strip()]  # Retourner les lignes non vides

# Fonction pour taper "elev" et sélectionner "Passer à cet onglet"
def naviguer_vers_elev(ligne):
    # Amener la fenêtre Chrome au premier plan
    chrome_windows = pyautogui.getWindowsWithTitle('Google Chrome')
    if chrome_windows:
        chrome_windows[0].activate()  # Activer la fenêtre existante de Chrome
    time.sleep(1)  # Attendre que la fenêtre soit active

    # Copier et coller la ligne actuelle
    pyperclip.copy(ligne)  # Copier la ligne actuelle dans le presse-papiers
    pyautogui.click(x=945, y=459) #Clic en plein dans la fenetre de saisie de txt du site web
    pyautogui.hotkey('ctrl', 'a')  # Sélectionner tout le texte
    pyautogui.hotkey('ctrl', 'v')  # Coller le texte copié
    time.sleep(0.1)  # Petite pause

    pyautogui.click(x=1809, y=957) #clic sur le bouton download dont la position est trouvée par le freeware mousepos
# Fonction principale exécutée lors du clic sur "Run Task"
def run_task():
    lignes = copier_texte()  # Obtenir les lignes non vides du texte
    for i in range(min(5, len(lignes))):  # Répéter jusqu'à la cinquième ligne
        naviguer_vers_elev(lignes[i])  # Naviguer avec la ligne actuelle

# Fonction pour continuer après la vérification
def continuer():
    avertissement_label.pack_forget()  # Masquer l'avertissement
    bouton_continuer.pack_forget()  # Masquer le bouton de confirmation
    initialiser_interface()  # Initialiser l'interface principale

# Fonction pour créer la fenêtre d'arrêt d'urgence
def fenetre_arret_urgence():
    arret_fenetre = tk.Toplevel()  # Créer une nouvelle fenêtre
    arret_fenetre.title("Arrêt d'Urgence")
    arret_fenetre.geometry("300x150")
    arret_fenetre.attributes("-topmost", True)  # La rendre flottante au-dessus de tout
    arret_fenetre.protocol("WM_DELETE_WINDOW", lambda: None)  # Désactiver la fermeture standard

    label_alerte = tk.Label(arret_fenetre, text="ABSOLUMENT TOUT ARRÊTER", font=("Arial", 14, "bold"), fg="red")
    label_alerte.pack(padx=20, pady=20)

    bouton_arret = tk.Button(arret_fenetre, text="ARRÊT D'URGENCE", font=("Arial", 12), bg="red", fg="white",
                             command=arreter_programme)
    bouton_arret.pack(padx=20, pady=10)

# Fonction pour arrêter le programme de manière drastique
def arreter_programme():
    os._exit(1)  # Terminer immédiatement tous les processus en cours

# Initialisation de l'interface principale
def initialiser_interface():
    # Ajouter le message initial en haut de la fenêtre
    label_message = tk.Label(root, text=message_initial, padx=10, pady=10, justify="left")
    label_message.pack(padx=20, pady=10)

    # Ajouter le bouton "Run Task"
    bouton_run = tk.Button(root, text="Run Task", command=run_task)
    bouton_run.pack(padx=20, pady=10)

    # Ajouter un encart pour le texte
    global texte_encart
    texte_encart = tk.Text(root, wrap="word", height=20, width=80, padx=10, pady=10)
    texte_encart.pack(padx=20, pady=20)

# Créer la fenêtre Tkinter
root = tk.Tk()
root.title("Instructions")

# Afficher le message d'avertissement en haut de la fenêtre
avertissement_label = tk.Label(root, text=message_avertissement, padx=10, pady=20, font=("Arial", 16, "bold"), fg="red")
avertissement_label.pack(padx=20, pady=20)

# Ajouter le bouton de confirmation
bouton_continuer = tk.Button(root, text="J'ai vérifié, je veux continuer", command=continuer, font=("Arial", 12), bg="green", fg="white")
bouton_continuer.pack(padx=20, pady=10)

# Créer la fenêtre d'arrêt d'urgence
fenetre_arret_urgence()

# Lancer la boucle principale Tkinter
root.mainloop()