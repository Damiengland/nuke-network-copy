import nuke
import nukescripts
from network_copy import NetworkCopy

# Add menu to Nuke
main_menu = nuke.menu("Nuke")
sub_menu = main_menu.findItem("Utilities")

if not sub_menu:
    sub_menu = main_menu.addMenu("Utilities")

def add_pane():
    net_copy = NetworkCopy()
    return net_copy.addToPane()


def add_menu():
    srPanel = NetworkCopy()
    return srPanel.show()


pane_menu = nuke.menu('Pane')
pane_menu.addCommand('NetCopy', add_pane)
nukescripts.registerPanel('NetCopy', add_pane)

sub_menu.addCommand("NetCopy/Copy Selected", add_menu)
sub_menu.addCommand("NetCopy/Copy From User...", add_menu)