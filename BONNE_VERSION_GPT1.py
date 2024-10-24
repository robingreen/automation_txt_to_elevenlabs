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

# Message initial et avertissement
message_initial = """Colle ton texte ici formaté avec des sauts de ligne après chaque point.
Assure-toi d'avoir Google Chrome connecté à ton compte et l'application ElevenLabs ouverte sur la bonne page.
Assure-toi aussi que tous tes réglages sont faits dans ElevenLabs.
Ne touche pas à l'ordinateur pendant l'exécution du script."""

message_avertissement = "Assure-toi que l'onglet ElevenLabs est ouvert dans Google Chrome, et qu'aucune autre fenêtre ne viendra interférer."

destination_finale = None  # Variable globale pour le dossier de destination final
fichiers_mp3_crees = []   # Liste des fichiers MP3 créés
lignes_globales = []      # Liste globale des lignes traitées

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
        match = re.search(r'\((\d+)s\)$', ligne)  # Chercher un nombre entre parenthèses à la fin
        if match:
            temps_silence = int(match.group(1))
            ligne_sans_silence = ligne[:match.start()].strip()
        else:
            temps_silence = 0
            ligne_sans_silence = ligne
        lignes_nettoyees.append((ligne_sans_silence, temps_silence))
    return lignes_nettoyees

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

# Fonction pour naviguer vers ElevenLabs et effectuer les actions
def naviguer_vers_elev(ligne):
    if not activer_fenetre_chrome_elevenlabs():
        return  # Si la fenêtre n'est pas trouvée, on arrête la fonction

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
    temps_attente = max(3.5, len(ligne) * 0.05)  # Temps d'attente basé sur la longueur du texte
    time.sleep(temps_attente)  # Attendre que la génération soit terminée

    # Clic pour lancer le téléchargement du MP3
    pyautogui.click(x=1809, y=957)  # Clic sur le bouton de téléchargement (coordonnées absolues)
    time.sleep(temps_attente)# Attendre que chrome download
    pyautogui.click(x=945, y=459)  # re-clic dans elevenlabs pour court-circuiter l'immobilisation de chrome en train de montrer le download en cours qui paralyse
# Fonction principale exécutée lors du clic sur "Run Task"
def run_task():
    global lignes_globales, fichiers_mp3_crees
    chemin_source = os.path.expanduser("~\\Downloads")
    fichiers_mp3_initial = set(f for f in os.listdir(chemin_source) if f.endswith(".mp3"))

    lignes = copier_texte()  # Obtenir les lignes non vides du texte avec les silences
    lignes_globales = lignes  # Stocker globalement pour d'autres fonctions

    for i, (ligne_sans_silence, temps_silence) in enumerate(lignes):
        naviguer_vers_elev(ligne_sans_silence)
        time.sleep(temps_silence)  # Attendre le silence spécifié

    time.sleep(5)  # Attendre que tous les fichiers soient bien téléchargés

    # Obtenir les nouveaux fichiers MP3
    fichiers_mp3_final = set(f for f in os.listdir(chemin_source) if f.endswith(".mp3"))
    nouveaux_fichiers_mp3 = list(fichiers_mp3_final - fichiers_mp3_initial)

    attribuer_noms_fichiers_mp3(lignes, nouveaux_fichiers_mp3, chemin_source)
    proposer_deplacer_fichiers(lignes)

# Fonction pour attribuer les noms des fichiers .mp3
def attribuer_noms_fichiers_mp3(lignes, nouveaux_fichiers_mp3, chemin_source):
    global fichiers_mp3_crees
    if len(nouveaux_fichiers_mp3) != len(lignes):
        messagebox.showwarning("Attention", "Le nombre de fichiers MP3 téléchargés ne correspond pas au nombre de lignes traitées.")

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

# Fonction pour générer un fichier texte avec les silences associés
def generer_fichier_silences(lignes):
    if destination_finale:
        chemin_fichier_silences = os.path.join(destination_finale, "silences_associes.txt")
        with open(chemin_fichier_silences, 'w', encoding='utf-8') as f:
            for ligne_sans_silence, temps_silence in lignes:
                if temps_silence > 0:
                    f.write(f"{ligne_sans_silence}... ({temps_silence} secondes de silence)\n")
                else:
                    f.write(f"{ligne_sans_silence}\n")
        messagebox.showinfo("Fichier créé", "Le fichier de confirmation des silences a été généré.")

