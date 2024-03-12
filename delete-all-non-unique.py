# Ce script permet, a partir du fichier json généré par image-to-RGB-median.py, de supprimer tout les entrées non uniques de triplet [R,G,B] (car parmis les image, souvent il y a des photos de profil par défaut). Ce script permet donc aussi d'éviter la potentielle utilisation de ces images par défaut (dans le cas ou il y en a plusieurs donc)
# Cela résoud aussi le problème des dominantes de couleur causant la non assignation d'un triplet RGB à une image (uniquement 1 composante)
import json

def load_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data

def remove_non_unique_rgb(data):
    rgb_counts = {}
    unique_entries = []
    
    # On va compter le nombre de fois ou l'on retrouve le tuple RGB, si le compte est égal à 1 on le conserve, sinon on ne le rajoute pas dans la liste unique_entries
    for entry in data:
        rgb = tuple(entry["median_rgb"])
        if rgb not in rgb_counts:
            rgb_counts[rgb] = 1
        else:
            rgb_counts[rgb] += 1

    for entry in data:
        rgb = tuple(entry["median_rgb"])
        if rgb_counts[rgb] == 1:
            unique_entries.append(entry)

    return unique_entries

def main():
    # Lecture du fichier contenant les RGB medians associées aux images téléchargées
    json_file = 'RGB-median.json'
    data = load_json(json_file)
    unique_entries = remove_non_unique_rgb(data)
    
    # Ecriture dans un nouveau ficher
    with open('output-unique.json', 'w') as f:
        json.dump(unique_entries, f, indent=4)

    print("Entries with non-unique RGB combinations removed and saved to output.json.")

if __name__ == "__main__":
    main()
