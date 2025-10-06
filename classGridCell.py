from PyQt6.QtWidgets import QGraphicsRectItem, QMessageBox, QGraphicsItem
from PyQt6.QtGui import QBrush, QPen
from PyQt6.QtCore import Qt

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