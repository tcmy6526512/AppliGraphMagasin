import sys, json, os, datetime
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from classProject import Project
from classGridCell import GridCell
from classStoreImage import StoreImage
from classSelectionPosition import SelectionPosition

#---------------------------------------------------
#---------     Classe MainWindow                    
#--------------------------------------------------- 

class MainWindow(QMainWindow):
    # Constructeur
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

        self.grid_button = QPushButton("Grille")
        self.grid_button.setFixedHeight(30)

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
        layout_gauche.addWidget(self.grid_button)
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
        self.grid_button.clicked.connect(self.grid)

    # signaux
    save_project_buttonClicked = pyqtSignal()
    open_project_buttonClicked = pyqtSignal()
    delete_project_buttonClicked = pyqtSignal()
    list_buttonClicked = pyqtSignal()
    panier_buttonClicked = pyqtSignal()

    # .emit des fonctions du modele
    def panier_products(self):
        self.panier_buttonClicked.emit()

    def list_products(self):
        self.list_buttonClicked.emit()

    def sauv_liste_course(self):
        self.save_project_buttonClicked.emit()

    def grid(self, grid_size):
        grid_size = self.grid_size_spinbox.value()
        self.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        print(self.grid)

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

    # Fonction pour supprimer le plan du magasin
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
