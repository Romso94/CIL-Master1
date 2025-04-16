import zipfile
import io

def extract_zip_contents_from_image(image_path):
    # Signature d'un fichier ZIP (PK\x03\x04)
    zip_signature = b'\x50\x4B\x03\x04'

    # Lire l'image en mode binaire
    with open(image_path, 'rb') as img_file:
        img_data = img_file.read()

    # Trouver l'index de la signature ZIP dans les données de l'image
    zip_start_index = img_data.find(zip_signature)

    if zip_start_index != -1:
        # Extraire le contenu ZIP à partir de l'index trouvé
        zip_data = img_data[zip_start_index:]

        # Charger le contenu ZIP dans un objet BytesIO
        zip_stream = io.BytesIO(zip_data)

        # Ouvrir le ZIP et lister les fichiers
        with zipfile.ZipFile(zip_stream, 'r') as zip_file:
            print("Contenu du fichier ZIP caché :")
            zip_file.printdir()
            # Pour lire le contenu des fichiers du ZIP, décommenter les lignes suivantes
            for file_name in zip_file.namelist():
                with zip_file.open(file_name) as file:
                    print(f"--- Contenu de {file_name} ---")
                    print(file.read().decode('utf-8'))
    else:
        print("Aucun fichier ZIP trouvé dans l'image.")

# Exemple d'utilisation
image_path = 'WalpHack_1.png'  # Remplace par le chemin de ton image
extract_zip_contents_from_image(image_path)
