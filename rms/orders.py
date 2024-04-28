from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget, QApplication, QLabel, QLineEdit, QVBoxLayout,
                             QHBoxLayout, QWidget, QFrame, QPushButton, QTableWidget, QTableWidgetItem,
                             QCheckBox, QComboBox, QGridLayout, QScrollArea, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import (QRect, Qt)
from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import (QIntValidator)

from appname import AppName
# from sidebar import Sidebar
from footer import Footer
import sidebar

import functools

from classes2.db import DB

import dashboard


class Orders(QMainWindow):

    def __init__(self, parent):
        super().__init__(parent)

        self.db = DB()

        self.initUI()

    def initUI(self):

        in_class = "orders"

        self.sidebar = sidebar.Sidebar(self)
        self.sidebar.window.connect(self.getvalue)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.sidebar)

        header = AppName(in_class)
        footer = Footer()

        self.scrollArea = QScrollArea()
        # self.scrollArea.setContentsMargins(0, 0, 0, 0)
        self.scrollArea.setStyleSheet("Border: none")

        left_content = QVBoxLayout(self.scrollArea)
        left_content.setContentsMargins(0, 0, 0, 0)
        left_content.setSpacing(0)

        table = QLabel("Table No")

        table_list = self.get_tables()

        self.table_no = QComboBox()
        self.table_no.setFixedWidth(250)
        self.table_no.addItems(table_list)

        hl = QHBoxLayout()
        hl.addStretch()
        hl.addWidget(table)
        hl.addStretch()
        hl.addWidget(self.table_no)
        hl.addStretch()

        # left_content.addLayout(hlayout1)
        left_content.addLayout(hl)

        menu_list = self.get_menu_items()

        for key, value in menu_list.items():
            if value:
                category = QLabel(key)
                category.setAlignment(Qt.AlignCenter)

                left_content.addWidget(category)

                for x in value:
                    quantity = QLineEdit()
                    quantity.setFixedWidth(50)
                    quantity.setFixedHeight(50)

                    xtimes = QLabel(" X ")

                    widget2 = MenuItems(x)
                    widget2.setMouseTracking(True)
                    widget2.mouseMoveEvent = functools.partial(self.mouse_moved, source_object=widget2)
                    widget2.leaveEvent = functools.partial(self.mouse_left, source_object=widget2)
                    widget2.mousePressEvent = functools.partial(self.mouse_pressed,
                                                                source_object=[quantity, widget2])
                    widget2.setStyleSheet("background-color: grey; color: black")

                    hlayout2 = QHBoxLayout()
                    hlayout2.setContentsMargins(10, 10, 0, 0)
                    hlayout2.addWidget(quantity)
                    hlayout2.addWidget(xtimes)
                    hlayout2.addWidget(widget2)

                    # widget2.mousePressEvent = functools.partial(self.mouse_pressed, source_object=hlayout2)

                    left_content.addLayout(hlayout2)
                    left_content.addStretch()

        # left_content.addLayout(hlayout2)



        # self.thumbnail = QHBoxLayout()
        # self.scrollArea.setMaximumWidth(self.width()/2)

        self.scrollChildArea = QWidget()
        self.scrollChildArea.setLayout(left_content)

        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.scrollArea.setMinimumHeight(160)
        # self.scrollArea.setMaximumHeight(160)
        self.scrollArea.setWidget(self.scrollChildArea)
        # self.scrollArea.setFrameShape(QFrame().NoFrame)
        self.scrollArea.setStatusTip("Preview")

        # ---------------------------------------------------
        self.scrollArea2 = QScrollArea()
        # self.scrollArea2.setContentsMargins(0, 0, 0, 0)
        self.scrollArea2.setStyleSheet("Border: none")
        # ---------------------------------------------------

        self.right_content = QVBoxLayout(self.scrollArea2)
        self.right_content.setContentsMargins(0, 0, 0, 0)
        # self.right_content.setAlignment(Qt.AlignCenter)

        # ---------------------------------------------------
        self.scrollChildArea2 = QWidget()
        self.scrollChildArea2.setLayout(self.right_content)

        self.scrollArea2.setWidgetResizable(True)
        self.scrollArea2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.scrollArea2.setMinimumHeight(160)
        # self.scrollArea2.setMaximumHeight(160)
        self.scrollArea2.setWidget(self.scrollChildArea2)
        # self.scrollArea2.setFrameShape(QFrame().NoFrame)
        self.scrollArea2.setStatusTip("Preview")
        bar = self.scrollArea2.verticalScrollBar()
        bar.rangeChanged.connect(lambda: bar.setValue(bar.maximum()))
        # ---------------------------------------------------

        bill = QLabel()
        bill.setText("Bill")
        bill.setAlignment(Qt.AlignCenter)
        bill.setFixedWidth(450)
        bill.setStyleSheet("font: 75 20pt \"MS Shell Dlg 2\";")

        self.msg = QLabel("")
        self.msg.setFixedHeight(50)

        print_bill = QPushButton("Send")
        print_bill.setFixedWidth(100)
        print_bill.setFixedHeight(50)
        print_bill.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";\n"
                                 "background-color: rgb(30, 45, 66);\n"
                                 "color: rgb(255, 255, 255);")
        print_bill.clicked.connect(self.send_bill)

        hl2 = QHBoxLayout()
        hl2.addWidget(self.msg, alignment=Qt.AlignCenter)
        hl2.addWidget(print_bill, alignment=Qt.AlignRight)
        self.subtotal = 0.00
        self.tax = 0.00
        self.total = 0.00
        self.HST_RATE = 0.15
        self.food_order = []

        self.subtotal_amount = QLabel("Subtotal : " + str(self.subtotal))
        self.subtotal_amount.setAlignment(Qt.AlignRight)

        self.tax_amount = QLabel("Tax : " + str(self.tax))
        self.tax_amount.setAlignment(Qt.AlignRight)

        self.total_amount = QLabel("Total : " + str(self.total))
        self.total_amount.setAlignment(Qt.AlignRight)

         # Payment Method Selection
        self.payment_option = QComboBox()
        self.payment_option.addItem("Debit/Credit Card")
        self.payment_option.addItem("Cash")

        self.payment_option.setFixedWidth(250)
        self.payment_option.currentIndexChanged.connect(self.payment_method_changed)

        payment_label = QLabel("Payment Method:")
        payment_label.setBuddy(self.payment_option)

        # Cash Received Input
        self.cash_received_input = QLineEdit()
        self.cash_received_input.setFixedWidth(100)
        self.cash_received_input.setValidator(QIntValidator(0, 100000))
        self.cash_received_input.textChanged.connect(self.calculate_change)
        self.cash_received_input.hide()

        cash_received_label = QLabel("Cash Received:")
        cash_received_label.setBuddy(self.cash_received_input)

        # Change Display
        self.change_display = QLabel("Change: $0.00")
        self.change_display.hide()

        # Layout for payment options and cash input
        payment_layout = QHBoxLayout()
        payment_layout.addWidget(payment_label)
        payment_layout.addWidget(self.payment_option)
        payment_layout.addWidget(cash_received_label)
        payment_layout.addWidget(self.cash_received_input)
        payment_layout.addWidget(self.change_display)

        self.right_content.addWidget(bill)
 
        self.right_content.addWidget(self.subtotal_amount)
        self.right_content.addWidget(self.tax_amount)
        self.right_content.addWidget(self.total_amount)
        
       # Integrate the payment layout into the existing right_content layout
   
        self.right_content.addLayout(payment_layout)  # Adjust index as needed

        self.right_content.addLayout(hl2)
     
        self.right_content.addStretch()

        content = QGridLayout()
        content.setContentsMargins(0, 0, 0, 0)
        content.setSpacing(0)

        content.addWidget(self.scrollArea, 0, 0)
        content.addWidget(self.scrollArea2, 0, 1)


        layout = QVBoxLayout()

        layout.addWidget(header)
        layout.addLayout(content)
        layout.addStretch()
        layout.addWidget(footer)

        layout.setContentsMargins(0, 0, 0, 0)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)
        self.setContentsMargins(0, 0, 0, 0)



        self.setWindowTitle("Settings")
        
        self.showMaximized()
        self.show()
        self.center()

    def center(self):
        '''centers the window on the screen'''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        # self.move(int((screen.width() - size.width()) / 2),
        #           int((screen.height() - size.height()) / 2))

    def getvalue(self, value):
        print(value)
        print(type(value))

        if value == 1:
            self.hide()
            view = sidebar.Dashboard(self)
        elif value == 2:
            self.hide()
            view = sidebar.Employee(self)
        elif value == 3:
            self.hide()
            view = sidebar.Table(self)
        elif value == 4:
            self.hide()
            view = sidebar.Reservations(self)
        elif value == 5:
            self.hide()
            view = sidebar.Category(self)
        elif value == 6:
            self.hide()
            view = sidebar.Settings(self)
        elif value == 7:
            pass
        elif value == 8:
            self.hide()
            view = sidebar.Menu(self)
        elif value == 9:
            self.hide()
            view = sidebar.Bill(self)

    def settle_bill(self):
        if not self.food_order:
            self.msg.setText("Food not ordered")
            self.msg.setStyleSheet("color: red")
        else:
            '''
                Update the database with the order details.
            '''
            query = "select id from tables where table_number=%s"
            values = (self.table_no.currentText(),)

            data = self.db.fetch(query, values)

            for (id) in data:
                table_id = id[0]

            query = "update orders set paid = 'yes' where id = %s"
            values = (table_id,)

            data = self.db.execute(query, values)

            self.msg.setText("Bill Settled")
            self.msg.setStyleSheet("color: green")

    def send_bill(self):
        print(self.food_order)

        if not self.food_order:
            print("Food not ordered")
            self.msg.setText("Food not ordered")
            self.msg.setStyleSheet("color: red")
            return  # Exit the function if no food is ordered

        # Query to fetch the table ID
        # query = "SELECT id FROM tables WHERE table_number = %s"
        # values = (self.table_no.currentText(),)

        # data = self.db.fetch(query, values)

        # if not data:
        #     print("No table found with number:", self.table_no.currentText())
        #     self.msg.setText("Table number not found")
        #     self.msg.setStyleSheet("color: red")
        #     return  # Exit the function if table ID not found

        # At this point, data is guaranteed to have at least one row
        # table_id = data[0][0]  # Assume first row and first column is table_id

        # Insert the order into the database
        query = "INSERT INTO orders (food_list, subtotal, tax, total_price) VALUES (%s, %s, %s, %s)"
        values = (', '.join(self.food_order), str(self.subtotal), str(self.tax), str(self.total))
        self.db.execute(query, values)

        print("Order saved")
        self.msg.setText("Saved")
        self.msg.setStyleSheet("color: green")



    def get_tables(self):
        query = "select table_number, covers from tables " \
                "WHERE id NOT IN (SELECT table_id FROM orders WHERE paid = 'no');"
        values = ()

        data = self.db.fetch(query, values)

        tables = []

        # for (table_number, covers) in data:
        #     tables.append("Table: " + str(table_number) + " Cover: (" + str(covers) + ")")

        for (table_number, covers) in data:
            tables.append(table_number)

        return tables

    def get_menu_items(self):
        query = "select category_name from category"
        values = ()

        data = self.db.fetch(query, values)

        menu = {}

        for (category_name) in data:
            menu[category_name[0]] = []

        print(menu)

        query = "select food_name, price, category_name from menu " \
                "join category on category.id = menu.category_id"
        values = ()

        data = self.db.fetch(query, values)

        for (food_name, price, category_name) in data:
            menu[category_name].append([food_name, price])

        print("\nHere is the list\n")
        for key, value in menu.items():
            print(str(key) + ": " + str(value))

        return menu


    def mouse_moved(self, event, source_object=None):
        # print("Moved")
        source_object.setStyleSheet("background-color: black; color: white")

    def mouse_left(self, event, source_object=None):
        # print("Left")
        source_object.setStyleSheet("background-color: grey; color: black")

    def mouse_pressed(self, event, source_object=None):
        print("Pressed")
        # print(source_object)
        # print(type(source_object))
        # # print(source_object.widget())
        # print(source_object[0].text())
        # print(source_object[1].food_label.text())
        # print(source_object[1].food_price_label.text())

        quantity = QLabel(source_object[0].text())
        if quantity.text() == "":
            quantity.setText("1")
        xtimes = QLabel(" X ")
        food_label = QLabel(source_object[1].food_label.text())
        food_price_label = QLabel(source_object[1].food_price_label.text())
        delete = QLabel("X")
        delete.setStyleSheet("color: red")

        # widget2 = MenuItems(x)
        # widget2.setMouseTracking(True)
        # widget2.mouseMoveEvent = functools.partial(self.mouse_moved, source_object=widget2)
        # widget2.leaveEvent = functools.partial(self.mouse_left, source_object=widget2)
        # widget2.mousePressEvent = functools.partial(self.mouse_pressed,
        #                                             source_object=[quantity, widget2])
        # widget2.setStyleSheet("background-color: grey; color: black")

        hlayout2 = QHBoxLayout()
        hlayout2.setContentsMargins(10, 10, 0, 0)
        hlayout2.addStretch()
        hlayout2.addWidget(quantity)
        hlayout2.addStretch()
        hlayout2.addWidget(xtimes)
        hlayout2.addStretch()
        hlayout2.addWidget(food_label)
        hlayout2.addStretch()
        hlayout2.addWidget(food_price_label)
        hlayout2.addStretch()
        hlayout2.addWidget(delete)
        hlayout2.addStretch()

        widget = QWidget()
        widget.setObjectName(str(int(quantity.text()) * round(float(food_price_label.text()), 2)))
        widget.setLayout(hlayout2)

        delete.mousePressEvent = functools.partial(self.delete_bill_item, source_object=widget)

        # widget2.mousePressEvent = functools.partial(self.mouse_pressed, source_object=hlayout2)

        # self.right_content.addWidget(widget)
        self.right_content.insertWidget(self.right_content.count() - 3, widget)
        # self.right_content.addStretch()
        self.subtotal += float(quantity.text()) * round(float(food_price_label.text()), 2)
        self.tax = self.HST_RATE * self.subtotal
        self.total =  self.subtotal + self.tax
        self.updateTotals()

        self.food_order.append(quantity.text() + " X " + food_label.text() + " = " + food_price_label.text())
        print("\nAdded")
        print(self.food_order)

        # print(widget.findChildren(QLabel)[0].text())
        # print(widget.findChildren(QLabel)[2].text())




    def delete_bill_item(self, event, source_object=None):
        print("Delete here")
        print(source_object.objectName())

        self.subtotal -= float(source_object.objectName())
        self.food_order.remove(source_object.findChildren(QLabel)[0].text()
                               + " X " + source_object.findChildren(QLabel)[2].text()
                               + " = " + source_object.findChildren(QLabel)[3].text())
        print("\nDeleted")
        print(self.food_order)
        self.tax = self.HST_RATE * self.subtotal
        self.total =  self.subtotal + self.tax
        self.updateTotals()
        source_object.setParent(None)
    
    def updateTotals(self):
        self.subtotal_amount.setText("Subtotal: " + str(round(self.subtotal, 2)))
        self.tax_amount.setText("Tax: " + str(round(self.tax, 2)))
        self.total_amount.setText("Total: " + str(round(self.total, 2)))

    def payment_method_changed(self):
        if self.payment_option.currentText() == "Cash":
            self.cash_received_input.show()
            self.change_display.show()
        else:
            self.cash_received_input.hide()
            self.change_display.hide()

    def calculate_change(self):
        if self.payment_option.currentText() == "Cash":
            try:
                cash_received = float(self.cash_received_input.text())
                change = cash_received - self.total
                self.change_display.setText(f"Change: ${change:.2f}")
            except ValueError:
                self.change_display.setText("Change: $0.00")



class MenuItems(QFrame):

    def __init__(self, parent):
        super().__init__()

        self.initUI(parent)

    def initUI(self, parent):
        print("Parent: ")
        print(type(parent))
        print(parent)

        frame = QFrame()
        # frame.setStyleSheet("background-color: rgb(30, 45, 66);")
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)
        frame.setFixedWidth(250)
        frame.setFixedHeight(50)

        self.food_label = QLabel()
        self.food_label.setText(parent[0])

        self.food_price_label = QLabel()
        self.food_price_label.setText(str(parent[1]))

        test_layout = QHBoxLayout(frame)
        test_layout.addWidget(self.food_label)
        test_layout.addStretch()
        test_layout.addWidget(self.food_price_label)

        layout = QVBoxLayout()
        layout.addWidget(frame)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setLayout(layout)
        # self.resize(250, 50)
        # self.setContentsMargins(0, 0, 0, 0)
        # self.setGeometry(QRect(0, 0, 450, 50))