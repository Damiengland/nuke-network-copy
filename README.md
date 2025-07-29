# **NetCopy Tool for Nuke**

NetCopy is a Nuke panel designed to streamline the process of sharing Nuke nodes between artists on a local network. It allows users to quickly export selected nodes to a shared location and easily copy other artists' exported nodes to their own clipboard for pasting into their Nuke scripts.

## **Features**

* **Export Selected Nodes:** Easily export your currently selected Nuke nodes to a .nk file in your designated user folder on the network.  
* **Browse Shared NetCopies:** View a list of all artists' shared folders and the last time their netcopy.nk file was updated.  
* **Copy Shared Nodes:** Select an artist's entry in the panel and copy the contents of their netcopy.nk file directly to your clipboard.  
* **Always On Top:** The NetCopy panel stays on top of other Nuke windows for convenient access.  
* **Sortable Table:** Sort shared entries by user or last modified date.

## **Installation**

1. **Clone or Download:** Download or clone this repository to a location accessible by your Nuke setup (e.g., your .nuke folder, or a shared network drive). The cloned repository should contain the netcopy\_tool folder and a config.yaml file in its root.  
2. **Configure base\_dir:**  
   * Edit the config.yaml file located in the root directory of the NetCopy tool (the same directory that contains the netcopy\_tool folder).  
   * Update the base\_dir entry to point to your desired shared network folder where all user-specific netcopy.nk files will be stored.

base\_dir: "Q:/path/to/your/shared/netcopy\_folder"

**Example config.yaml:**base\_dir: "//network\_share/nuke\_assets/NetCopies"

*Ensure this base\_dir path exists and all users have read/write permissions to it.*

## **Usage**

1. **Open the Panel:** In Nuke, navigate to Tools \> NetCopy in the main menu bar.  
2. **Export Nodes:**  
   * Select the Nuke nodes you wish to share in your current script.  
   * Click the "Send Selected" button in the NetCopy panel. This will export your selected nodes to a netcopy.nk file in your personal folder within the base\_dir.  
3. **Copy Other Artists' Nodes:**  
   * The table will display all users who have exported nodes and the last time they updated their netcopy.nk.  
   * Select one or more rows corresponding to the artists whose nodes you want to copy.  
   * Click the "Copy" button. The contents of their netcopy.nk file(s) will be copied to your system clipboard.  
   * You can then paste these nodes directly into your Nuke script (e.g., by pressing Ctrl+V or Cmd+V).  
4. **Refresh:** Click the "Refresh" button to update the list of user folders and their latest NetCopy data.

## **Requirements**

* Nuke (Tested with Nuke 12.x and above)  
* Python 2.7 or 3.x (depending on your Nuke version)  
* PySide2 (Comes with Nuke)  
* pyperclip (for clipboard operations \- you might need to install this if it's not present in your Nuke environment):  
  \# You might need to use pip specific to your Nuke's Python environment  
  \# For Nuke 12.x (Python 2.7)  
  \# nuke \-t \-c "import pip; pip.main(\['install', 'pyperclip'\])"  
  \# For Nuke 13.x+ (Python 3.x)  
  nuke \-t \-c "import subprocess; subprocess.call(\[sys.executable, '-m', 'pip', 'install', 'pyperclip'\])

* PyYAML (for reading the config file \- you might need to install this):  
  \# For Nuke 13.x+ (Python 3.x)  
  nuke \-t \-c "import subprocess; subprocess.call(\[sys.executable, '-m', 'pip', 'install', 'PyYAML'\])

## **Contributing**

Feel free to fork the repository, make improvements, and submit pull requests.

## **License**

This project is open-source and available under the [MIT License](http://docs.google.com/LICENSE.md) (if you plan to use MIT, otherwise specify your license).