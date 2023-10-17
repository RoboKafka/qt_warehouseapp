import pyodbc

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, \
    QPushButton, QMessageBox
from PySide6.QtGui import QFont


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        self.setWindowTitle("Sql Login")

        self.layout = QVBoxLayout()

        # Create QLabel widgets
        self.username_label = QLabel("Username")
        self.password_label = QLabel("Password")

        # Create QLineEdit widgets
        self.username_field = QLineEdit(self)
        self.password_field = QLineEdit(self)
        self.password_field.setEchoMode(QLineEdit.Password)

        # Create QPushButton widget
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.check_credentials)

        # Customize font size for labels and button
        font = QFont()
        font.setPointSize(16)  # Change this value to your desired font size

        self.username_label.setFont(font)
        self.password_label.setFont(font)
        self.username_field.setFont(font)  # Set font for username input field
        self.password_field.setFont(font)
        self.login_button.setFont(font)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_field)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_field)
        self.layout.addWidget(self.login_button)

        # Set layout margins and spacing
        self.layout.setContentsMargins(40, 40, 40, 40)  # Adjust margins as needed
        self.layout.setSpacing(10)  # Adjust spacing as needed

        self.setLayout(self.layout)

    def check_credentials(self):
        username = self.username_field.text()
        password = self.password_field.text()

        # Basic check: fields are not empty
        if not username or not password:
            QMessageBox.warning(self, "Error", "Username or password cannot be empty.")
            return

        # Optional: try to connect to the database using the provided credentials
        test_connection_string = f'Driver={{SQL Server}};Server=192.168.60.5\\innova;Database=Innova;Uid={username};Pwd={password};TrustServerCertificate=yes;'
        try:
            # This is just a test connection to check if the credentials are valid
            pyodbc.connect(test_connection_string)
        except pyodbc.Error:
            QMessageBox.warning(self, "Error", "Failed to connect with the provided credentials.")
            return

        self.accept()

    def get_credentials(self):
        return self.username_field.text(), self.password_field.text()