import os
import nuke
import yaml
import getpass

def get_yaml_var(variable):
    """
    Loads the YAML file at file_path and retrieves the value of 'my_variable'.

    Args:
        variable (str): Variable to fetch from the .yaml

    Returns:
        str: The value of 'variable', or None if not found.
    """
    # Get the directory of the current Python file (dev/toolkit)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the parent directory (dev)
    parent_dir = os.path.dirname(current_dir)

    # Build the path to the config.yaml file
    config_file_path = os.path.join(parent_dir, "config.yaml")

    try:
        with open(config_file_path, 'r') as file:
            config = yaml.safe_load(file)
            return config.get(variable)
    except Exception as e:
        print(f"Error reading YAML file: {e}")
        return None


def export_selected_nodes():
    """
    Exports the currently selected nodes in Nuke to a .nk file in the specified directory.

    Args:
        file_name (str, optional): The name of the file to create. Defaults to "exported_nodes.nk".

    Returns:
        None
    """
    filename = "netcopy.nk"

    selected_nodes = nuke.selectedNodes()
    if not selected_nodes:
        nuke.message("No nodes selected!")
        return

    # Create the export directory if it doesn't exist.
    export_dir = get_yaml_var("base_dir")
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    current_user = get_current_user()

    file_path = os.path.join(export_dir, current_user, filename)

    # Export the selected nodes to the file.
    nuke.nodeCopy(file_path)
    nuke.message("Selected nodes have been Network copied to: " + file_path)

def get_current_user():
    try:
        # Try to get the current user's login name.
        current_user = os.getlogin()
    except Exception:
        # os.getlogin() may fail in some contexts (e.g., services); fallback to getpass.
        current_user = getpass.getuser()

    return current_user

def ensure_current_user_folder_exist():
    """
    Checks if a folder named after the current user exists in the given base directory.
    """
    directory = get_yaml_var("base_dir")

    # Construct the expected path to the user's folder.
    user_folder = os.path.join(directory, get_current_user())

    # Check if the folder exists and is a directory.
    if not os.path.isdir(user_folder):
        os.makedirs(user_folder)
