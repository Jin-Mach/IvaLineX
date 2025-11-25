import pyqtgraph as pg

from PyQt6.QtWidgets import QToolTip
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import QDateTime

from src.ui.dialogs.widgets.date_axis_item import DateAxisItem


class ProgressGraphWidget(pg.PlotWidget):
    MAX_VISIBLE_POINTS = 20

    def __init__(self, parent=None) -> None:
        axis = DateAxisItem(orientation="bottom")
        super().__init__(parent, axisItems={"bottom": axis})
        self.setBackground("#2E2E2E")
        self.view_box = self.getPlotItem().getViewBox()
        self.view_box.setMouseEnabled(x=True, y=False)
        self.view_box.enableAutoRange(False, False)
        self.getPlotItem().showGrid(x=True, y=True)
        self.getPlotItem().hideButtons()
        self.scatter = None
        self.line = None
        self.tooltips = []
        self.scene().sigMouseMoved.connect(self.on_hover)


    def set_plot_data(self, x_values: list[int], y_values: list[int], detail_data_dict: dict[str, dict[str, int]],
                      total_label: str, code_label: str, empty_label: str, comments_label: str) -> None:
        if self.line is not None:
            self.removeItem(self.line)
        if self.scatter is not None:
            self.removeItem(self.scatter)
        self.line = self.plot(x_values, y_values, pen="#8AB4F8")
        self.tooltips.clear()
        for date_str in detail_data_dict:
            counts = detail_data_dict[date_str]
            date_time = QDateTime.fromString(date_str, "yyyy-MM-ddTHH:mm:ss.zzz")
            code = counts.get("code", "N/A")
            empty = counts.get("empty", "N/A")
            comments = counts.get("comments", "N/A")
            tooltip = date_time.toString("yyyy-MM-dd HH:mm:ss") + "\n"
            if isinstance(code, int) and isinstance(empty, int) and isinstance(comments, int):
                tooltip += f"{total_label}: {code + empty + comments}\n"
            else:
                tooltip += f"{total_label}: N/A\n"
            tooltip += f"{code_label}: {code}\n"
            tooltip += f"{empty_label}: {empty}\n"
            tooltip += f"{comments_label}: {comments}"
            self.tooltips.append(tooltip)
        scatter_spots = []
        for i, val in enumerate(x_values):
            scatter_spots.append({"pos": (val, y_values[i]), "data": i})
        self.scatter = pg.ScatterPlotItem(spots=scatter_spots, pen=pg.mkPen("#8AB4F8"), brush=pg.mkBrush("#8AB4F8"), size=12)
        self.addItem(self.scatter)
        min_x_value = min(x_values)
        max_x_value = max(x_values)
        min_y_value = min(y_values)
        max_y_value = max(y_values)
        padding_x = (max_x_value - min_x_value) * 0.05 if (max_x_value - min_x_value) > 0 else 1
        padding_y = (max_y_value - min_y_value) * 0.1 if (max_y_value - min_y_value) > 0 else 1
        self.view_box.setLimits(xMin=min_x_value - padding_x, xMax=max_x_value + padding_x, yMin=min_y_value - padding_y,
                     yMax=max_y_value + padding_y)
        if len(x_values) > self.MAX_VISIBLE_POINTS:
            start_index = len(x_values) - self.MAX_VISIBLE_POINTS
            visible_x_min = x_values[start_index]
            visible_x_max = x_values[-1]
        else:
            visible_x_min = min_x_value
            visible_x_max = max_x_value
        self.view_box.setXRange(visible_x_min, visible_x_max, padding=0)
        self.view_box.setYRange(min_y_value, max_y_value + padding_y, padding=0)

    def on_hover(self, pos) -> None:
        if not self.scatter:
            return
        mouse_point = self.getPlotItem().vb.mapSceneToView(pos)
        pts = self.scatter.pointsAt(mouse_point)
        if pts.size > 0:
            index = pts[0].data()
            if 0 <= index < len(self.tooltips):
                QToolTip.showText(QCursor.pos(), self.tooltips[index])