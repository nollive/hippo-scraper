import os
import json
from PIL import Image # PYTHON IMAGE LIBRARY
import numpy as np


def rgb_median(image):
    # On converti en RGB (eviter le cas de la "4ème composante" RGB ( si jamais l'image contient de la transparence)
    img_rgb = image.convert('RGB')
    # Conversion en array
    img_array = np.array(img_rgb)
    median_rgb = np.median(img_array, axis=(0, 1))
    
    # Si une seule composante RGB est prédominante --> Eviter de comparer des vecteurs de tailles différentes lorsqu'on cherchera ensuite l'image avec le RGB le plus proche
    if len(set(median_rgb)) == 1:
        # On va "remplir" le triplet en prenant cette valeur et en l'assignant au deux autres (pas très élégant SOIT)
        median_value = np.median(img_array) #eww
        median_rgb = [median_value, median_value, median_value]
    return median_rgb.tolist()

# Folder_path correspond à l'endroit où les images sont stockées
def process_images(folder_path):
    image_data = []
    # On lit chacune des images dans le dossier image
    for filename in os.listdir(folder_path):
        # Si jamais format différent d'image
        if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            # On récupère le path de chaque image (folder_path+filename)
            file_path = os.path.join(folder_path, filename)
            try:
                # Lecture de l'image
                with Image.open(file_path) as img:
                    # Calcul du RBG median
                    median_rgb = rgb_median(img)
                    # On écrit le path ainsi que le RBG médian pour l'export en json (path pour pouvoir aller chercher l'image lors de la construction de la mosaïque...
                    image_info = {
                        "file_path": file_path,
                        "median_rgb": median_rgb
                    }
                    # On ajoute image_info au fichier json (sous forme de liste)
                    image_data.append(image_info)
            # Si jamais error -> nous donne l'image en question (e est l'error qui a eu lieu)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                
    return image_data

# Export des données sous format json
def save_to_json(data, json_file):
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    # A modifier selon le format du path
    folder_path = "/images"
    json_file = "RGB-median.json"
    image_data = process_images(folder_path)
    save_to_json(image_data, json_file)
    print("RGB median generated successfully.")

if __name__ == "__main__":
    main()
