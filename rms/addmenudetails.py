from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget, QApplication, QLabel, QLineEdit, QVBoxLayout,
                             QHBoxLayout, QWidget, QFrame, QPushButton, QDateEdit, QComboBox)
from PyQt5.QtCore import (QRect, Qt, QDate, pyqtSignal)
from PyQt5.QtGui import (QIntValidator, QDoubleValidator)

from classes2.db import DB

import datetime


class AddMenuDetails(QMainWindow):

    closing = pyqtSignal(int)

    def __init__(self, parent, update, id=None):
        super().__init__(parent)

        self.db = DB()

        self.initUI(update, id)

    def initUI(self, update, id):

        self.setWindowModality(Qt.ApplicationModal)

        frame = QFrame()
        # frame.setStyleSheet("background-color: rgb(30, 45, 66);")
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)
        # frame.setMinimumWidth(430)
        # frame.setFixedHeight(395)
        frame.setStyleSheet("border: none")

        add_employee_button = QLabel(frame)
        add_employee_button.setAlignment(Qt.AlignCenter)
        add_employee_button.setGeometry(QRect(110, 30, 210, 41))
        add_employee_button.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";\n"
                                 "background-color: rgb(30, 45, 66);\n"
                                 "color: rgb(255, 255, 255);")
        add_employee_button.setText("Add Menu Details")

        foodname = QLabel(frame)
        foodname.setText("Food Name")
        foodname.setGeometry(QRect(50, 100, 75, 13))

        self.nametextbox = QLineEdit(frame)
        self.nametextbox.setGeometry(QRect(160, 90, 181, 31))
        self.nametextbox.setFixedWidth(180)

        foodcategory = QLabel(frame)
        foodcategory.setText("Category")
        foodcategory.setGeometry(QRect(50, 140, 61, 16))

        categories = self.get_all_category()

        self.category_list = QComboBox(frame)
        self.category_list.setGeometry(QRect(160, 130, 181, 31))
        self.category_list.setFixedWidth(180)
        self.category_list.addItems(categories)

        pricelabel = QLabel(frame)
        pricelabel.setText("Price")
        pricelabel.setGeometry(QRect(50, 180, 47, 13))

        self.pricetextbox = QLineEdit(frame)
        self.pricetextbox.setGeometry(QRect(160, 170, 181, 31))
        self.pricetextbox.setFixedWidth(180)
        self.pricetextbox.setValidator(QDoubleValidator())

        joindatelabel = QLabel(frame)
        joindatelabel.setText("Start Date")
        joindatelabel.setGeometry(QRect(80, 260, 71, 16))

        self.addbutton = QPushButton(frame)
        self.addbutton.setText("Add Item")
        self.addbutton.setGeometry(QRect(160, 300, 111, 31))
        self.addbutton.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";\n"
                                   "background-color: rgb(30, 45, 66);\n"
                                   "color: rgb(255, 255, 255);")
        # self.addbutton.clicked.connect(lambda: self.add_button_click("tables"))

        if update == 'add':
            print("Add")
            print(id)
            self.addbutton.setText("Add Table")
            self.addbutton.clicked.connect(lambda: self.add_button_click("menu"))
        else:
            print("Update")
            print(id)
            self.addbutton.setText("Update Table")
            self.addbutton.clicked.connect(lambda: self.update_button_click("menu", id))

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(frame)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)

        # self.setLayout(layout)

        self.setWindowTitle("Add Employee Details")
        self.resize(430, 395)
        self.show()

        self.center()

    def center(self):
        '''centers the window on the screen'''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        

    def update_button_click(self, where, id):
        if where == "menu":
            print("Tables Finally here")

            food_name = self.nametextbox.text()
            price = self.pricetextbox.text()

            query = "select id from category where category_name=%s limit 1"
            values = (self.category_list.currentText(),)

            result = self.db.fetch(query, values)

            for (id) in result:
                category_id = id[0]

            print(category_id)
            print(type(category_id))

            query = "update menu set `food_name`=%s, `price`=%s, category_id=%s " \
                    "where food_name=%s;"
            values = (food_name, price, category_id, food_name)

            result = self.db.execute(query, values)

            self.closeEvent = self.message()

    def add_button_click(self, where):
        print("Button Clicked")
        print(self.nametextbox.text())
        print(self.category_list.currentText())
        print(self.pricetextbox.text())

        food_name = self.nametextbox.text()
        price = self.pricetextbox.text()

        query = "select id from category where category_name=%s limit 1"
        values = (self.category_list.currentText(),)

        result = self.db.fetch(query, values)

        for (id) in result:
            category_id = id[0]

        '''
            All set up..
            Now query to add the item in the database.
            Also format the decimal place.
        '''
        query = "insert into menu (food_name, price, category_id)" \
                "values (%s, %s, %s);"
        values = (food_name, price, category_id)

        try:
            result = self.db.execute(query, values)
        except:
            pass

        self.closeEvent = self.message()

    def message(self):
        self.closing.emit(1)
        self.close()

    def get_all_category(self):
        query = "select category_name from category"
        values = ()

        data = self.db.fetch(query, values)

        list = []

        for (category_name) in data:
            print(category_name)
            list.append(category_name[0])
        return list