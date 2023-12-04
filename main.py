from PyQt6.QtWidgets import QApplication,QMainWindow, QTableWidget,QTableWidgetItem,\
 QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton

from PyQt6.QtGui import QAction
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student",self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name","Course","Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)



    def load_data(self):
        connection = sqlite3.connect("database.db")
        results  = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(results):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        student_name = QLineEdit()
        student_name.setPlaceholderText("Name")
        layout.addWidget(student_name)

        course_name = QComboBox()
        courses = ["Biology","Maths","Computer Science","Geography"]
        course_name.addItems(courses)
        layout.addWidget(course_name)

        mobile = QLineEdit()
        mobile.setPlaceholderText("Mobile")
        layout.addWidget(mobile)

        button = QPushButton("Register")


        self.setLayout(layout)






app = QApplication(sys.argv)
student_management_system = MainWindow()
student_management_system.load_data()
student_management_system.show()
sys.exit(app.exec())

