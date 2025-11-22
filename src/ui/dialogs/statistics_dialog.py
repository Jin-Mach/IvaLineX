from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTabWidget, QWidget

from src.ui.dialogs.widgets.progress_graph_widget import ProgressGraphWidget


class StatisticsDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("statisticsDialog")
        self.setMinimumSize(800, 600)
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        font = QFont()
        font.setBold(True)
        main_layout = QVBoxLayout()
        project_name_layout = QHBoxLayout()
        self.project_name_text = QLabel()
        self.project_name_text.setObjectName("projectNameText")
        self.project_combobox = QComboBox()
        self.project_combobox.setObjectName("projectCombobox")
        self.info_label_text = QLabel()
        self.info_label_text.setObjectName("infoLabelText")
        self.info_label_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label_text.setFont(font)
        self.info_label_text.setVisible(True)
        self.count_widget = QWidget()
        self.count_widget.setVisible(False)
        count_layout = QVBoxLayout()
        total_count_layout = QHBoxLayout()
        self.total_count_text = QLabel()
        self.total_count_text.setObjectName("totalCountText")
        self.total_count_text.setFont(font)
        detail_count_layout = QHBoxLayout()
        self.detail_code_count_text = QLabel()
        self.detail_code_count_text.setObjectName("detailCodeCountText")
        self.detail_empty_count_text = QLabel()
        self.detail_empty_count_text.setObjectName("detailEmptyCountText")
        self.detail_comments_count_text = QLabel()
        self.detail_comments_count_text.setObjectName("detailCommentsCountText")
        self.graph_tab_widget = QTabWidget()
        self.graph_tab_widget.setObjectName("graphTabWidget")
        self.progress_graph_widget = ProgressGraphWidget(self)
        self.graph_tab_widget.addTab(self.progress_graph_widget, "")
        legend_layout = QHBoxLayout()
        self.code_legend_text = QLabel()
        self.code_legend_text.setObjectName("codeLegendText")
        code_box = QLabel()
        code_box.setStyleSheet("background-color: #2E86C1; border: 1px solid black;")
        self.empty_legend_text = QLabel()
        self.empty_legend_text.setObjectName("emptyLegendText")
        empty_box = QLabel()
        empty_box.setStyleSheet("background-color: #F1C40F; border: 1px solid black;")
        self.comments_legend_text = QLabel()
        self.comments_legend_text.setObjectName("commentsLegendText")
        comments_box = QLabel()
        comments_box.setStyleSheet("background-color: #C0392B; border: 1px solid black;")
        project_name_layout.addStretch()
        project_name_layout.addWidget(self.project_name_text)
        project_name_layout.addWidget(self.project_combobox)
        project_name_layout.addStretch()
        total_count_layout.addStretch()
        total_count_layout.addWidget(self.total_count_text)
        total_count_layout.addStretch()
        detail_count_layout.addStretch()
        labels = [self.detail_code_count_text, self.detail_empty_count_text, self.detail_comments_count_text]
        for label in labels:
            detail_count_layout.addStretch()
            detail_count_layout.addWidget(label)
        detail_count_layout.addStretch()
        legends = [[code_box, self.code_legend_text], [empty_box, self.empty_legend_text], [comments_box, self.comments_legend_text]]
        for box, text in legends:
            box.setFixedSize(15, 15)
            legend_layout.addWidget(box)
            legend_layout.addWidget(text)
            legend_layout.addSpacing(10)
        legend_layout.addStretch()
        count_layout.addLayout(total_count_layout)
        count_layout.addLayout(detail_count_layout)
        count_layout.addWidget(self.graph_tab_widget)
        self.count_widget.setLayout(count_layout)
        main_layout.addLayout(project_name_layout)
        main_layout.addWidget(self.info_label_text)
        main_layout.addWidget(self.count_widget)
        return main_layout

    def set_ui_text(self, title: str, project: str, placeholder: str, projects_list: list[str], total: str, code_count: str,
                    empty_count: str, comments_count: str, info_text: str, progress_tab: str, code_legend: str,
                    empty_legend: str, comments_legend: str) -> None:
        self.setWindowTitle(title)
        self.project_name_text.setText(project)
        self.project_combobox.setPlaceholderText(placeholder)
        self.project_combobox.addItems(projects_list)
        self.total_count_text.setText(total)
        self.detail_code_count_text.setText(code_count)
        self.detail_empty_count_text.setText(empty_count)
        self.detail_comments_count_text.setText(comments_count)
        self.info_label_text.setText(info_text)
        self.graph_tab_widget.setTabText(0, progress_tab)
        self.code_legend_text.setText(code_legend)
        self.empty_legend_text.setText(empty_legend)
        self.comments_legend_text.setText(comments_legend)

    def update_values(self, total: str, code: str, empty: str, comments: str) -> None:
        labels = [[self.total_count_text, total], [self.detail_code_count_text, code], [self.detail_empty_count_text, empty],
                  [self.detail_comments_count_text, comments]]
        for label, value in labels:
            default_text = label.text().rsplit(":", 1)[0].strip()
            label.setText(f"{default_text}: {value}")

    def set_visible(self) -> None:
        self.info_label_text.setVisible(False)
        self.count_widget.setVisible(True)