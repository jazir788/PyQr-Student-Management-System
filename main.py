from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication,QMainWindow, QTableWidget,QTableWidgetItem,\
 QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QMessageBox, QToolBar, QStatusBar, QLabel, QGridLayout
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Student",self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        search_action  = QAction(QIcon("icons/search.png"),"Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name","Course","Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        self.setFixedWidth(450)
        self.setFixedHeight(450)

        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.table.cellClicked.connect(self.cell_clicked)





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

    def search(self):
        dialog = SearchDialog()
        dialog.exec()


    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)


        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)


    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(500)
        self.setFixedHeight(500)

        layout = QVBoxLayout()

        index = student_management_system.table.currentRow()
        student_name = student_management_system.table.item(index, 1).text()

        self.student_id = student_management_system.table(index, 0).text()


        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        course_name = student_management_system.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Maths", "Computer Science", "Geography"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        student_phone_number = student_management_system.table.item(index, 3).text()

        self.mobile = QLineEdit(student_phone_number)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        button = QPushButton("Register")
        layout.addWidget(button)
        button.clicked.connect(self.update_student)

        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(), self.course_name.text(),
                        self.mobile.text(), self.student_id ))
        connection.commit()
        cursor.close()
        connection.close()

        student_management_system.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)




class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(500)
        self.setFixedHeight(500)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        courses = ["Biology", "Maths", "Computer Science", "Geography"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        button = QPushButton("Register")
        layout.addWidget(button)
        button.clicked.connect(self.add_student)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection =  sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))

        connection.commit()
        cursor.close()
        connection.close()
        student_management_system.load_data()
        self.accept()


    def closing(self):
        self.accept()

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(500)
        self.setFixedHeight(500)

        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        button = QPushButton("Search")
        button.clicked.connect(self.search)
        button.clicked.connect(self.search_records)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students "
                                "WHERE name = ?", (name,))
        rows = list(result)
        print(rows)
        items = student_management_system.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(items)
            student_management_system.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()

    def search_records(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        try:
            with connection:
                cursor = connection.cursor()
                query = cursor.execute("SELECT * FROM students WHERE UPPER(name) LIKE UPPER(?)", ('%' + name + '%',))
                rows = list(query)
                print(rows)
                student_management_system.table.clearSelection()
                for row_data in rows:
                    student_id, student_name, course, mobile_number = row_data
                    items = student_management_system.table.findItems(student_name, Qt.MatchFlag.MatchContains)

                    for row in range(student_management_system.table.rowCount()):
                        item = student_management_system.table.item(row, 1)
                        if item and student_name in item.text():

                            for column in range(student_management_system.table.columnCount()):
                                student_management_system.table.item(row, column).setSelected(True)

                # Handle no matching records found with pop-up dialog.
                if not rows:
                    msg = QMessageBox()
                    msg.setWindowTitle("No Records")
                    msg.setText("No matching records found")
                    msg.setIcon(QMessageBox.Icon.Warning)
                    msg.exec()
        finally:
            connection.close()
        self.close()


app = QApplication(sys.argv)
student_management_system = MainWindow()
student_management_system.load_data()
student_management_system.show()
sys.exit(app.exec())

