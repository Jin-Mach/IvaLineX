import pyqtgraph as pg

from PyQt6.QtWidgets import QToolTip
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import QDateTime

from src.ui.dialogs.widgets.date_axis_item import DateAxisItem


class ProgressGraphWidget(pg.PlotWidget):
    MAX_VISIBLE_POINTS = 10

    def __init__(self, parent=None) -> None:
        axis = DateAxisItem(orientation="bottom")
        super().__init__(parent, axisItems={"bottom": axis})
        self.setBackground("w")
        self.getPlotItem().showGrid(x=True, y=True)
        self.scatter = None
        self.line = None
        self.tooltips = []
        vb = self.getPlotItem().getViewBox()
        vb.wheelEvent = lambda ev: None
        vb.setMouseEnabled(x=True, y=False)
        self.scene().sigMouseMoved.connect(self.on_hover)

    def set_plot_data(self, x: list[float], y: list[int], detail_data: dict[str, dict[str, int]],
                      code: str, empty: str, comments: str) -> None:
        self.clear()
        self.line = self.plot(x, y, pen="b")
        self.tooltips = []
        for timestamp_str in detail_data:
            date_time = QDateTime.fromString(timestamp_str, "yyyy-MM-ddTHH:mm:ss.zzz")
            counts = detail_data[timestamp_str]
            self.tooltips.append(
                f"{date_time.toString('yyyy-MM-dd HH:mm:ss')}\n"
                f"{code}: {counts.get('code', 'N/A')}\n"
                f"{empty}: {counts.get('empty', 'N/A')}\n"
                f"{comments}: {counts.get('comments', 'N/A')}"
            )
        spots = []
        for x_value in range(len(x)):
            point = {"pos": (x[x_value], y[x_value]), "data": x_value}
            spots.append(point)
        self.scatter = pg.ScatterPlotItem(
            spots=spots, pen=pg.mkPen("b"), brush=pg.mkBrush("b"), size=10
        )
        self.addItem(self.scatter)
        view_box = self.getPlotItem().getViewBox()
        view_box.disableAutoRange()
        if len(x) > self.MAX_VISIBLE_POINTS:
            start = len(x) - self.MAX_VISIBLE_POINTS
            min_x = x[start]
            max_x = x[-1]
        else:
            min_x = min(x)
            max_x = max(x)
        min_y = 0
        max_y = max(y) if y else 1
        view_box.setXRange(min_x, max_x, padding=0)
        view_box.setYRange(min_y, max_y * 1.1, padding=0)
        view_box.setMouseEnabled(x=True, y=False)

    def on_hover(self, pos) -> None:
        if not self.scatter:
            return
        mouse_point = self.getPlotItem().vb.mapSceneToView(pos)
        pts = self.scatter.pointsAt(mouse_point)
        if pts.size > 0:
            index = pts[0].data()
            if 0 <= index < len(self.tooltips):
                QToolTip.showText(QCursor.pos(), self.tooltips[index])