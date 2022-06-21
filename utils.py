from qtpy.QtWidgets import *
from PyQt5.QtGui import *
import PyQt5.QtGui as QtGui
from PyQt5.QtCore import *

def layoutAddWidgets(self, *widgets:list):
    for widget in widgets:
        self.addWidget(widget)

class PositiveIntValidator(QValidator):
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def validate(self, s, cursorPos):
        print(s)
        if s.isdigit() and int(s) >= 0:
            print("yes")
            return (QtGui.QValidator.Acceptable, cursorPos)
        else:
            return (QtGui.QValidator.Invalid, cursorPos)

class LabeledLineEdit(QWidget):
    '''
    A useful, simple little widget that lets you couple a label and a lineedit.
    '''

    def __init__(self, labelText:str, defaultLineEditContents:str = "", position = "", parent=None,):
            super().__init__()
            self.layout = QHBoxLayout()
            
            self.label = QLabel()
            self.label.setText(labelText)

            self.lineEdit = QLineEdit()
            self.lineEdit.setText(defaultLineEditContents)

            # Actually adds the widgets to the layout
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.lineEdit)
            self.setLayout(self.layout)
    def setLabelText(self, what):
        self.label.setText(what)

    def getInputtedText(self):
        return self.lineEdit.text()
    
    def setLineEditText(self, what):
        self.lineEdit.setText(what)


class LabeledTimeEdit(QWidget):
    '''
    A useful, simple little widget that lets you couple a label and a lineedit.
    '''

    def __init__(self, labelText:str, position = "", parent=None,):
            super().__init__()
            self.layout = QHBoxLayout()
            
            self.label = QLabel()
            self.label.setText(labelText)

            self.timeEdit = QTimeEdit()

            # Actually adds the widgets to the layout
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.timeEdit)
            self.setLayout(self.layout)

    def getTime(self) -> str:
        return self.timeEdit.text()
    
    def setTime(self, time : str):
        self.timeEdit.setTime(QTime.fromString(time))
    def setLabelText(self, what):
        self.label.setText(what)

'''
if __name__ == "__main__":
    app = QApplication([])
    testLabeledLineEdit = LabeledLineEdit(labelText="Enter your password: ")
    testLabeledLineEdit.show()
    #h = QLabel("hi")
    #h.show()
    app.exec_()
'''
