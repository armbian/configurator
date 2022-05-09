import sys

from PyQt5.QtWidgets import QAbstractItemView, QApplication, QCheckBox, QWidget, QPushButton, QListWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSlot, Qt

class SelectionMenu(QWidget):
    def __init__(self, title, choices=[], selected_choices=[]):
        super().__init__()
        self.title = title
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.choices = choices
        self.selections = [set(), set()]
        self.initUI(choices, selected_choices)
    
    def checked_items(self):
        checked = set()
        unchecked = set()
        for item_i in range(self.selectionList.count()):
            item = self.selectionList.item(item_i)
            item_text = item.text()
            
            if item.checkState():
                checked.add(item_text)
            else:
                unchecked.add(item_text)
        return checked, unchecked
    
    def cb_cancel(self):
        sys.exit(1)
        
    def cb_select(self):
        self.selections = self.checked_items()
        self.close()
    
    def initUI(self, choices=[], selected_choices=[]):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        layout = QVBoxLayout(self)
        
        selectionList = QListWidget(self)
        for choice in choices:
            item = QListWidgetItem(choice, selectionList)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            state = Qt.Checked if choice in selected_choices else Qt.Unchecked
            item.setCheckState(state)

        #selectionList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.selectionList = selectionList
        #selectionList.itemSelectionChanged.connect(self.cb_selection_changed)
        #selectionList.itemChanged.connect(self.cb_item_changed)
        layout.addWidget(selectionList)
        
        buttonsLayout = QHBoxLayout(self)
        button = QPushButton('Cancel', self)
        button.setToolTip('Cancel the operation')
        button.clicked.connect(self.cb_cancel)
        buttonsLayout.addWidget(button)
        
        button = QPushButton('Select', self)
        button.setToolTip('This is an example button')
        button.clicked.connect(self.cb_select)
        #button.setEnabled(False)
        buttonsLayout.addWidget(button)
        self.select_button = button
        
        layout.addLayout(buttonsLayout)
        self.setLayout(layout)
        
        self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

def provide_user_choice(choices=[], selected_choices=[]):
    app = QApplication(sys.argv)
    ex = SelectionMenu(title="Armbian docker installation module", choices=choices, selected_choices=selected_choices)
    app.exec_()
    return ex.selections
