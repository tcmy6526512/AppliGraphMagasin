from PyQt6.QtWidgets import QMessageBox
from app2V2 import MainWindow
from modeleApp2 import MagasinModel, ProduitModel

class Controller:
    # la classe Controller est responsable de la communication entre la vue et le modèle
    def __init__(self):
        # initialiser les modèles et la vue
        self.magasin_model = MagasinModel()
        self.produit_model = ProduitModel()
        self.view = MainWindow(self)

        self.view.update_magasins(self.magasin_model.get_magasins())

    def ajouter_a_liste_courses(self):
        # obtenir le produit sélectionné
        produit_selectionne = self.view.produits_Texte.text()
        if produit_selectionne:
            self.view.update_txt(True, produit_selectionne, list_name="produit rajouté ")
            self.view.produits_Texte.clear()
        else:
            QMessageBox.warning(self.view, "Erreur", "Veuillez entrer un produit")

    def afficher_plan_magasin(self):
        # obtenir le magasin sélectionné
        magasin = self.view.magasin_combobox.currentText()
        if magasin == "Magasin 1":
            self.view.set_image("C:/cours/but1/sae/sae c12/Exemples de plans-20240419/plan1.jpg")
        elif magasin == "Magasin 2":
            self.view.set_image("C:/cours/but1/sae/sae c12/Exemples de plans-20240419/plan2.png")
        else:
            self.view.set_image("C:/cours/but1/sae/sae c12/Exemples de plans-20240419/plan3.png")

    def update_txt(self, checked, item):
        # mettre à jour le fichier TXT
        self.view.update_txt(checked, item)

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    controller = Controller()
    controller.view.show()
    sys.exit(app.exec())
