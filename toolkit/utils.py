import os
import nuke
import yaml
import getpass
from yaml.parser import ParserError
from yaml.scanner import ScannerError


def get_config_file_path():
    """
    Retrieves the absolute path to the config.yaml file.

    Returns:
        str: Full path to the config.yaml file.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Current file directory
    parent_dir = os.path.dirname(current_dir)  # Parent directory
    return os.path.join(parent_dir, "config.yaml")


def get_yaml_var(key):
    """
    Reads the config.yaml file and retrieves the value for the specified key.

    Args:
        key (str): The key to fetch from the YAML file.

    Returns:
        Any: Value associated with the key, or None if not found.
    """
    config_file_path = get_config_file_path()

    try:
        with open(config_file_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            return config.get(key)
    except FileNotFoundError:
        print(f"[ERROR] Config file not found at: {config_file_path}")
    except PermissionError:
        print(f"[ERROR] Permission denied while accessing: {config_file_path}")
    except (ParserError, ScannerError) as e:
        print(f"[ERROR] YAML parsing error in {config_file_path}: {e}")
    except OSError as e:
        print(f"[ERROR] OS error while reading config file: {e}")
    return None


def get_current_user():
    """
    Retrieves the current system user's login name.

    Returns:
        str: Username of the current user.
    """
    try:
        return os.getlogin()
    except OSError:
        # Fallback if os.getlogin() fails
        return getpass.getuser()


def get_user_folder_path():
    """
    Constructs the path to the current user's folder based on the base directory from the config.

    Returns:
        str: Path to the user's folder or None if base_dir isn't found.
    """
    base_dir = get_yaml_var("base_dir")
    if not base_dir:
        print("[ERROR] 'base_dir' not found in the configuration.")
        return None
    return os.path.join(base_dir, get_current_user())


def ensure_current_user_folder_exists():
    """
    Ensures that a folder for the current user exists in the base directory.
    Creates it if it does not exist.
    """
    user_folder = get_user_folder_path()
    if not user_folder:
        return

    if not os.path.isdir(user_folder):
        try:
            os.makedirs(user_folder)
            print(f"[INFO] Created user folder at: {user_folder}")
        except FileExistsError:
            print(f"[WARNING] A file with the same name as the user folder exists: {user_folder}")
        except PermissionError:
            print(f"[ERROR] Permission denied while creating folder: {user_folder}")
        except OSError as e:
            print(f"[ERROR] OS error while creating user folder: {e}")


def export_selected_nodes():
    """
    Exports selected Nuke nodes to a .nk file in the user's designated folder.
    """
    
    selected_nodes = nuke.selectedNodes()
    if not selected_nodes:
        nuke.message("[WARNING] No nodes selected!")
        return

    ensure_current_user_folder_exists()
    user_folder = get_user_folder_path()

    if not user_folder:
        nuke.message("[ERROR] Failed to retrieve user folder path.")
        return

    export_path = os.path.join(user_folder, "netcopy.nk")
    try:
        nuke.nodeCopy(export_path)
        nuke.message(f"[SUCCESS] Nodes exported to: \n{export_path}")
    except IOError as e:
        nuke.message(f"[ERROR] I/O error during node export: {e}")
    except nuke.NukeError as e:
        nuke.message(f"[ERROR] Nuke-specific error during node export: {e}")
    except PermissionError:
        nuke.message(f"[ERROR] Permission denied while writing to: {export_path}")