from pyqtgraph import PlotWidget


class ProgressGraphWidget(PlotWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)