# Fonction pour déplacer les fichiers .mp3
def proposer_deplacer_fichiers(lignes):
    global destination_finale
    reponse = messagebox.askyesno("Déplacer les fichiers", 
                                  "Voulez-vous déplacer les fichiers .mp3 du dossier 'Downloads' vers un autre emplacement ?")
    if reponse:
        destination_finale = filedialog.askdirectory()
        if destination_finale:
            chemin_source = os.path.expanduser("~\\Downloads")
            for fichier in fichiers_mp3_crees:
                try:
                    shutil.move(os.path.join(chemin_source, fichier), os.path.join(destination_finale, fichier))
                except Exception as e:
                    print(f"Erreur lors du déplacement du fichier {fichier}: {e}")

            messagebox.showinfo("Fichiers déplacés", 
                                f"Vos fichiers .mp3 ont été déplacés vers {destination_finale}")
            generer_fichier_silences(lignes)
            afficher_options_finales()

# Fonction pour ouvrir le dossier de destination et quitter
def ouvrir_dossier_et_quitter():
    if destination_finale:
        os.startfile(destination_finale)  # Ouvrir le dossier dans l'explorateur Windows
    root.quit()  # Quitter l'application

# Fonction pour effacer les MP3 créés et quitter
def effacer_tous_les_mp3_et_quitter():
    if destination_finale:
        chemin_source = os.path.expanduser("~\\Downloads")
        # Supprimer les fichiers créés
        for fichier in fichiers_mp3_crees:
            fichier_source = os.path.join(chemin_source, fichier)
            if os.path.exists(fichier_source):
                try:
                    os.remove(fichier_source)
                except Exception as e:
                    print(f"Erreur lors de la suppression du fichier {fichier_source}: {e}")
            fichier_dest = os.path.join(destination_finale, fichier)
            if os.path.exists(fichier_dest):
                try:
                    os.remove(fichier_dest)
                except Exception as e:
                    print(f"Erreur lors de la suppression du fichier {fichier_dest}: {e}")

        messagebox.showinfo("Nettoyage", "Les fichiers .mp3 créés ont été effacés.")
        root.quit()  # Quitter l'application

# Fonction pour passer à la partie "mix" du programme (à définir)
def passer_a_partie_mix():
    messagebox.showinfo("Mix", "Passage à la partie 'mix' du programme (fonctionnalité à venir).")
    root.quit()  # Quitter l'application pour l'instant

# Fonction pour afficher les options finales
def afficher_options_finales():
    options_fenetre = tk.Toplevel(root)
    options_fenetre.title("Actions finales")
    options_fenetre.geometry("400x200")
    options_fenetre.attributes("-topmost", True)

    bouton_ouvrir = tk.Button(options_fenetre, text="Ouvrir le dossier et quitter", command=ouvrir_dossier_et_quitter)
    bouton_ouvrir.pack(padx=20, pady=10)

    bouton_effacer = tk.Button(options_fenetre, text="Effacer les MP3 créés et quitter", command=effacer_tous_les_mp3_et_quitter)
    bouton_effacer.pack(padx=20, pady=10)

    bouton_mix = tk.Button(options_fenetre, text="Passer à la partie mix (à venir)", state='disabled')
    bouton_mix.pack(padx=20, pady=10)

# Fonction pour continuer après la vérification
def continuer():
    avertissement_label.pack_forget()  # Masquer l'avertissement
    bouton_continuer.pack_forget()  # Masquer le bouton de confirmation
    initialiser_interface()  # Initialiser l'interface principale

# Fonction pour créer la fenêtre d'arrêt d'urgence
def fenetre_arret_urgence():
    arret_fenetre = tk.Toplevel()
    arret_fenetre.title("Arrêt d'Urgence")
    arret_fenetre.geometry("300x150")
    arret_fenetre.attributes("-topmost", True)
    arret_fenetre.protocol("WM_DELETE_WINDOW", lambda: None)

    label_alerte = tk.Label(arret_fenetre, text="ABSOLUMENT TOUT ARRÊTER", font=("Arial", 14, "bold"), fg="red")
    label_alerte.pack(padx=20, pady=20)

    bouton_arret = tk.Button(arret_fenetre, text="ARRÊT D'URGENCE", font=("Arial", 12), bg="red", fg="white",
                             command=arreter_programme)
    bouton_arret.pack(padx=20, pady=10)

# Fonction pour arrêter le programme de manière propre
def arreter_programme():
    sys.exit(1)  # Terminer le programme proprement

# Initialisation de l'interface principale
def initialiser_interface():
    # Ajouter le message initial en haut de la fenêtre
    label_message = tk.Label(root, text=message_initial, padx=10, pady=10, justify="left")
    label_message.pack(padx=20, pady=10)

    # Ajouter un encart pour le texte
    global texte_encart
    texte_encart = tk.Text(root, wrap="word", height=20, width=80, padx=10, pady=10)
    texte_encart.pack(padx=20, pady=20)

    # Ajouter le bouton "Run Task"
    bouton_run = tk.Button(root, text="Run Task", command=run_task)
    bouton_run.pack(padx=20, pady=10)

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
