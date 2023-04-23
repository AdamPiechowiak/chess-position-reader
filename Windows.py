from PySide6.QtWidgets import QWidget, QPushButton, QTextEdit, QApplication, QLabel
from PySide6.QtCore import QPoint, Qt, QRectF
from PySide6 import QtGui
from PIL import ImageGrab
import time
import tkinter as tk
from PIL.ImageQt import ImageQt

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
        
        self.image = QLabel(self)
        self.image.setFixedWidth(280)
        self.image.setFixedHeight(280)
        self.image.move(10,40)
        
        self.text_box = QTextEdit(self)
        self.text_box.setMaximumHeight(150)
        self.text_box.setMinimumWidth(280)
        self.text_box.move(10,330)
        
        self.select_btn.clicked.connect(self.select)
        self.read_btn.clicked.connect(self.read)
        
        self.setFixedSize(300,40)
        self.setWindowTitle("Window")
        self.move(100,100)
        
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
        #root = tk.Tk()
        #screen_width = root.winfo_screenwidth()
        #screen_height = root.winfo_screenheight()
        #self.setGeometry(0, 0, screen_width, screen_height)
        self.setFixedWidth(1535)
        self.setFixedHeight(863)
        #self.move(0,0)
        self.move(-7,-30)
        self.setWindowOpacity(0.3)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
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
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x1 = int(min(self.begin.x(), self.end.x())*screen_width/self.width())
        y1 = int(min(self.begin.y(), self.end.y())*screen_height/self.height())
        x2 = int(max(self.begin.x(), self.end.x())*screen_width/self.width())
        y2 = int(max(self.begin.y(), self.end.y())*screen_height/self.height())
        self.setWindowOpacity(0)
        QApplication.restoreOverrideCursor()
        self.parent.screanshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        print(self.parent.screanshot.shape)
        print(self.parent.screanshot.resize((280, 280)).shape)
        qim = ImageQt(self.parent.screanshot.resize((280, 280)))
        pix = QtGui.QPixmap.fromImage(qim)
        self.parent.image.setPixmap(pix)
        
        self.parent.setFixedSize(300,490)
        self.parent.move(100,100)
        self.parent.show()
        self.close()