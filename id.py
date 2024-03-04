# Création du fichier txt avec tous les identifiants à essayer
with open('identifiants.txt', 'w') as f:
    # On parcourt l'ensemble des identifiant à essayer, ici à 5 chiffres --> 10^5 id attention!
    for i in range(100000):
        # On utilise des identifiants sous le format XXXXX
        identifiant = '{:05d}'.format(i)
        # On utilise le saut de ligne comme séparateur
        f.write(identifiant + '\n')

print("Les identifiants ont été créés dans le fichier identifiant.txt")
