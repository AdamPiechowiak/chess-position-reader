from PySide6.QtWidgets import QWidget, QPushButton, QTextEdit, QApplication, QLabel
from PySide6.QtCore import QPoint, Qt, QRectF
from PySide6 import QtGui
from PIL import ImageGrab
import time
import tkinter as tk
from PIL.ImageQt import ImageQt
from tools.split_images import splitImage

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.new_btn = QPushButton()
        self.save_btn = QPushButton()
        self.text_box = QTextEdit()
        self.screanshot = None
        self.snipping_window = None
        
        self.setup()
        
    def setup(self):
        
        self.new_btn = QPushButton("New", self)
        self.new_btn.move(10,10)
        
        self.save_btn = QPushButton("Save", self)
        self.save_btn.move(90,10)
        
        self.open_btn = QPushButton("Open", self)
        self.open_btn.move(170,10)
        
        self.image = QLabel(self)
        self.image.setFixedWidth(280)
        self.image.setFixedHeight(280)
        self.image.move(10,40)
        
        self.text_box = QTextEdit(self)
        self.text_box.setMaximumHeight(150)
        self.text_box.setMinimumWidth(280)
        self.text_box.move(10,330)
        
        self.new_btn.clicked.connect(self.newClicked)
        self.save_btn.clicked.connect(self.saveClicked)
        self.open_btn.clicked.connect(self.openClicked)
        
        self.setFixedSize(300,40)
        self.setWindowTitle("Chess position reader")
        self.move(100,100)
        
        self.show()
        
    def newClicked(self):
        self.hide()
        time.sleep(0.2)
        self.snipping_window = SnippingWindow(self)
        
        
    def saveClicked(self):
        self.screanshot.show()
        self.text_box.setText("save")
        
    def openClicked(self):
        self.screanshot.show()
        self.text_box.setText("open")

    def readImage(self):
        
        
        pieces_list = [[0] * 8 for i in range(8)]
        
        # split Image
        image_list = splitImage(self.screanshot, 8, 8)
        #image_list[7][3].show()
        
        pieces_list[7][3]="Q"
        print(pieces_list)
        
        # what is in image
        
        #if(ispeice):
            # what color is piece
        
        
        #set text_box
        fen = self.encodeToFEN(pieces_list)
        self.text_box.setText(fen)
    
    def encodeToFEN(self, table):
        text = ""
        for row in table:    
            i=0
            for cell in row:
                if(cell==0):
                    i+=1
                else:
                    if(i!=0):
                        text +=str(i)
                        i=0
                    text +=str(cell)
            if(i!=0):
                text +=str(i)
            text+="/"
        text=text[:-1]+" w - - 0 1"
        return text

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
        
        qim = ImageQt(self.parent.screanshot.resize((280, 280)))
        pix = QtGui.QPixmap.fromImage(qim)
        self.parent.image.setPixmap(pix)
        self.parent.setFixedSize(300,490)
        
        self.parent.move(100,100)
        self.parent.readImage()
        self.parent.show()
        self.close()