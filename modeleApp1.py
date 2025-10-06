import json, os, sys
from PyQt6.QtWidgets import *
from classProject import Project
from classGridCell import GridCell
from classStoreImage import StoreImage
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt

#---------------------------------------------------
#---------     Classe Modele                        
#--------------------------------------------------- 

class Modele:
    # Constructeur
    def __init__(self):
        self.current_project = None
        self.store_image_item = None
        self.grid_group = None
        self.tree = None

    # Fonction pour le panier
    def panier_products(self):
        panier_window = QDialog()
        panier_window.setWindowTitle("Votre panier")
        panier_window.setFixedSize(200, 300)
        panier_window.setWindowIcon(QIcon("logo.png"))

        layout1 = QVBoxLayout(panier_window)
        
        with open('liste_de_course.json') as f:
            liste_de_course = json.load(f)
        
        list_widget = QListWidget()
        list_widget.addItems(liste_de_course)
        layout1.addWidget(list_widget)

        add_button = QPushButton("Placer sur la grille")
        layout1.addWidget(add_button)
        add_button.clicked.connect(panier_window.close)
        
        close_button = QPushButton("Fermer")
        layout1.addWidget(close_button)
        close_button.clicked.connect(panier_window.close)
        
        panier_window.exec()

    #  Fonction pour ajouter un élément à l'arbre
    def add_tree_item(self, parent_name, child_names):
        parent_item = QTreeWidgetItem(self.tree, [parent_name])
        for child_name in child_names:
            child_item = QTreeWidgetItem(parent_item, [child_name])

            child_item.setCheckState(0, Qt.CheckState.Unchecked)

            parent_item.addChild(child_item)

    # Fonction pour la liste des produits
    def list_products(self):
        product_window = QDialog()
        product_window.setWindowTitle("Liste des produits")
        product_window.setWindowIcon(QIcon("logo.png"))
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Produits"])
        self.tree.setFixedSize(200, 300)
    
        layout = QVBoxLayout(product_window)
    
        with open('liste_produits.json') as f:
            products = json.load(f)
    
        for key in products.keys():
            self.add_tree_item(key, products[key])
            layout.addWidget(self.tree)
    
        self.save_list_button = QPushButton("Enregistrer la liste de courses")
        self.save_list_button.setFixedHeight(30)
        layout.addWidget(self.save_list_button)
        self.save_list_button.clicked.connect(self.sauv_liste_course)
        
        self.close_button = QPushButton("Fermer")
        layout.addWidget(self.close_button)
        self.close_button.clicked.connect(product_window.close)
        
        product_window.exec()

    # Fonction pour enregistrer la liste de courses
    def sauv_liste_course(self):
        checked_items = []
        for i in range(self.tree.topLevelItemCount()):
            parent_item = self.tree.topLevelItem(i)
            for j in range(parent_item.childCount()):
                child_item = parent_item.child(j)
                if child_item.checkState(0) == Qt.CheckState.Checked:
                    checked_items.append(child_item.text(0))
            
        if checked_items:
            with open('liste_de_course.json', 'w') as f:
                json.dump(checked_items, f)
            QMessageBox.information(None, "Succès", "Liste de courses enregistrée avec succès")
        else:
            QMessageBox.warning(None, "Erreur", "Aucun produit sélectionné")

    # Fonction pour sauvegarder le projet
    def save_project(self):
        if self.current_project:
            self.current_project.save_project()
            QMessageBox.information(None, "Succès", "Projet enregistré avec succès")
        else:
            QMessageBox.warning(None, "Avertissement", "Aucun projet à enregistrer")

    # Fonction pour ouvrir un projet
    def open_project(self):
        project_name, _ = QFileDialog.getOpenFileName(None, "Ouvrir un projet", "", "Text Files (*.txt)")
        if project_name:
            project_basename = os.path.basename(project_name).split('.')[0]
            self.create_new_project()
            self.current_project.open_project(project_basename)
            QMessageBox.information(None, "Succès", f"Projet {project_basename} ouvert avec succès")

    # Fonction pour supprimer un projet
    def delete_project(self):
        if self.current_project:
            self.current_project.delete_project()
            self.current_project = None
            QMessageBox.information(None, "Succès", "Projet supprimé avec succès")
        else:
            QMessageBox.warning(None, "Avertissement", "Aucun projet à supprimer")