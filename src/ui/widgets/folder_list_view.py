from PyQt6.QtCore import QStringListModel, QModelIndex
from PyQt6.QtWidgets import QListView, QAbstractItemView


class FolderListView(QListView):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.setObjectName("folderListView")
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setUniformItemSizes(True)
        self.model = QStringListModel()
        self.setModel(self.model)

    def update_data(self, data: list[str]) -> None:
        self.model.setStringList(data)

    def clear_model(self) -> None:
        self.model.setStringList([])

    def remove_item(self, index: QModelIndex) -> None:
        row = index.row()
        current_list = self.model.stringList()
        current_list.pop(row)
        self.model.setStringList(current_list)