import nuke
import os
import time
from PySide2 import QtCore, QtWidgets, QtGui
import pyperclip
from . import utils

# TODO: update folder naming and refine yaml

class NetCopyPanel(QtWidgets.QWidget):
    """
    Nuke panel for displaying user folders and their latest NetCopy data.
    Allows copying and sending selected NetCopy files.
    """
    _instance = None  # Singleton instance

    def __init__(self, parent=None):
        super(NetCopyPanel, self).__init__(parent)

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)  # Always on top
        self.setWindowTitle("NetCopy")  # Optional: Set a custom window title

        self.table = self._create_table_widget()
        self._setup_ui()
        self._refresh_table()

    # =========================
    # UI CREATION
    # =========================
    def _setup_ui(self):
        """Initialize and configure the user interface."""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.table)
        main_layout.addLayout(self._create_button_panel())
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def _create_button_panel(self):
        """Create the button layout (Refresh, Send Selected, Copy)."""
        button_layout = QtWidgets.QHBoxLayout()

        # Refresh Button
        refresh_button = self._create_icon_button("refresh.png", self._refresh_table)
        button_layout.addWidget(refresh_button)

        # Send Selected Button
        send_button = QtWidgets.QPushButton("Send Selected")
        send_button.clicked.connect(utils.export_selected_nodes)
        button_layout.addWidget(send_button)

        # Copy Button
        copy_button = QtWidgets.QPushButton("Copy")
        copy_button.clicked.connect(self._handle_copy_action)
        button_layout.addWidget(copy_button)

        return button_layout

    def _create_icon_button(self, icon_filename, callback):
        """Helper to create a button with an icon."""
        button = QtWidgets.QPushButton()
        button.clicked.connect(callback)

        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons", icon_filename)
        button.setIcon(QtGui.QIcon(icon_path))
        button.setIconSize(QtCore.QSize(16, 16))
        button.setFixedSize(24, 24)
        return button

    @staticmethod
    def _create_table_widget():
        """Set up the QTableWidget for displaying user data."""
        table = QtWidgets.QTableWidget(0, 2)
        table.setHorizontalHeaderLabels(['User', 'Latest NetCopy'])
        table.setColumnWidth(0, 200)
        table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        table.setSelectionMode(QtWidgets.QTableView.ExtendedSelection)
        table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        table.setSortingEnabled(True)
        table.sortByColumn(1, QtCore.Qt.DescendingOrder)
        table.setAlternatingRowColors(True)
        return table

    # =========================
    # DATA HANDLING
    # =========================
    def _refresh_table(self):
        """Refresh table data with updated folder information."""
        self.table.clearContents()
        self.table.setRowCount(0)
        self._populate_table()

    def _populate_table(self):
        """Retrieve folder data and populate the table."""
        base_dir = utils.get_yaml_var("base_dir")

        if not os.path.isdir(base_dir):
            nuke.message("Provided path is not a directory!")
            return

        utils.ensure_current_user_folder_exists()
        folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

        self.table.setRowCount(len(folders))

        for row, folder in enumerate(folders):
            # Folder Name
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(folder))

            # Last Modified Date
            netcopy_path = os.path.join(base_dir, folder, "netcopy.nk")
            last_modified_str = time.ctime(os.path.getmtime(netcopy_path)) if os.path.isfile(netcopy_path) else "Not found"
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(last_modified_str))

    # =========================
    # EVENT HANDLERS
    # =========================
    def _handle_copy_action(self):
        """Copy the contents of the selected netcopy.nk files to the clipboard."""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            nuke.message("No row selected!")
            return

        base_dir = utils.get_yaml_var("base_dir")

        for index in selected_rows:
            user_folder = self.table.item(index.row(), 0).text()
            file_path = os.path.join(base_dir, user_folder, "netcopy.nk")

            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r") as file:
                        file_contents = file.read()
                        pyperclip.copy(file_contents)  # Copy using pyperclip
                    nuke.message(f"Contents of '{file_path}' copied to clipboard.")
                except Exception as e:
                    nuke.message(f"Error reading '{file_path}': {str(e)}")
            else:
                nuke.message(f"File '{file_path}' not found.")

    # =========================
    # EXPOSED METHODS
    # =========================
    @staticmethod
    def open_panel():
        """Opens the NetCopyPanel singleton instance."""
        if NetCopyPanel._instance is None:
            NetCopyPanel._instance = NetCopyPanel()
        NetCopyPanel._instance.resize(600, 400)
        NetCopyPanel._instance.show()
        return NetCopyPanel._instance