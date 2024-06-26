from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget, QApplication, QLabel, QLineEdit, QVBoxLayout,
                             QHBoxLayout, QWidget, QFrame, QPushButton, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import (QRect, Qt)
from PyQt5.QtCore import Qt

from appname import AppName
# from sidebar import Sidebar
from footer import Footer
from addsearchframe import AddSearchFrame
import sidebar

from addtabledetails import AddTableDetails

from classes2.db import DB


import dashboard

class Table(QMainWindow):

    def __init__(self, parent):
        super().__init__(parent)

        self.db = DB()

        self.initUI()

    def initUI(self):

        in_class = "tables"

        self.sidebar = sidebar.Sidebar(self)
        self.sidebar.window.connect(self.getvalue)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.sidebar)

        header = AppName(in_class)
        footer = Footer()

        add_and_search = AddSearchFrame(in_class)
        add_and_search.add_button.clicked.connect(lambda: self.add_tables(in_class))
        add_and_search.search_button.clicked.connect(
                                        lambda: self.search_tables(add_and_search.search_box))

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        # self.table.setStyleSheet("border: none")
        # self.table.setStyleSheet(
        #     "background-color: rgb(255, 255, 255);\n"
        #     'font: 10pt "MS Shell Dlg 2";\n'
        #     "color: rgb(30, 45, 66);"
        # )

        # self.table.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("Table Name"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Covers"))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Edit"))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem("Delete"))



        # self.table.insertRow(self.table.rowCount())
        #
        # self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem("ID1"))
        # self.table.setItem(self.table.rowCount() - 1, 1, QTableWidgetItem("Name1"))
        # self.table.setItem(self.table.rowCount() - 1, 2, QTableWidgetItem("Job1"))
        # self.table.setItem(self.table.rowCount() - 1, 3, QTableWidgetItem("Joining Date1"))
        # self.table.setItem(self.table.rowCount() - 1, 4, QTableWidgetItem("Salary1"))
        # self.table.setItem(self.table.rowCount() - 1, 5, QTableWidgetItem("Bonus1"))
        # self.table.setItem(self.table.rowCount() - 1, 6, QTableWidgetItem("Total Salary1"))
        # self.table.setItem(self.table.rowCount() - 1, 7, QTableWidgetItem("Edit1"))
        # self.table.setItem(self.table.rowCount() - 1, 8, QTableWidgetItem("Delete1"))

        data = self.load_tables_data()
        print(data)

        for x in data:
            print(x)

        self.populate_table(data)

        layout = QVBoxLayout()

        layout.addWidget(header)
        layout.addWidget(add_and_search)
        layout.addWidget(self.table)
        # layout.addStretch()
        layout.addWidget(footer)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)
        self.setContentsMargins(0, 0, 0, 0)

        # self.resize(800, 600)
        self.setWindowTitle("Login")
        self.showMaximized()

        self.show()
        self.center()

    def center(self):
        '''centers the window on the screen'''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        

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
            pass
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
            self.hide()
            view = sidebar.Orders(self)
        elif value == 8:
            self.hide()
            view = sidebar.Menu(self)
        elif value == 9:
            self.hide()
            view = sidebar.Bill(self)

    def load_tables_data(self):
        query = "SELECT id, table_number, covers FROM tables;"

        result = self.db.fetch(query)

        return result

    '''
        This function is called after an employee has been added and returns only the last row.
    '''
    def add_update_tables_data(self):
        query = "SELECT id, table_number, covers FROM tables " \
                "order by id desc limit 1;"

        result = self.db.fetch(query)

        return result

    def edit_tables(self):
        emp_row = self.table.indexAt(self.sender().pos())
        id = int(self.table.cellWidget(emp_row.row(), emp_row.column()).objectName())
        print(emp_row.row())
        print(id)
        print(type(id))

        '''
            Get the data from the database for that user.
        '''
        data = self.get_data(id)

        print("Data")
        print(data)
        # print(type(data[4]))

        view = AddTableDetails(self, "update", data[0])

        view.tablenotextbox.setText(data[1])
        view.covertextbox.setText(str(data[2]))

        view.closing.connect(self.editupdate_emp)

    def editupdate_emp(self, check):
        print("I am here")
        print(check)

        self.table.clearContents()
        self.table.setRowCount(0)

        data = self.load_tables_data()

        self.populate_table(data)
        # self.table.resizeColumnsToContents()

    def get_data(self, id):
        query = "SELECT id, table_number, covers FROM tables " \
                "where id=%s"
        values = (id,)

        result = self.db.fetch(query, values)

        for (id, table_number, covers) in result:
            id = id
            table_number = table_number
            covers = covers

        return [id, table_number, covers]

    def delete_tables(self):
        emp_row = self.table.indexAt(self.sender().pos())

        # print(emp_row.row())
        # print(emp_row.column())

        # print(self.table.cellWidget(emp_row.row(), emp_row.column()).objectName())

        id = int(self.table.cellWidget(emp_row.row(), emp_row.column()).objectName())
        # print(id)
        # print(emp_row.child(emp_row.row(), emp_row.column()))

        query = "DELETE FROM tables WHERE id=%s"
        values = (id,)

        try:
            result = self.db.execute(query, values)
        except:
            pass

        self.table.clearContents()
        self.table.setRowCount(0)
        data = self.load_tables_data()

        self.populate_table(data)

    def add_tables(self, where):
        if where == "tables":
            print("Category Button Clicked from tables")

            view = AddTableDetails(self, "add")
            view.closing.connect(self.update_tables)

        elif where == "stocks":
            print("Stock Button Clicked")

    def search_tables(self, search_obj):
        search = search_obj.text()
        search_obj.setText("")

        print("Search")
        if search != "":
            query = "SELECT * FROM tables WHERE table_number like %s"
            values = ("%" + search + "%",)
        else:
            query = "SELECT * FROM tables"
            values = ()

        self.table.clearContents()
        self.table.setRowCount(0)

        data = self.db.fetch(query, values)

        self.populate_table(data)




    '''
        Repopulates the employee table with the updated data.
    '''
    def update_tables(self, check):
        print("I am here")
        print(check)

        data = self.add_update_tables_data()

        self.populate_table(data)

    '''
        This function populates the employee table with data.
    '''
    def populate_table(self, data):
        for (id, table_number, covers) in data:
            self.table.insertRow(self.table.rowCount())

            self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem(str(table_number)))
            self.table.setItem(self.table.rowCount() - 1, 1, QTableWidgetItem(str(covers)))

            edit = QPushButton(self.table)
            edit.setObjectName(str(id))
            edit.setStyleSheet("background-color: rgb(50,205,50);")
            edit.setText("Edit")
            edit.adjustSize()
            edit.clicked.connect(self.edit_tables)

            self.table.setCellWidget(self.table.rowCount() - 1, 2, edit)

            delete = QPushButton(self.table)
            delete.setObjectName(str(id))
            delete.setStyleSheet("background-color: #d63447;")
            delete.setText("Delete")
            delete.adjustSize()
            delete.clicked.connect(self.delete_tables)
            # delete.mousePressEvent = functools.partial(self.delete_emp, source_object=delete)
            self.table.setCellWidget(self.table.rowCount() - 1, 3, delete)