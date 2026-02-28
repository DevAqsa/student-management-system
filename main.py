from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton,
                             QMainWindow, QMessageBox)
import sys
from PyQt6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu = self.menuBar().addMenu("&File")
        help_about_menu = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)
        file_menu.addAction(add_student_action)

        about_action = QAction("About", self)
        file_menu.addAction(about_action)




app = QApplication(sys.argv)
age_calculator = MainWindow()
age_calculator.show()
sys.exit(app.exec())

