from PySide6.QtWidgets import QWidget, QPushButton, QTextEdit
from PIL import ImageGrab
import time

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.select_btn = QPushButton()
        self.read_btn = QPushButton()
        self.text_box = QTextEdit()
        self.screanshot = None
        
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
        self.screanshot = ImageGrab.grab(bbox=(81,135,500,300))
        self.show()
        print("aaa")
        
    def read(self):
        self.screanshot.show()
        print("bbb")
