from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, \
    QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from dataframe_palletfind import PalletLocation
from log import LoginDialog
from tabview import TableWindow
from dataframe_invenloc import inv_loc
from dataframe_pallets import PalletFilled
from letter_select import LetterButton


class MyWidget(QMainWindow):
    def __init__(self):
        super(MyWidget, self).__init__()

        # Set the window properties
        self.setWindowTitle("Warehouse Application")
        self.setWindowState(Qt.WindowMaximized)  # Maximize the window
        self.table_windows = []

        # Create a central widget and set it to QMainWindow
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a vertical layout for the central widget
        self.vertical_layout = QVBoxLayout(self.central_widget)
        self.horizontal_layout = QHBoxLayout(self.central_widget)

        # Create a horizontal layout for buttons (A to I)
        self.button_layout = QHBoxLayout()

        # Generate buttons A to I using custom LetterButton instances
        letter_names = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        self.buttons = []


        for letter_name in letter_names:
            btn = LetterButton(letter_name)
            btn.setStyleSheet("background-color: green;")
            btn.setFixedHeight(btn.sizeHint().height() * 4)
            btn.setFixedWidth(btn.sizeHint().width() * 0.75)
            btn.letterSelected.connect(self.handle_letter_selected)  # Connect the custom signal
            font = QFont("Arial", 18)  # 18 is the font size
            btn.setFont(font)
            self.button_layout.addWidget(btn)
            self.buttons.append(btn)

        # Add the button layout to the vertical layout
        self.vertical_layout.addLayout(self.button_layout)

        # Create a dynamic grid layout for the buttons (A01, A02, etc.)
        self.dynamic_grid_layout = QGridLayout()
        self.vertical_layout.addLayout(self.dynamic_grid_layout)  # Add to the vertical layout

        self.value = self.get_value_from_dataframe()

    # Slot method to handle letter selection
    def handle_letter_selected(self, letter):
        # Clear the dynamic grid layout
        for i in reversed(range(self.dynamic_grid_layout.count())):
            widget = self.dynamic_grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create buttons with the selected letter
        for i in range(5, 0, -1):
            for j in range(27, 0, -1):
                button_name = f"{letter}0{j}{i}" if j < 10 else f"{letter}{j}{i}"
                btn = QPushButton(button_name)
                btn.clicked.connect(self.handle_button_click)
                # Set the background color based on the condition
                if button_name in self.value.tolist():
                    btn.setStyleSheet("background-color: red;")
                else:
                    btn.setStyleSheet("background-color: green;")
                btn.setFixedHeight(btn.sizeHint().height() * 4)
                btn.setFixedWidth(btn.sizeHint().width() * 0.75)
                font = QFont("Arial", 18)  # 18 is the font size
                btn.setFont(font)

                self.dynamic_grid_layout.addWidget(btn, i - 1, j - 1)
                self.buttons.append(btn)
                self.vertical_layout.addLayout(self.dynamic_grid_layout)
                self.horizontal_layout.addLayout(self.dynamic_grid_layout)

        # Update the layout
        # self.vertical_layout.addLayout(self.dynamic_grid_layout)
        # self.horizontal_layout.addLayout(self.dynamic_grid_layout)

    @staticmethod
    def get_value_from_dataframe():
        df = pal_instance.get_data()
        try:
            # Assuming 'code' is the column containing button names
            value = df['LocationID']
            return value
        except IndexError:
            return None  # Handle the case where the button name is not found in the DataFrame

    def handle_button_click(self):
        button_name = str(self.sender().text())
        df = pal_loc_instance.get_data(button_name)
        self.show_table_window(df)  # Using TableWindow to show data

    def show_table_window(self, df):
        if df is not None:
            table_window = TableWindow(df)
            table_window.show()

            # Store the table window instance to prevent it from being garbage collected
            self.table_windows.append(table_window)


if __name__ == '__main__':
    app = QApplication([])

    # Show the login dialog first
    login = LoginDialog()
    # noinspection PyUnresolvedReferences
    if login.exec() == QDialog.Accepted:
        username, password = login.get_credentials()

        # Construct the connection string
        connection_string = f'Driver={{SQL Server}};Server=192.168.60.5\\innova;Database=Innova;Uid={username};Pwd={password};TrustServerCertificate=yes;'
        inv_instance = inv_loc(connection_string)
        pal_instance = PalletFilled(connection_string)
        pal_loc_instance = PalletLocation(connection_string)

        # Now you can run the rest of your widget logic
        widget = MyWidget()
        widget.showMaximized()

        widget.show()
        app.exec()
