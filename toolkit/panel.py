import nuke
import os
import time
from PySide2 import QtCore, QtWidgets, QtGui
from . import utils

#TODO: update latest netcopy ui

class NetCopyPanel(QtWidgets.QWidget):
    """
    A Nuke panel widget that displays user information and the latest NetCopy data in a table.
    """

    def __init__(self, parent=None):
        """
        Initialize the NetCopy panel.

        Args:
            parent (QWidget, optional): The parent widget.
        """
        super(NetCopyPanel, self).__init__(parent)
        self._table = self._build_table_widget()
        self._init_ui()
        self.populate_table_with_folders()

    def _init_ui(self):
        """
        Set up the user interface of the panel.
        """
        # Main vertical layout for the panel.
        main_layout = QtWidgets.QVBoxLayout(self)

        # Create and add the table widget to the layout.
        main_layout.addWidget(self._table)

        # Create a horizontal layout for the buttons.
        button_layout = QtWidgets.QHBoxLayout()

        # Create the extra button with an icon.
        extra_button = QtWidgets.QPushButton()
        extra_button.clicked.connect(self.on_refresh_button_clicked)
        # Build the path to the icon; adjust the icon file name/path as needed.
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons", "refresh.png")
        icon = QtGui.QIcon(icon_path)
        extra_button.setIcon(icon)
        extra_button.setIconSize(QtCore.QSize(16, 16))
        # Set a fixed size to roughly the icon's dimensions.
        extra_button.setFixedSize(24, 24)
        button_layout.addWidget(extra_button)

        # Create the "Copy" button.
        send_button = QtWidgets.QPushButton("Send Selected")
        send_button.clicked.connect(utils.export_selected_nodes)
        button_layout.addWidget(send_button)

        # Create the "Paste" button.
        copy_button = QtWidgets.QPushButton("Copy")
        copy_button.clicked.connect(self.on_copy_button_clicked)
        button_layout.addWidget(copy_button)

        # Add the button layout to the main layout.
        main_layout.addLayout(button_layout)

        # Set the panel to expand in both directions.
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def populate_table_with_folders(self):
        """
        Retrieves all subfolders from the given directory, checks each folder for a file named "netcopy.nk",
        gets its last modified time if present, and populates the table with the folder name in the first column and
        the last modified time in the second column.
        """
        directory = utils.get_yaml_var("base_dir")

        if not os.path.isdir(directory):
            nuke.message("Provided path is not a directory!")
            return

        utils.ensure_current_user_folder_exist()

        # List only subdirectories
        folders = [f for f in os.listdir(directory)
                   if os.path.isdir(os.path.join(directory, f))]

        self._table.setRowCount(len(folders))
        for row, folder in enumerate(folders):
            # Create a table item for the folder name.
            folder_item = QtWidgets.QTableWidgetItem(folder)
            self._table.setItem(row, 0, folder_item)

            # Build the path to "netcopy.nk" inside the folder.
            netcopy_file = os.path.join(directory, folder, "netcopy.nk")
            if os.path.exists(netcopy_file) and os.path.isfile(netcopy_file):
                # Get the last modified time and convert it to a human-readable string.
                last_modified = os.path.getmtime(netcopy_file)
                last_modified_str = time.ctime(last_modified)
            else:
                last_modified_str = "Not found"

            # Create a table item for the last modified time.
            netcopy_item = QtWidgets.QTableWidgetItem(last_modified_str)
            self._table.setItem(row, 1, netcopy_item)

    @staticmethod
    def _build_table_widget():
        """
        Create and configure a QTableWidget to display the NetCopy data.

        Returns:
            QTableWidget: A configured table widget.
        """
        table = QtWidgets.QTableWidget()

        # Define the header labels for the table.
        headers = ['User', 'Latest NetCopy']
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        # Configure column sizing:
        table.setColumnWidth(0, 200)  # Fixed width for the first column.
        table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)  # Stretch the second column.

        # Configure selection and sorting behavior.
        table.setSelectionMode(QtWidgets.QTableView.ExtendedSelection)  # Allow selection of multiple rows.
        table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)  # Entire rows are selected.
        table.setSortingEnabled(True)  # Enable sorting.
        table.sortByColumn(1, QtCore.Qt.DescendingOrder)  # Sort the second column descending.

        # Visual appearance settings.
        table.setAlternatingRowColors(True)  # Use alternating row colors.
        table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  # Disable horizontal scroll bar.

        # Set an initial number of rows.
        table.setRowCount(5)

        # Ensure the table expands with the layout.
        table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        return table

    def on_copy_button_clicked(self):
        """
        Handler for the "Copy" button. Retrieves the selected row(s) from the table,
        gets the user name from the first column, and if a file named "netcopy.nk"
        exists in that user's directory, copies its contents to the clipboard.
        """
        selected_rows = self._table.selectionModel().selectedRows()
        if not selected_rows:
            nuke.message("No row selected!")
            return

        for index in selected_rows:
            row = index.row()
            user_item = self._table.item(row, 0)
            if user_item:
                user = user_item.text()
                # Construct the path to the netcopy.nk file using the base directory from YAML.
                netcopy_file = os.path.join(utils.get_yaml_var("base_dir"), user, "netcopy.nk")
                if os.path.isfile(netcopy_file):
                    try:
                        with open(netcopy_file, "r") as f:
                            file_contents = f.read()
                        # Copy the contents to the clipboard using Qt's clipboard.
                        clipboard = QtWidgets.QApplication.clipboard()
                        clipboard.setText(file_contents)
                        nuke.message("Contents of\n '{}' have been copied to the clipboard.".format(netcopy_file))
                    except Exception as e:
                        nuke.message("Error copying file contents: " + str(e))
                else:
                    nuke.message("File '{}' not found.".format(netcopy_file))
            else:
                nuke.message("No user found in row " + str(row))

    def on_refresh_button_clicked(self):
        """
        Handler for the extra icon button.
        Clears the table and repopulates it using the base directory from the YAML configuration.
        """
        # Clear all contents from the table.
        self._table.clearContents()
        self._table.setRowCount(0)
        self.populate_table_with_folders()


