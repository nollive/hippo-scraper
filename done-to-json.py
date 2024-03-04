# On souhaite garder en mémoire ceux qu'on a pu scrapper ou non
import json

# Lecture du fichier done (en sortie de script-hippo.py, exemple python3 script-hippo.py > done.txt)
with open('done.txt', 'r') as file:
    lignes = file.readlines()

# On stocke les informations dans un dictionnaire
done = {}

# Analyse des lignes pour extraire les informations sur le statut de téléchargement
for ligne in lignes:
    mots = ligne.split()
    if len(mots) >= 6:
        identifiant = int(mots[4][:-1])  # On supprime le point à la fin de l'id
        statut = mots[5] == 'downloaded'  # On vérifie si on a pu scrapper l'image (downloaded est le 4ème mot de la phrase, PAS TRES ELEGANT OK)
        done[identifiant] = statut

# On export sous format JSON
with open('done.json', 'w') as json_file:
    json.dump(done, json_file, indent=4)

print("Le fichier JSON a été généré.")

