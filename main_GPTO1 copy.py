import tkinter as tk
from tkinter import filedialog, messagebox
import pyperclip
import pyautogui
import time
import os
import shutil
import pygetwindow as gw
import re
import string
import sys
from pydub import AudioSegment
from pydub.utils import which

AudioSegment.converter = which("ffmpeg")

# Message initial et avertissement
message_initial = """Colle ton texte ici formaté avec des sauts de ligne après chaque point.
Assure-toi d'avoir Google Chrome connecté à ton compte et l'application ElevenLabs ouverte sur la bonne page.
Assure-toi aussi que tous tes réglages sont faits dans ElevenLabs.
Ne touche pas à l'ordinateur pendant l'exécution du script."""

message_avertissement = "Assure-toi que l'onglet ElevenLabs est ouvert dans Google Chrome, et qu'aucune autre fenêtre ne viendra interférer."

destination_finale = None  # Variable globale pour le dossier de destination final
fichiers_mp3_crees = []   # Liste des fichiers MP3 créés
lignes_globales = []      # Liste globale des lignes traitées

# Fonction pour effacer les mp3 commençant par 'ElevenLab' dans Downloads
def effacer_mp3_elevenlabs():
    chemin_source = os.path.expanduser("~\\Downloads")
    fichiers_a_effacer = [f for f in os.listdir(chemin_source) if f.startswith('ElevenLab') and f.endswith('.mp3')]
    if fichiers_a_effacer:
        reponse = messagebox.askyesno("Effacer les fichiers", "Voulez-vous effacer tous les fichiers MP3 commençant par 'ElevenLab' dans le dossier Downloads ?")
        if reponse:
            for fichier in fichiers_a_effacer:
                try:
                    os.remove(os.path.join(chemin_source, fichier))
                except Exception as e:
                    print(f"Erreur lors de la suppression du fichier {fichier}: {e}")
            messagebox.showinfo("Suppression terminée", "Les fichiers MP3 ont été supprimés.")
        else:
            messagebox.showinfo("Info", "Les fichiers MP3 n'ont pas été supprimés.")
    else:
        messagebox.showinfo("Info", "Aucun fichier MP3 commençant par 'ElevenLab' trouvé dans le dossier Downloads.")

# Fonction pour nettoyer les noms de fichiers
def nettoyer_nom_fichier(nom):
    # Remplacer les caractères non autorisés par '_'
    nom_nettoye = re.sub(r'[<>:"/\\|?*]', '_', nom)
    # Supprimer les caractères non imprimables
    nom_nettoye = ''.join(c for c in nom_nettoye if c in string.printable)
    # Limiter la longueur du nom
    return nom_nettoye[:255]

# Fonction pour copier tout le texte de l'encart
def copier_texte():
    texte = texte_encart.get("1.0", "end-1c")  # Obtenir tout le texte de l'encart
    lignes = [ligne.strip() for ligne in texte.split('\n') if ligne.strip()]
    lignes_nettoyees = []
    for ligne in lignes:
        # Retirer les parenthèses et leur contenu du texte à copier
        ligne_sans_parentheses = re.sub(r'\s*\(.*?\)\s*', '', ligne).strip()
        # Trouver tous les nombres à l'intérieur des parenthèses
        nombres = re.findall(r'\(([^()]*)\)', ligne)
        temps_silence = 0
        for contenu in nombres:
            nombres_dans_contenu = re.findall(r'\d+', contenu)
            temps_silence += sum(int(n) for n in nombres_dans_contenu)
        lignes_nettoyees.append((ligne_sans_silence, temps_silence))
    return lignes_nettoyees

# Fonction pour charger le texte depuis un fichier .txt
def charger_texte_fichier():
    fichier_txt = filedialog.askopenfilename(title="Sélectionner un fichier texte", filetypes=[("Fichiers texte", "*.txt")])
    if fichier_txt:
        with open(fichier_txt, 'r', encoding='utf-8') as f:
            contenu = f.read()
            texte_encart.delete("1.0", tk.END)
            texte_encart.insert(tk.END, contenu)

