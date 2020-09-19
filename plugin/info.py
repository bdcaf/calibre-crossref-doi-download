from PyQt5.Qt import QDialog, QVBoxLayout, QPushButton, QMessageBox, QLabel, QScrollArea
class AnotherWindow(QDialog):
    """
    This "window" is a QWidget. If it has no parent, it 
    will appear as a free-floating window as we want.
    """
    def __init__(self, gui, text):
        QDialog.__init__(self, gui)
        layout = QVBoxLayout()
        self.label = QLabel(text)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.label)
        layout.addWidget(self.scroll)
        self.setLayout(layout)
        self.resize(self.sizeHint())
