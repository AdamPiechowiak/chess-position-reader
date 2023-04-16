from PySide6.QtWidgets import QWidget, QPushButton, QTextEdit, QApplication
from PySide6.QtCore import QPoint, Qt, QRectF
from PySide6 import QtGui
from PIL import ImageGrab
import time
import tkinter as tk

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.select_btn = QPushButton()
        self.read_btn = QPushButton()
        self.text_box = QTextEdit()
        self.screanshot = None
        self.snipping_window = None
        
        self.setup()
        
    def setup(self):
        
        self.select_btn = QPushButton("Select", self)
        self.select_btn.move(10,10)
        
        self.read_btn = QPushButton("Read position", self)
        self.read_btn.setMinimumWidth(100)
        self.read_btn.move(100,10)
        
        self.text_box = QTextEdit(self)
        self.text_box.setMaximumHeight(150)
        self.text_box.setMinimumWidth(280)
        self.text_box.move(10,40)
        
        self.select_btn.clicked.connect(self.select)
        self.read_btn.clicked.connect(self.read)
        
        self.setFixedSize(300,200)
        self.setWindowTitle("Window")
        
        self.show()
        
    def select(self):
        self.hide()
        time.sleep(0.2)
        self.snipping_window = SnippingWindow(self)
        
    def read(self):
        self.screanshot.show()
        self.text_box.setText("asdad")


class SnippingWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        
        self.parent = parent
        self.begin = QPoint()
        self.end = QPoint()
        
        self.setup()
        self.show()
        
    def setup(self):
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        print(screen_width)
        print(screen_height)
        self.setGeometry(0, 0, screen_width, screen_height)
        #self.move(0,0)
        self.move(-7,-30)
        self.setWindowOpacity(0.3)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle(" ")
        
        QApplication.setOverrideCursor(QtGui.QCursor(Qt.CrossCursor))
        
    def paintEvent(self, event):
        brush_color = (0, 0, 0, 255)
        lw = 2

        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('red'), lw))
        qp.setBrush(QtGui.QColor(*brush_color))
        rect = QRectF(self.begin, self.end)
        qp.drawRect(rect)
    
    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        x1 = int(min(self.begin.x(), self.end.x())*1920/1535)
        y1 = int(min(self.begin.y(), self.end.y())*1080/863)
        x2 = int(max(self.begin.x(), self.end.x())*1920/1535)
        y2 = int(max(self.begin.y(), self.end.y())*1080/863)
        print(x1)
        print(y1)
        print(x2)
        print(y2)
        self.setWindowOpacity(0)
        QApplication.restoreOverrideCursor()
        self.parent.screanshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.parent.show()
        self.close()