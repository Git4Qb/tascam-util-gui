# tuxam/ui/widgets/device_list.py

from PySide6.QtWidgets import QComboBox, QStyledItemDelegate
from PySide6.QtCore import Qt


class CenteredItemDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index, /):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter


class DeviceDropdown(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setEditable(False)
        self.setMaxVisibleItems(6)
        self.view().setMinimumHeight(80)
        self.setItemDelegate(CenteredItemDelegate(self))

    def showPopup(self):
        super().showPopup()

        popup = self.view().window()
        pos = self.mapToGlobal(self.rect().bottomLeft())
        popup.move(pos)