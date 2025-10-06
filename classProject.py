import datetime
import os

# Classe Project (inchangée)
class Project:
    def __init__(self, name, author, store_name, store_address):
        self.name = name
        self.author = author
        self.creation_date = datetime.datetime.now()
        self.store_name = store_name
        self.store_address = store_address
        self.store_layout_path = ""
        self.grid = None
        

    # Fonction pour charger le plan du magasin (texte)
    def load_store_layout(self, layout_path):
        with open(layout_path, 'r') as file:
            self.store_layout_path = layout_path

    # Fonction pour créer la grille
    def create_grid(self, size):
        self.grid = [[0 for _ in range(size)] for _ in range(size)]

    # Fonction pour enregistrer le projet
    def save_project(self):
        with open(f"{self.name}.txt", 'w') as file:
            file.write(f"Nom : {self.name}\n")
            file.write(f"Auteur : {self.author}\n")
            file.write(f"Date de création : {self.creation_date}\n")
            file.write(f"Nom du magasin : {self.store_name}\n")
            file.write(f"Adresse du magasin : {self.store_address}\n")
            file.write(f"Disposition du magasin : {self.store_layout_path}\n")
            file.write(f"Grille : {self.grid}\n")

    # Fonction pour ouvrir un projet
    def open_project(self, project_name):
        with open(f"{project_name}.txt", 'r') as file:
            data = file.readlines()
            self.name = data[0].split(": ")[1].strip()
            self.author = data[1].split(": ")[1].strip()
            self.creation_date = data[2].split(": ")[1].strip()
            self.store_name = data[3].split(": ")[1].strip()
            self.store_address = data[4].split(": ")[1].strip()
            self.store_layout_path = data[5].split(": ")[1].strip()
            self.grid = eval(data[6].split(": ")[1].strip())

    # Fonction pour supprimer le projet
    def delete_project(self):
        os.remove(f"{self.name}.txt")
        print("Projet supprimé avec succès.")