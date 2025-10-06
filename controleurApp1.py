import sys
from PyQt6.QtWidgets import *
from modeleApp1 import Modele
from vueApp1 import MainWindow

#---------------------------------------------------
#---------     Classe Controleur                        
#--------------------------------------------------- 

class Controleur:
    # Constructeur
    def __init__(self):
        # Attributs
        self.modele = Modele()
        self.vue = MainWindow()

        # signaux et slots
        self.vue.save_project_buttonClicked.connect(self.save_project)
        self.vue.open_project_buttonClicked.connect(self.open_project)
        self.vue.delete_project_buttonClicked.connect(self.delete_project)
        self.vue.list_buttonClicked.connect(self.list_products)
        self.vue.panier_buttonClicked.connect(self.panier_products)

    # Appels des différentes fonctions
    def load_store_layout(self):
        self.vue.load_store_layout()

    def create_grid(self):
        self.vue.create_grid()

    def save_project(self):
        self.modele.save_project()

    def open_project(self):
        self.modele.open_project()

    def delete_project(self):
        self.modele.delete_project()

    def list_products(self):
        self.modele.list_products()

    def panier_products(self):
        self.modele.panier_products()

# Exécution de l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controleur()
    controller.vue.show()
    sys.exit(app.exec())
