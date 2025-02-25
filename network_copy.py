import nuke
from PySide2 import QtCore, QtWidgets
from nukescripts import panels


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
        self._table = None  # Will hold our QTableWidget instance.
        self._init_ui()

    def _init_ui(self):
        """
        Set up the user interface of the panel.
        """
        # Main vertical layout for the panel.
        main_layout = QtWidgets.QVBoxLayout(self)

        # Create and add the table widget to the layout.
        self._table = self._create_table_widget()
        main_layout.addWidget(self._table)

        # Set the panel to expand in both directions.
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def _create_table_widget(self):
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


# Register the NetCopyPanel as a panel in Nuke.
panels.registerWidgetAsPanel('NetCopyPanel', 'NetCopy', 'mellowpictures.com.au.NetCopy')