from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setup()
        
    def setup(self):
        select_btn = QPushButton("Select", self)
        select_btn.move(10,10)
        #select_btn.clicked.connect()
        
        read_btn = QPushButton("Read position", self)
        read_btn.setMinimumWidth(100)
        read_btn.move(100,10)
        
        text_box = QTextEdit(self)
        text_box.setMaximumHeight(150)
        text_box.move(10,40)
        
        #select_btn.setText("unselect")
        
        self.setFixedSize(300,200)
        self.setWindowTitle("Window")
        
        self.show()

if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()
    
    main_window = MainWindow()
    
    app.exec()