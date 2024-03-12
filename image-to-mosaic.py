# Pour ce script, on va mettre en argument l'image que l'on souhaite transformer en mosaïque grâce à --file et aussi le fichier contenant les associations image-RGB median (sortie de image-to-RGB-median.py) grâce à --json

# On peut choisir --cols et --rows pour partitionner notre image de départ (ici on prendra --cols et --rows égaux pour créer une image carré, format d'origine des images obtenues via script-hippo.py ainsi que des images à transformer)

# On pourrais rajouter un export des id/path des images utilisées lors de la construction de la mosaïque ainsi que leur position.


import argparse
import json
import numpy as np
import os
from PIL import Image
import time



# Lecture de l'image que l'on souhaite transformer en mosaique
def load_image(file):
    try:
        return Image.open(file)
    except FileNotFoundError:
        print(f"Error: Image file '{file}' not found.")
        exit()

# Découpe l'image selon les argument cols et row et la stocke sous forme de liste avant d'être reconstruite
def partition_image(image, cols, rows):
    width, height = image.size
    col_width = width // cols
    row_height = height // rows
    partitions = []
    for i in range(rows):
        for j in range(cols):
            # On calcule la position des 4 coins de notre partition
            left = j * col_width
            top = i * row_height
            right = (j + 1) * col_width
            bottom = (i + 1) * row_height
            partition = image.crop((left, top, right, bottom))
            partitions.append(partition)
    return partitions


# On réutilise la même fonction que RGB-to-image pour récuperer le RGB médian de chacune de nos partitions de l'image de départ
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
    return median_rgb # Etrangement le .tolist() pose problème ici, à voir pourquoi..


def load_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


# A partir du dictionnaire mis en argument, cherche l'image ayant le RGB le plus proche de celui mis également en argument
def find_closest_image(rgb, image_data):
    closest_image = None
    min_distance = float('inf')
    for image_info in image_data:
        try:
            median_rgb = image_info['median_rgb']
            distance = np.linalg.norm(np.array(rgb) - np.array(median_rgb))
            if distance < min_distance:
                min_distance = distance
                closest_image = image_info
        except Exception as e:
            print(f"Error processing {image_info['file_path']}: {e}")
    
    return closest_image


# Lit le fichier d'associations image-RGB et appele la fonction au dessus pour connaitre l'image la plus proche et nous la renvoie (path et RGB)
def get_closest_image(rgb):
    json_file = "RGB-median.json"
    image_data = load_json(json_file)
    closest_image = find_closest_image(rgb, image_data)
    return closest_image


# Fonction permettant de reconstruire la mosaïque
def reconstruct_image(partitions, image_data, cols, rows):
    width = partitions[0].width
    height = partitions[0].height
    reconstructed_image = Image.new("RGB", (width * cols, height * rows))
    for i, partition in enumerate(partitions):
        closest_image = find_closest_image(rgb_median(partition), image_data)
        if closest_image:
            closest_image_path = closest_image["file_path"]
            closest_image_data = load_image(closest_image_path)  # Utilisez la fonction load_image pour charger l'image
            reconstructed_image.paste(closest_image_data, (i % cols * width, i // cols * height))
    return reconstructed_image


# Recuperer l'ID de l'image de départ à partir de son path (pour l'export de la mosaïque
def extract_id(file_path):
    filename = os.path.basename(file_path)
    file_id, _ = os.path.splitext(filename)
    return file_id


def main():
    parser = argparse.ArgumentParser(description="Partition an image into subparts and reconstruct the image using images associated with closest median RGB.")
    parser.add_argument("--file", type=str, help="Path to the input image file.")
    parser.add_argument("--cols", type=int, default=2, help="Number of columns to divide the image into.")
    parser.add_argument("--rows", type=int, default=2, help="Number of rows to divide the image into.")
    parser.add_argument("--json", type=str, help="Path to the JSON file containing image data.")
    args = parser.parse_args()
    
    
    image = load_image(args.file)
    partitions = partition_image(image, args.cols, args.rows)

    with open(args.json, 'r') as f:
        image_data = json.load(f)

    # On calcule les dimensions de la mosaïque (pour conserver la qualité originale des images utilisées)
    width = image.width * args.cols
    height = image.height * args.rows

    # On initialise la mosaïque
    reconstructed_image = Image.new("RGB", (width, height))

    # Reconstruire l'image en collant chaque partition avec l'image la plus proche
    for i, partition in enumerate(partitions):
        closest_image = find_closest_image(rgb_median(partition), image_data)
        if closest_image:
            closest_image_path = closest_image["file_path"]
            closest_image_data = load_image(closest_image_path)
            # On calcule où positionner l'image sur la mosaïque
            x_offset = (i % args.cols) * image.width
            y_offset = (i // args.cols) * image.height
            # On calcule quelle image placer à ces coordonnées
            reconstructed_image.paste(closest_image_data, (x_offset, y_offset))

    # On placera les résultats (mosaïques) dans un fichier dédié
    os.makedirs('mosaic', exist_ok=True)
    file_id = extract_id(args.file)
    # Chemin du fichier de l'image reconstruite
    file_name = file_id+'-image-mosaic.png'
    output_path = os.path.join('mosaic',file_name)
    
    # On enregistre la mosaïque générée
    reconstructed_image.save(output_path)
    print(f"Reconstructed image saved to '{output_path}'.") 


if __name__ == "__main__":
    # Permet de connaitre le temps d'execution
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