# Fonction pour activer la fenêtre Chrome avec ElevenLabs
def activer_fenetre_chrome_elevenlabs():
    # Rechercher les fenêtres dont le titre contient 'ElevenLabs' et 'Google Chrome'
    all_windows = gw.getAllWindows()
    for window in all_windows:
        if 'ElevenLabs' in window.title and 'Google Chrome' in window.title:
            try:
                if window.isMinimized:
                    window.restore()
                window.activate()
                window.maximize()  # S'assurer que la fenêtre est maximisée
                time.sleep(1)  # Attendre pour que la fenêtre soit bien activée
                return True
            except Exception as e:
                print(f"Erreur lors de l'activation de la fenêtre Chrome ElevenLabs : {e}")
                return False
    print("Fenêtre 'ElevenLabs' dans Google Chrome non trouvée.")
    return False

# Fonction pour détecter le message d'erreur
def detect_error_message():
    # Assumes that 'error_message.png' is an image of the error message
    try:
        error_location = pyautogui.locateOnScreen('error_message.png', confidence=0.8)
        return error_location is not None
    except Exception as e:
        print(f"Erreur lors de la détection du message d'erreur: {e}")
        return False

# Fonction pour naviguer vers ElevenLabs et effectuer les actions
def naviguer_vers_elev(ligne):
    if not activer_fenetre_chrome_elevenlabs():
        return False  # Si la fenêtre n'est pas trouvée, on arrête la fonction et indique un échec

    # Copier et coller la ligne actuelle
    pyperclip.copy(ligne)  # Copier la ligne actuelle dans le presse-papiers
    pyautogui.click(x=945, y=459)  # Clic sur le champ de saisie de texte (coordonnées absolues)
    time.sleep(0.5)  # Petite pause pour stabiliser le clic

    pyautogui.hotkey('ctrl', 'a')  # Sélectionner tout le texte
    time.sleep(0.2)  # Pause entre les actions
    pyautogui.hotkey('ctrl', 'v')  # Coller le texte copié
    time.sleep(0.2)  # Pause entre les actions
    pyautogui.hotkey('shift', 'enter')  # Lancer la génération du mp3

    # Ajuster le temps de pause selon la longueur de la ligne
    if len(ligne) > 50:
        temps_attente = max(5.0, len(ligne) * 0.07)
    else:
        temps_attente = max(3.5, len(ligne) * 0.05)

    time.sleep(temps_attente)  # Attendre que la génération soit terminée

    # Essayer de télécharger le MP3, avec des tentatives en cas d'erreur
    max_attempts = 4
    attempts = 0
    while attempts < max_attempts:
        # Clic pour lancer le téléchargement du MP3
        pyautogui.click(x=1809, y=957)  # Clic sur le bouton de téléchargement (coordonnées absolues)
        time.sleep(1)  # Attendre un peu pour que le message d'erreur puisse apparaître

        # Vérifier si le message d'erreur apparaît
        if detect_error_message():
            attempts += 1
            print(f"Tentative {attempts}/{max_attempts} échouée. Le serveur est occupé.")
            if attempts >= max_attempts:
                print("Le serveur est occupé. Nombre maximal de tentatives atteint. Passage à l'étape de mixage.")
                return False  # Indiquer un échec pour cette phrase
            else:
                time.sleep(3)  # Attendre 3 secondes avant de réessayer le même clic
                continue  # Réessayer avec la même phrase
        else:
            break  # Pas d'erreur, on sort de la boucle et passe à l'étape suivante normalement

    pyautogui.click(x=945, y=459)  # Pour recentrer l'attention sur la fenêtre d'entrée ElevenLabs.
    return True  # Indiquer un succès

