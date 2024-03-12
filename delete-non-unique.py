# Ce script permet, a partir du fichier json généré par image-to-RGB-median.py, de supprimer les potentielles entrées non uniques de triplet [R,G,B] (car parmis les image, souvent il y a des photos de profil par défaut). Ce script permet, à la différence de delete-all-non-unique.py, de conserver tous les triplets RGB, même si il y a eu plusieurs occurences de ce dernier. On préferera utiliser ce script plutôt que l'autre dans le cas où on sait qu'il n'y a pas de problème de profil par défaut etc.
# Dans de rares cas, il est possible qu'on obtienne pour deux photos différentes le même triplet RGB, on pourrais donc effectuer un tirage aléatoire entre ces photos pour compléter la mosaïque. Cependant, notre collection d'image scrappée n'est pas idéale toutes les photos ne sont pas uniques, dans ce cas, on préférera supprimer tous les triplets RGB non unique pour éviter tout problème.

import json

def load_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data

def remove_non_unique_rgb(data):
    unique_rgb = []
    unique_entries = []

    # Contrairement à l'autre script, il suffit de chercher si le triplet est ou non dans unique_entries pour savoir si il faut l'ajouter ou non. On ne se pose pas de question sur le nombre d'occurence de ce triplet dans notre base de données
    for entry in data:
        rgb = tuple(entry["median_rgb"])
        if rgb not in unique_rgb:
            unique_rgb.append(rgb)
            unique_entries.append(entry)

    return unique_entries

def main():
    json_file = 'RGB-median.json'
    data = load_json(json_file)
    unique_entries = remove_non_unique_rgb(data)

    with open("output.json", 'w') as f:
        json.dump(unique_entries, f, indent=4)

    print("Non-unique RGB combinations removed and saved to output.json.")

if __name__ == "__main__":
    main()
