import nuke
from nukescripts import panels
from toolkit.panel import NetCopyPanel
from toolkit.utils import export_selected_nodes


def get_or_create_submenu(main_menu, submenu_name):
    """
    Retrieves or creates a submenu in the given main menu.

    Args:
        main_menu (nuke.Menu): The main Nuke menu to search in.
        submenu_name (str): The name of the submenu to retrieve or create.

    Returns:
        nuke.Menu: The found or newly created submenu.
    """
    submenu = main_menu.findItem(submenu_name)
    if not submenu:
        submenu = main_menu.addMenu(submenu_name)
    return submenu


def add_netcopy_commands(submenu):
    """
    Adds NetCopy-related commands to the specified submenu.

    Args:
        submenu (nuke.Menu): The submenu to which commands will be added.
    """
    submenu.addCommand("NetCopy/Send Selected", export_selected_nodes)
    submenu.addCommand("NetCopy/Copy From User...", lambda: NetCopyPanel.open_panel())


def register_netcopy_panel():
    """
    Registers the NetCopyPanel as a dockable panel in Nuke.
    """
    try:
        panels.registerWidgetAsPanel(
            'NetCopyPanel',               # Class name
            'NetCopy',                    # Display name
            'netcopy.mellowpictures.com.au'  # Unique identifier
        )
        print("[INFO] NetCopyPanel registered successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to register NetCopyPanel: {e}")


def initialize_netcopy_menu():
    """
    Initializes the NetCopy menu and registers the panel in Nuke.
    """
    main_menu = nuke.menu("Nuke")
    utilities_menu = get_or_create_submenu(main_menu, "Utilities")

    add_netcopy_commands(utilities_menu)
    register_netcopy_panel()


# Initialize NetCopy integration when this script runs
initialize_netcopy_menu()