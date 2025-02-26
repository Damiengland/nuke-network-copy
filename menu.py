import nuke
from nukescripts import panels
from toolkit.panel import NetCopyPanel
# # Add menu to Nuke
# main_menu = nuke.menu("Nuke")
# sub_menu = main_menu.findItem("Utilities")
#
# if not sub_menu:
#     sub_menu = main_menu.addMenu("Utilities")
#
# def add_menu():
#     srPanel = NetworkCopy()
#     return srPanel.show()
#
# sub_menu.addCommand("NetCopy/Send Selected", add_menu)
# sub_menu.addCommand("NetCopy/Copy From User...", add_menu)

# Register the NetCopyPanel as a panel in Nuke.
panels.registerWidgetAsPanel('NetCopyPanel', 'NetCopy', 'netcopy.mellowpictures.com.au')