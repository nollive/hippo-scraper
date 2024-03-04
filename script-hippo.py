# "Scrapper" sommaire pour extraire les photos de profil présentes sur un site de type moodle.com, ici il s'agit du site moodle associé à CN.
# Le lien à vérifier si il y a image ou non se trouve facilement selon la disposition du site.
#

import requests
import os

# Fonction pour récuperer l'image de profil.
def download_images(user_id):
    url = f"https://hippocampus.ec-nantes.fr/pluginfile.php/{user_id}/user/icon/boost/f3" #f3 permet d'obtenir l'image en résolution "maximale".
    response = requests.get(url, stream=True)
    if response.status_code == 200:
    # On enregistre les image dans le dossier image
        if not os.path.exists('images'):
            os.makedirs('images')
        with open(f'images/{user_id}.png', 'wb') as file:
            file.write(response.content)
        print(f"Image for user {user_id} downloaded successfully.")
    else:
        print(f"Failed to download image for user {user_id}.")

if __name__ == "__main__":
    # Ici on charge le fichier identifiants.txt généré par id.py, mais on peut aussi utiliser notre propre liste d'identifiant à vérifier. On a utilisé le saut de ligne comme délimiteur.
        with open('identifiants.txt', 'r') as file:
        user_ids = [int(line.strip()) for line in file.readlines()]

    for user_id in user_ids:
        download_images(user_id)
