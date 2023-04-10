from PySide6.QtWidgets import QApplication
from Window import MainWindow

if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()
    
    main_window = MainWindow()
    
    app.exec()