from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont
from PySide6.QtWidgets import QMainWindow, QTableView, QPushButton, QVBoxLayout, QWidget, QApplication


class TableWindow(QMainWindow):
    def __init__(self, df):
        super(TableWindow, self).__init__()
        self.setWindowTitle("Table View")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        layout.setContentsMargins(50, 50, 50, 50)

        self.tableView = QTableView(self)
        layout.addWidget(self.tableView)

        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close_window)
        layout.addWidget(self.close_button)
        self.close_button.setMaximumWidth(200)

        self.populate_table(df)
        self.set_font_and_size()

        # Make QMainWindow full-screen
        self.showFullScreen()

    def populate_table(self, df):
        if df is not None:
            model = QStandardItemModel(df.shape[0], df.shape[1])
            model.setHorizontalHeaderLabels(df.columns.tolist())
            for row in range(df.shape[0]):
                for col in range(df.shape[1]):
                    item = QStandardItem(str(df.iat[row, col]))
                    model.setItem(row, col, item)
            self.tableView.setModel(model)
            self.tableView.resizeColumnsToContents()

    def set_font_and_size(self):
        font = QFont("Arial", 16)
        self.tableView.setFont(font)
        self.tableView.verticalHeader().setDefaultSectionSize(100)
        self.tableView.horizontalHeader().setDefaultSectionSize(225)

    def close_window(self):
        self.close()