# Fonction principale exécutée lors du clic sur "Run Task"
def run_task():
    global lignes_globales, fichiers_mp3_crees
    chemin_source = os.path.expanduser("~\\Downloads")
    fichiers_mp3_initial = set(f for f in os.listdir(chemin_source) if f.endswith(".mp3"))

    lignes = copier_texte()  # Obtenir les lignes non vides du texte avec les silences
    lignes_globales = lignes  # Stocker globalement pour d'autres fonctions

    compteur_telechargements = 0  # Initialiser un compteur pour les téléchargements
    stop_processing = False  # Indicateur pour arrêter le traitement

    for i, (ligne_sans_silence, temps_silence) in enumerate(lignes):
        success = naviguer_vers_elev(ligne_sans_silence)
        if not success:
            print("Arrêt du traitement en raison d'erreurs répétées.")
            stop_processing = True
            break  # Sortir de la boucle des lignes

        time.sleep(temps_silence)  # Attendre le silence spécifié

        compteur_telechargements += 1  # Incrémenter le compteur après chaque téléchargement

        # Pause de 10 secondes tous les quatre téléchargements
        if compteur_telechargements % 4 == 0:
            time.sleep(10)

    time.sleep(5)  # Attendre que tous les fichiers soient bien téléchargés

    # Obtenir les nouveaux fichiers MP3
    fichiers_mp3_final = set(f for f in os.listdir(chemin_source) if f.endswith(".mp3"))
    nouveaux_fichiers_mp3 = list(fichiers_mp3_final - fichiers_mp3_initial)

    attribuer_noms_fichiers_mp3(lignes, nouveaux_fichiers_mp3, chemin_source)

    # Si le traitement a été arrêté prématurément, adapter la liste des lignes pour le reste du programme
    if stop_processing:
        lignes = lignes[:compteur_telechargements]
        lignes_globales = lignes

    proposer_deplacer_fichiers(lignes)

# Fonction pour attribuer les noms des fichiers .mp3
def attribuer_noms_fichiers_mp3(lignes, nouveaux_fichiers_mp3, chemin_source):
    global fichiers_mp3_crees
    if len(nouveaux_fichiers_mp3) == 0:
        messagebox.showwarning("Attention", "Aucun fichier MP3 n'a été téléchargé.")
        return

    # Trier les nouveaux fichiers par date de création
    nouveaux_fichiers_mp3.sort(key=lambda f: os.path.getctime(os.path.join(chemin_source, f)))

    fichiers_crees = []
    for i, fichier in enumerate(nouveaux_fichiers_mp3):
        if i < len(lignes):
            ligne_sans_silence, _ = lignes[i]
            nouveau_nom = f"{nettoyer_nom_fichier(ligne_sans_silence)}.mp3"
            ancien_chemin = os.path.join(chemin_source, fichier)
            nouveau_chemin = os.path.join(chemin_source, nouveau_nom)
            try:
                os.rename(ancien_chemin, nouveau_chemin)
                fichiers_crees.append(nouveau_nom)
            except Exception as e:
                print(f"Erreur lors du renommage du fichier {fichier}: {e}")
    fichiers_mp3_crees = fichiers_crees  # Stocker la liste des fichiers créés

# Le reste du code (fonctions pour déplacer les fichiers, mixage, interface graphique, etc.) reste inchangé.

# Fonction pour initialiser l'interface principale
def initialiser_interface():
    # Ajouter le message initial en haut de la fenêtre
    label_message = tk.Label(root, text=message_initial, padx=10, pady=10, justify="left")
    label_message.pack(padx=20, pady=10)

    # Ajouter un encart pour le texte
    global texte_encart
    texte_encart = tk.Text(root, wrap="word", height=20, width=80, padx=10, pady=10)
    texte_encart.pack(padx=20, pady=20)

    # Ajouter un bouton pour charger un fichier .txt
    bouton_charger_fichier = tk.Button(root, text="Je préfère soumettre un fichier .txt", command=charger_texte_fichier)
    bouton_charger_fichier.pack(padx=20, pady=5)

    # Ajouter le bouton "Run Task"
    bouton_run = tk.Button(root, text="Run Task", command=run_task)
    bouton_run.pack(padx=20, pady=10)

# Fonction pour continuer après la vérification
def continuer():
    avertissement_label.pack_forget()  # Masquer l'avertissement
    bouton_continuer.pack_forget()  # Masquer le bouton de confirmation
    effacer_mp3_elevenlabs()  # Appeler la fonction pour effacer les MP3 si nécessaire
    initialiser_interface()  # Initialiser l'interface principale

# Création de la fenêtre principale
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