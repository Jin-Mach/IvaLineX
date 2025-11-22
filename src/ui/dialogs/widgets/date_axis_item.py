from pyqtgraph import AxisItem
from PyQt6.QtCore import QDateTime

class DateAxisItem(AxisItem):
    def tickStrings(self, values, scale, spacing):
        strings = []
        for value in values:
            date_time = QDateTime.fromMSecsSinceEpoch(int(value))
            strings.append(date_time.toString("yyyy-MM-dd"))
        return strings