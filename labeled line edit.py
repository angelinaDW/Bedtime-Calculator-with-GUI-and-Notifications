from qtpy.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QApplication

class LabeledLineEdit(QWidget):
    '''
    A useful, simple little widget that lets you couple a label and a lineedit.
    '''

    def __init__(self, labelText:str, defaultLineEditContents:str = "", position = "", parent=None,):
            super(LabeledLineEdit, self).__init__()
            self.layout = QHBoxLayout()
            
            self.label = QLabel()
            self.label.setText(labelText)

            self.lineEdit = QLineEdit()
            self.lineEdit.setText(defaultLineEditContents)

            # Actually adds the widgets to the layout
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.lineEdit)
            self.setLayout(self.layout)

    def getLineEdit():
        return lineEdit
            

    def setLabelText(what):
        self.label.setText(what)

    def setLineEditText(what):
        self.lineEdit.setText(what)





if __name__ == "__main__":
    app = QApplication([])
    testLabeledLineEdit = LabeledLineEdit(labelText="Enter your password: ")
    testLabeledLineEdit.show()
    #h = QLabel("hi")
    #h.show()
    app.exec_()
