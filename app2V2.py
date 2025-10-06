import json
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
import os

class MainWindow(QMainWindow):
    # la classe MainWindow est responsable de l'interface graphique
    def __init__(self, controller):
        # initialiser la fenêtre principale
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Application de Courses")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # initialiser l'interface graphique
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)


        self.magasin_label = QLabel("Choisir un magasin:")
        self.layout.addWidget(self.magasin_label)

        self.magasin_combobox = QComboBox()
        self.layout.addWidget(self.magasin_combobox)

        self.produits_label = QLabel("ajouter des produits inexistant:")
        self.layout.addWidget(self.produits_label)

        self.produits_Texte = QLineEdit(placeholderText="Entrez le nom du produit")
        self.layout.addWidget(self.produits_Texte)

        self.liste_courses_button = QPushButton("Ajouter à la liste de courses")
        self.layout.addWidget(self.liste_courses_button)

        self.afficher_plan_button = QPushButton("Afficher le plan du magasin")
        self.layout.addWidget(self.afficher_plan_button)
        
        self.afficher_liste_button = QPushButton("Afficher la liste de courses")
        self.layout.addWidget(self.afficher_liste_button)
        
        self.lister_produits_button = QPushButton("Lister les produits")  
        self.layout.addWidget(self.lister_produits_button)

        self.plan_layout = QHBoxLayout()
        self.layout.addLayout(self.plan_layout)

        self.chemin_label = QLabel("Chemin le plus efficace:")
        self.plan_layout.addWidget(self.chemin_label)
        
        self.image_label = QLabel()
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(600, 500)
        self.plan_layout.addWidget(self.image_label)

        self.liste_courses_button.clicked.connect(self.controller.ajouter_a_liste_courses)
        self.afficher_plan_button.clicked.connect(self.controller.afficher_plan_magasin)
        self.afficher_liste_button.clicked.connect(self.afficher_liste_courses)
        self.lister_produits_button.clicked.connect(self.list_products)  # Connecter le bouton à la méthode

        ### menu en haut
        self.json_file_path = './listeProduit/liste_produits.json'
        self.txt_file_path = './listeProduit/liste_course.txt'
        with open(self.json_file_path, 'r') as file:
            self.data = json.load(file)
        self.checked_items = {}


    def update_magasins(self, magasins):
        # mettre à jour la liste des magasins
        self.magasin_combobox.clear()
        self.magasin_combobox.addItems(magasins)

    def update_txt(self, checked, item, list_name):
        # mettre à jour le fichier TXT
        if list_name not in self.checked_items:
            self.checked_items[list_name] = []

        if checked:
            if item not in self.checked_items[list_name]:
                self.checked_items[list_name].append(item)
        else:
            if item in self.checked_items[list_name]:
                self.checked_items[list_name].remove(item)

        with open(self.txt_file_path, 'w') as file:
            for list_name in self.checked_items:
                for checked_item in self.checked_items[list_name]:
                    file.write(f"{list_name}:{checked_item}\n")

    def set_image(self, image_path):
        # afficher l'image du plan du magasin
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        
    def afficher_liste_courses(self):
        # afficher la liste de courses
        if os.path.exists(self.txt_file_path):
            with open(self.txt_file_path, 'r') as file:
                data = file.read()
        else:
            data = "Aucun article sélectionné."

        self.liste_window = ListeWindow(data)
        self.liste_window.show()

    def afficher_chemin(self, path):
        # afficher le chemin le plus efficace
        self.text_edit.setText(" -> ".join(path))

    def list_products(self):
        # Lister les produits
        product_window = QDialog()
        product_window.setWindowTitle("Liste des produits")
        product_window.setWindowIcon(QIcon("logo.png"))
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Produits"])
        self.tree.setFixedSize(200, 300)
    
        layout = QVBoxLayout(product_window)
    
        with open(self.json_file_path) as f:
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

    def add_tree_item(self, parent_name, child_names):
        # Ajouter un élément à l'arbre
        parent_item = QTreeWidgetItem(self.tree, [parent_name])
        for child_name in child_names:
            child_item = QTreeWidgetItem(parent_item, [child_name])

            child_item.setCheckState(0, Qt.CheckState.Unchecked)

            parent_item.addChild(child_item)

    def sauv_liste_course(self):
        # Enregistrer la liste de courses
        checked_items = []
        for i in range(self.tree.topLevelItemCount()):
            parent_item = self.tree.topLevelItem(i)
            for j in range(parent_item.childCount()):
                child_item = parent_item.child(j)
                if child_item.checkState(0) == Qt.CheckState.Checked:
                    checked_items.append(child_item.text(0))
    
        if checked_items:
            with open(self.txt_file_path, 'w') as f:
                for item in checked_items:
                    f.write(f"{item}\n")
            QMessageBox.information(self, "Succès", "Liste de courses enregistrée avec succès")
        else:
            QMessageBox.warning(self, "Erreur", "Aucun produit sélectionné")


class ListeWindow(QMainWindow):
    # la classe ListeWindow est responsable de l'affichage de la liste de courses
    def __init__(self, data):
        # initialiser la fenêtre de la liste de courses
        super().__init__()
        self.setWindowTitle("Liste de Courses")
        self.setGeometry(100, 100, 400, 300)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setText(data)
        self.layout.addWidget(self.text_edit)

if __name__ == '__main__':
    import sys

    class Controller:
        def ajouter_a_liste_courses(self):
            print("Ajouter à la liste de courses")

        def afficher_plan_magasin(self):
            print("Afficher le plan du magasin")

    app = QApplication(sys.argv)
    window = MainWindow(Controller())
    window.show()
    sys.exit(app.exec())
