from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from modeleApp1 import Modele

class SelectionPosition(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        scene_pos = event.scenePos()
        self.parent().CliqueProduit(scene_pos.x(), scene_pos.y())