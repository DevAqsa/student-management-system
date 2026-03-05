from idlelib import statusbar

from PyQt6.QtStateMachine import QState
from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton,
                             QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox,
                             QToolBar, QStatusBar)
import sys
from PyQt6.QtGui import QAction, QIcon
import sqlite3

from PyQt6.sip import delete


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu = self.menuBar().addMenu("&File")
        help_about_menu = self.menuBar().addMenu("&Help")

        add_student_action = QAction(QIcon("icons/add.png"),"Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu.addAction(add_student_action)

        about_action = QAction("About", self)
        file_menu.addAction(about_action)

        search_action = QAction(QIcon("icons/search.png"),"Search", self)
        file_menu.addAction(search_action)
        search_action.triggered.connect(self.load_data)


        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # create the toolbar and the toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # create the status bar and status bar elements
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

    #     detect a click

        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Student")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Student")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusBar().removeWidget(child)


        self.statusBar.addWidget(edit_button)
        self.statusBar.addWidget(delete_button)


    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number , row_data in enumerate(result):
            self.table.insertRow(row_number)
            for colum_number , data in enumerate(row_data):
                self.table.setItem(row_number, colum_number, QTableWidgetItem(str(data)))
        connection.close()


    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()


    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()


class EditDialog(QDialog):
    pass


class DeleteDialog(QDialog):
    pass


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert student data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # add combo box of courses
        self.course_name = QComboBox()
        courses = ["Biology", "Maths", "Physics", "Computer science"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # add mobile number
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("number")
        layout.addWidget(self.mobile)


        # add a submit button
        button = QPushButton("Add Student")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)
    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students(name,course,mobile) Values (?,?,?)",
                       (name, course, mobile)
                       )
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())

