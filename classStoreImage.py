from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem

class StoreImage(QGraphicsPixmapItem):
    def __init__(self, pixmap, *args, **kwargs):
        super().__init__(pixmap, *args, **kwargs)
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

