import sys
import datetime
import os
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import json
from PyQt6.QtWidgets import *

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

class GridCell(QGraphicsRectItem):
    def __init__(self, x, y, width, height, *args, **kwargs):
        super().__init__(x, y, width, height, *args, **kwargs)
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setBrush(QBrush(Qt.GlobalColor.transparent))
        self.setPen(QPen(Qt.GlobalColor.black))
        self.click_position = None 

    def mousePressEvent(self, event):
        #print("Mouse pressed at:", event.pos().toPoint())
        pos = event.pos().toPoint()
        scene_pos = self.mapToScene(pos)
        print("Mouse pressed at:", scene_pos.toPoint())
        QMessageBox.information(None, "Cell Clicked", f"Cell clicked at position: {scene_pos.x()}, {scene_pos.y()}")

class StoreImage(QGraphicsPixmapItem):
    def __init__(self, pixmap, *args, **kwargs):
        super().__init__(pixmap, *args, **kwargs)
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

# Classe principale avec modification pour charger et afficher le plan du magasin
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1100, 600)
        self.setWindowTitle("Gestion du Projet de Magasin")
        self.setWindowIcon(QIcon("logo.png"))

        self.current_project = None
        self.store_image_item = None  # Variable pour stocker l'élément image

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout_gauche = QVBoxLayout()
        layout_droit = QVBoxLayout()

        ligne = QFrame()
        ligne.setFrameShape(QFrame.Shape.VLine)
        ligne.setLineWidth(4)
        ligne.setStyleSheet("color: black;")
        ligne2 = QFrame()
        ligne2.setFrameShape(QFrame.Shape.HLine)
        ligne2.setLineWidth(4)
        ligne2.setStyleSheet("color: black;")

        self.name_label = QLineEdit(placeholderText="Nom du projet")
        self.author_label = QLineEdit(placeholderText="Auteur du projet")
        self.store_name_label = QLineEdit(placeholderText="Nom du magasin")
        self.store_address_label = QLineEdit(placeholderText="Adresse du magasin")
        self.grid_size_spinbox = QSpinBox()
        self.grid_size_spinbox.setMinimum(1)
        self.grid_size_spinbox.setMaximum(50)
        
        self.load_layout_button = QPushButton("Charger le plan du magasin")
        self.load_layout_button.setFixedHeight(30)
        layout_gauche.addStretch(1)

        self.create_grid_button = QPushButton("Créer une grille")
        self.create_grid_button.setFixedHeight(30)
        layout_gauche.addStretch(1)

        self.save_project_button = QPushButton("Enregistrer le projet")
        self.save_project_button.setFixedHeight(30)
        layout_gauche.addStretch(1)

        self.open_project_button = QPushButton("Ouvrir un projet")
        self.open_project_button.setFixedHeight(30)
        layout_gauche.addStretch(1)
        
        self.delete_project_button = QPushButton("Supprimer le projet")
        self.delete_project_button.setFixedHeight(30)

        self.list_button = QPushButton("Liste des produits")
        self.list_button.setFixedHeight(30)

        self.panier_button = QPushButton("Votre panier")
        self.panier_button.setFixedHeight(30)

        layout_gauche.addStretch(1)
        layout_gauche.addWidget(QLabel("Nom du Projet :"))
        layout_gauche.addWidget(self.name_label)
        layout_gauche.addWidget(QLabel("Auteur du Projet :"))
        layout_gauche.addWidget(self.author_label)
        layout_gauche.addWidget(QLabel("Nom du Magasin :"))
        layout_gauche.addWidget(self.store_name_label)
        layout_gauche.addWidget(QLabel("Adresse du Magasin :"))
        layout_gauche.addWidget(self.store_address_label)
        layout_gauche.addWidget(QLabel("Taille de la Grille :"))
        layout_gauche.addWidget(self.grid_size_spinbox)

        layout_gauche.addStretch(1)
        layout_gauche.addWidget(ligne2)
        layout_gauche.addStretch(1)
        layout_gauche.addWidget(self.list_button)
        layout_gauche.addWidget(self.panier_button)
        layout_gauche.addStretch(2)

        layout_gauche.addWidget(self.load_layout_button)
        layout_gauche.addWidget(self.create_grid_button)
        layout_gauche.addStretch(2)
        layout_gauche.addWidget(self.save_project_button)
        layout_gauche.addWidget(self.open_project_button)
        layout_gauche.addWidget(self.delete_project_button)

        self.image_label = QLabel()
        self.image_label.setScaledContents(True)
        layout_droit.addWidget(self.image_label)

        self.graphics_view = QGraphicsView()
        self.graphics_scene = QGraphicsScene()
        self.graphics_view.setScene(self.graphics_scene)

        layout_droit.addWidget(self.graphics_view)

        main_layout = QHBoxLayout()
        main_layout.addLayout(layout_gauche, 1)
        main_layout.addWidget(ligne)
        main_layout.addLayout(layout_droit, 3)

        central_widget.setLayout(main_layout)

        self.load_layout_button.clicked.connect(self.load_store_layout)
        self.create_grid_button.clicked.connect(self.create_grid)
        self.save_project_button.clicked.connect(self.save_project)
        self.open_project_button.clicked.connect(self.open_project)
        self.delete_project_button.clicked.connect(self.delete_project)
        self.list_button.clicked.connect(self.list_products)
        self.panier_button.clicked.connect(self.panier_products)

    def panier_products(self):
        # Créer une nouvelle fenêtre
        panier_window = QDialog(self)
        panier_window.setWindowTitle("Votre panier")
        panier_window.setFixedSize(200, 300)

        # Créer un layout vertical pour la fenêtre
        layout1 = QVBoxLayout(panier_window)
        
        # Lire le contenu du fichier "liste_de_course.json"
        with open('liste_de_course.json') as f:
            liste_de_course = json.load(f)
        
        # Créer une QListWidget pour afficher le contenu du fichier
        list_widget = QListWidget()
        list_widget.addItems(liste_de_course)
        layout1.addWidget(list_widget)

        # Ajouter un bouton pour ajouter un élément du panier
        add_button = QPushButton("Placer sur la grille")
        layout1.addWidget(add_button)
        #add_button.clicked.connect(self.add_tree_item)
        add_button.clicked.connect(panier_window.close)
        
        # Ajouter un bouton pour fermer la fenêtre
        close_button = QPushButton("Fermer")
        layout1.addWidget(close_button)
        close_button.clicked.connect(panier_window.close)
        
        # Afficher la fenêtre
        panier_window.exec()

    #  Fonction pour ajouter un élément à l'arbre
    def add_tree_item(self, parent_name, child_names):
        parent_item = QTreeWidgetItem(self.tree, [parent_name])
        for child_name in child_names:
            child_item = QTreeWidgetItem(parent_item, [child_name])

            child_item.setCheckState(0, Qt.CheckState.Unchecked)

            parent_item.addChild(child_item)

    def list_products(self):
        # Créer une nouvelle fenêtre
        product_window = QDialog(self)
        product_window.setWindowTitle("Liste des produits")
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Produits"])
        self.tree.setFixedSize(200, 300)
    
        # Créer un layout vertical pour la fenêtre
        layout = QVBoxLayout(product_window)
    
        # Créer une liste de produits
        with open('liste_produits.json') as f:
            products = json.load(f)
    
        for key in products.keys():
            self.add_tree_item(key, products[key])

            layout.addWidget(self.tree)
    
        #layout.addWidget(QPushButton("Validez la liste des produits"))
        self.save_list_button = QPushButton("Enregistrer la liste de courses")
        #self.save_list_button.setStyleSheet("background-color: #33b3ff; color: white; font-size: 15px; border-radius: 10px; font-weight: bold; border: 1px solid black;")
        self.save_list_button.setFixedHeight(30)
        layout.addWidget(self.save_list_button)
        self.save_list_button.clicked.connect(self.sauv_liste_course)
        self.close_button = QPushButton("Fermer")
        layout.addWidget(self.close_button)
        self.close_button.clicked.connect(product_window.close)

        # Afficher la fenêtre
        product_window.exec()

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
            QMessageBox.information(self, "Succès", "Liste de courses enregistrée avec succès")
        else:
            QMessageBox.warning(self, "Erreur", "Aucun produit sélectionné")

    # Fonction pour charger et afficher le plan du magasin
    def load_store_layout(self):
        layout_path, _ = QFileDialog.getOpenFileName(self, "Charger le plan du magasin", "", "Images (*.png *.jpg)")
        if layout_path:
            if not self.current_project:
                self.create_new_project()
            self.current_project.load_store_layout(layout_path)
            self.graphics_scene.clear() # Effacer la scène
            pixmap = QPixmap(layout_path)  # Charger l'image
            self.store_image_item = StoreImage(pixmap)  # Créer l'élément image
            self.graphics_scene.addItem(self.store_image_item)  # Ajouter l'image à la scène
            self.graphics_view.fitInView(self.store_image_item, Qt.AspectRatioMode.KeepAspectRatio)  # Ajuster la vue pour l'image
            QMessageBox.information(self, "Succès", "Plan du magasin chargé avec succès")

    def suppr_store_layout(self):
        self.current_project.store_layout_path = ""
        self.image_label.clear()

    # Fonction pour créer la grille
    def create_grid(self):
        if not self.current_project:
            QMessageBox.warning(self, "Avertissement", "Aucun projet en cours. Veuillez créer ou ouvrir un projet.")
            return

        grid_size = self.grid_size_spinbox.value()
        if self.current_project.store_layout_path == "":
            QMessageBox.warning(self, "Avertissement", "Veuillez charger d'abord le plan du magasin.")
            return

        self.graphics_scene.clear()
        pixmap = QPixmap(self.current_project.store_layout_path)
        self.store_image_item = StoreImage(pixmap)
        self.graphics_scene.addItem(self.store_image_item)
        self.graphics_view.fitInView(self.store_image_item, Qt.AspectRatioMode.KeepAspectRatio)

        image_width = pixmap.width()
        image_height = pixmap.height()
        cell_width = image_width / grid_size
        cell_height = image_height / grid_size

        # Créer un groupe d'éléments pour la grille
        self.grid_group = QGraphicsItemGroup()
        self.grid_group.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)  # Permettre le déplacement du groupe

        for i in range(grid_size):
            for j in range(grid_size):
                cell = GridCell(i * cell_width, j * cell_height, cell_width, cell_height)
                cell.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)  # Rendre les cellules sélectionnables
                self.grid_group.addToGroup(cell)

        self.graphics_scene.addItem(self.grid_group)  # Ajouter le groupe à la scène

        QMessageBox.information(self, "Succès", f"Grille de {grid_size}x{grid_size} créée avec succès.")

    # Fonction pour créer un nouveau projet
    def create_new_project(self):
        name = self.name_label.text()
        author = self.author_label.text()
        store_name = self.store_name_label.text()
        store_address = self.store_address_label.text()
        
        self.current_project = Project(name, author, store_name, store_address)

    # Fonction pour enregistrer le projet
    def save_project(self):
        if self.current_project:
            self.current_project.save_project()
            QMessageBox.information(self, "Succès", "Projet enregistré avec succès")
        else:
            QMessageBox.warning(self, "Avertissement", "Aucun projet à enregistrer")

    # Fonction pour ouvrir un projet existant
    def open_project(self):
        project_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir un projet", "", "Text Files (*.txt)")
        if project_name:
            project_basename = os.path.basename(project_name).split('.')[0]
            self.create_new_project()
            self.current_project.open_project(project_basename)
            QMessageBox.information(self, "Succès", f"Projet {project_basename} ouvert avec succès")

    # Fonction pour supprimer le projet
    def delete_project(self):
        if self.current_project:
            self.current_project.delete_project()
            self.current_project = None
            QMessageBox.information(self, "Succès", "Projet supprimé avec succès")
        else:
            QMessageBox.warning(self, "Avertissement", "Aucun projet à supprimer")

# Programme principal
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
