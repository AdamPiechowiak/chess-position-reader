from PySide6.QtWidgets import QWidget, QPushButton, QTextEdit, QApplication, QLabel
from PySide6.QtCore import QPoint, Qt, QRectF, QThread, Signal
from PySide6 import QtGui
from PIL import ImageGrab
import time
import tkinter as tk
from tkinter import filedialog
from PIL.ImageQt import ImageQt
from tools.split_images import splitImage
import tensorflow as tf
import numpy as np
from PIL import Image



class ThreadReadImage(QThread):
    
    signal = Signal(str)
    
    def __init__(self,parent,image,piece_model,color_model):
         self.image = image
         self.piece_model = piece_model
         self.color_model = color_model
         
         super(ThreadReadImage,self).__init__(parent)
        
    def run(self):
        
        pieces_list = [[0] * 8 for i in range(8)]
        
        # split Image
        image_list = splitImage(self.image, 8, 8)
        
        
        
        piece_names = ['bishop', 'king', 'knight', 'none', 'pawn', 'queen', 'rook']
        color_names = ['black', 'white']
        
        # what is in image
        for i in range(8):
            for j in range(8):
                
                im = np.array(image_list[i][j].resize((80,80)))
                img = im.reshape((1,80,80,3))
                
                pred_piece = self.piece_model.predict(img)
                score_p = tf.nn.softmax(pred_piece[0])
                piece = piece_names[np.argmax(score_p)]
                if(piece=='none'):
                    pieces_list[i][j]=0
                else:
                    
                    pred_color = self.color_model.predict(img)
                    score_c = tf.nn.softmax(pred_color[0])
                    color = color_names[np.argmax(score_c)]
                    
                    if(piece=='king'):
                        if(color=='black'):
                            pieces_list[i][j]='k'
                        else:
                            pieces_list[i][j]='K'
                    elif(piece=='queen'):
                        if(color=='black'):
                            pieces_list[i][j]='q'
                        else:
                            pieces_list[i][j]='Q'
                    elif(piece=='bishop'):
                        if(color=='black'):
                            pieces_list[i][j]='b'
                        else:
                            pieces_list[i][j]='B'
                    elif(piece=='rook'):
                        if(color=='black'):
                            pieces_list[i][j]='r'
                        else:
                            pieces_list[i][j]='R'
                    elif(piece=='pawn'):
                        if(color=='black'):
                            pieces_list[i][j]='p'
                        else:
                            pieces_list[i][j]='P'
                    elif(piece=='knight'):
                        if(color=='black'):
                            pieces_list[i][j]='n'
                        else:
                            pieces_list[i][j]='N'
        
        
        fen = self.encodeToFEN(pieces_list)
        
        self.signal.emit(fen)
        
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

class MainWindow(QWidget):
    
    screanshot_is_set = Signal()
    
    def __init__(self):
        super().__init__()
        
        self.piece_model = tf.keras.models.load_model('tools/piece_model')
        self.color_model = tf.keras.models.load_model('tools/color_model')
        self.new_btn = QPushButton()
        self.save_btn = QPushButton()
        self.text_box = QTextEdit()
        self.screanshot = None
        self.snipping_window = None
        
        
        self.setup()
        
    def setup(self):
        
        self.new_btn = QPushButton("New", self)
        self.new_btn.move(10,10)
        
        self.open_btn = QPushButton("Open", self)
        self.open_btn.move(90,10)
        
        self.save_btn = QPushButton("Save", self)
        self.save_btn.move(170,10)
        self.save_btn.hide()
        
        
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
        self.screanshot_is_set.connect(self.readImage)
        
        self.setFixedSize(300,40)
        self.setWindowTitle("Chess position reader")
        self.move(100,100)
        
        self.show()
        
    def newClicked(self):
        self.hide()
        time.sleep(0.2)
        self.snipping_window = SnippingWindow(self)
        self.save_btn.show()
        
        
    def saveClicked(self):
        #self.screanshot.show()
        self.text_box.setText("save")
        self.readImage()
        
    def openClicked(self):
        
        filepath = tk.filedialog.askopenfilename(
            title='Select a file...',
            filetypes=[('Image files', '*.png')]
            )   
        
        self.screanshot = Image.open(filepath).convert('RGB')
        
        qim = ImageQt(self.screanshot.resize((280, 280)))
        pix = QtGui.QPixmap.fromImage(qim)
        
        self.image.setPixmap(pix)
        self.setFixedSize(300,490)
        self.save_btn.show()
        self.screanshot_is_set.emit()

    def readImage(self):
        
        
        self.text_box.setText("in progres")
        self.t = ThreadReadImage(self,self.screanshot,self.piece_model,self.color_model)
        self.t.signal.connect(self.setTextBox)
        self.t.start()
        
    
    def setTextBox(self,text):
        
        self.text_box.setText(text)
        
    

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
        
        self.hide()
        self.parent.show()

        self.parent.screanshot_is_set.emit()
        
        self.close()