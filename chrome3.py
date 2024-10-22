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
    return [ligne for ligne in texte.split('\n') if ligne.strip()]  # Retourner uniquement les lignes non vides

# Fonction pour déterminer le temps d'attente (X) en fonction de la longueur de la phrase
def calculer_temps_attente(phrase):
    longueur = len(phrase)
    if 1 <= longueur <= 30:
        return 3
    elif 30 < longueur <= 500:
        return 6
    return 0  # Si la longueur dépasse 500 (cas inattendu), X = 0

# Fonction pour taper "elev" et sélectionner "Passer à cet onglet"
def goElevenlabs_and_paste(ligne):
    # Amener la fenêtre Chrome au premier plan
    chrome_windows = pyautogui.getWindowsWithTitle('Google Chrome')
    if chrome_windows:
        chrome_windows[0].activate()  # Activer la fenêtre existante de Chrome
    time.sleep(1)  # Attendre que la fenêtre soit active

    # Copier et coller la ligne actuelle
    pyperclip.copy(ligne)  # Copier la ligne actuelle dans le presse-papiers
    pyautogui.hotkey('ctrl', 'a')  # Sélectionner tout le texte
    pyautogui.hotkey('ctrl', 'v')  # Coller le texte copié
    pyautogui.hotkey('shift', 'enter')  # Shift + Enter

    # Calculer le temps d'attente (X)
    temps_attente = calculer_temps_attente(ligne)
    time.sleep(temps_attente)  # Attendre X secondes

    # Effectuer 34 frappes de Tab, puis Enter
    for _ in range(34):
        pyautogui.press('tab')
    pyautogui.press('enter')

# Afficher le message de pause pour la vérification
def pause_verification():
    pause_window = tk.Toplevel(root)
    pause_window.title("Vérification")

    label_pause = tk.Label(
        pause_window,
        text="Assure-toi que ElevenLabs est le dernier onglet ouvert, et rien d'autre!\n\n"
             "PS : appuie sur * ou µ pour tout arrêter",
        padx=10, pady=10, fg="red", font=("Arial", 14, "bold")
    )
    label_pause.pack(padx=20, pady=20)

    bouton_continuer = tk.Button(
        pause_window,
        text="Continuer",
        command=lambda: [pause_window.destroy(), run_task_continuer()],
        padx=10, pady=10, bg="lightgreen", font=("Arial", 12, "bold")
    )
    bouton_continuer.pack(padx=20, pady=10)

# Fonction principale exécutée lors du clic sur "Run Task"
def run_task():
    pause_verification()  # Appeler la fonction de pause

# Fonction pour continuer la tâche après la vérification
def run_task_continuer():
    lignes = copier_texte()  # Obtenir les lignes du texte
    for i in range(min(5, len(lignes))):  # Répéter jusqu'à la cinquième ligne
        goElevenlabs_and_paste(lignes[i])  # Naviguer avec la ligne actuelle

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
                                        