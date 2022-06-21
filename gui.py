from concurrent.futures import thread
from qtpy.QtWidgets import QMainWindow,  QLayout, QPushButton, QApplication, QLabel, QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QTimeEdit
from utils import *
from calculate_bedtime import *
from datetimeUtils import *
from PyQt5 import QtGui
import utils
import sys
from PyQt5.QtCore import QSize
import calculate_bedtime
import logging
import threading
from notification import *
from calculate_bedtime import *
import load_save_data

notificationDisplaysList : list[NotificationEdit] = []
masterLayout = None
wakeUpTimeEdit, hoursToSleepEdit, bedtimeLabel, addNotificationButton, saveSettingsButton = [None]*5
bedtime: datetime.datetime = None

# Global variables
notificationlist = NotificationsList() # Holds all the notifications
notificationThread : thread = None


# Adds a "monkeypatch" method that allows us to add multiple widgets in one line to a given layout
QLayout.addWidgets = utils.layoutAddWidgets

# Overrides the way that exceptions work, enabling us to see exceptions that exist inside of slots
sys._excepthook = sys.excepthook
def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = exception_hook

# I figured out the problem--the parameter n isn't actually being passed in!
def notificationDestroyCallback(n: NotificationEdit):
    notificationDisplaysList.remove(n)
    # If there is a corresponding notification, destroy it
    n.deleteLater()
    # Update notification thread


def restartWaitNotifyThread():
    global notificationThread, bedtime
    if notificationThread and notificationThread.is_alive():
        notificationlist._stop.set() # tell it to shut down this thread
        print("thread stopped?")
    notificationThread = threading.Thread(target=notificationlist.waitUntilNextNotification, args=(bedtime,)) # Variable for holding the thread that waits for the next notification
    notificationThread.start()
    print("thread started")
    
    
def updateMasterLayout():
    global masterLayout, wakeUpTimeEdit, hoursToSleepEdit, bedtimeLabel, notificationDisplaysList, addNotificationButton, saveSettingsButton
    for i in reversed(range(masterLayout.count())): 
        masterLayout.itemAt(i).widget().setParent(None)
    masterLayout.addWidgets(wakeUpTimeEdit, hoursToSleepEdit, bedtimeLabel, *notificationDisplaysList, addNotificationButton, saveSettingsButton)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global masterLayout, wakeUpTimeEdit, hoursToSleepEdit, bedtimeLabel, addNotificationButton, saveSettingsButton
        global bedtime
        # Setup the window
        self.setWindowTitle("Time2Sleep Calculator")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setFixedSize(QSize(640, 480))
        
        # Create the parts of the UI
        mainWidget = QWidget()
        masterLayout = QVBoxLayout()
        wakeUpTimeEdit = LabeledTimeEdit(labelText="Time to wake up:")
        hoursToSleepEdit = LabeledLineEdit(labelText="Hours of sleep desired:")
        bedtimeLabel = QLabel("Bedtime: ")
        addNotificationButton = QPushButton("Add Notification")
        saveSettingsButton = QPushButton("Save Settings")
        
        # Define and connect button press methods
        def onSaveSettingsPressed():
            # Display an error message if any of the notifications are not filled in correctly (but just ignore them and proceed)
            # Update the list of actual notification objects
            notificationlist.clear()
            for notificationDisplay in notificationDisplaysList:
                try:
                    print("notificationDisplay.minutesBefore(): {}".format(notificationDisplay.minutesBefore()))
                    i = int(notificationDisplay.minutesBefore())
                    assert i > 0
                    notificationlist.createNewNotification(i, notificationDisplay) # Create a notification associated with this
                except:
                    print("There's something wrong with this notification.")
            notificationlist.sort()
            the_dict = {}
            the_dict['wakeupTime'] = wakeUpTimeEdit.getTime()
            the_dict['hoursOfSleep'] = hoursToSleepEdit.getInputtedText()
            the_dict['notifications'] = [str(key) for key in list(notificationlist._internalRep.keys())]
            load_save_data.saveData(the_dict)
            updateBedtimeDisplay()
            restartWaitNotifyThread()
            # Start the thread associated with waiting for the next notification
            
            
        saveSettingsButton.clicked.connect(onSaveSettingsPressed)
        
        def onAddNotificationButtonPressed():
           notificationDisplaysList.append(NotificationEdit(notificationDestroyCallback))
           # Refresh the layout
           updateMasterLayout()
        addNotificationButton.clicked.connect(onAddNotificationButtonPressed)
        
        # Connect method for time or sleep hours edited to method
        def onTimeHoursChanged():
                        
            wakeTime : str = wakeUpTimeEdit.timeEdit.time().toString()
            hours2Sleep : str = hoursToSleepEdit.getInputtedText()
            
            if hoursToSleepEdit.getInputtedText() == "":
                return
            try:
                i = int(hours2Sleep)
                if i < 0:
                    raise Exception()
            except:
                print("The value input for # of hours to sleep was invalid")

            updateBedtimeDisplay()            
        wakeUpTimeEdit.timeEdit.userTimeChanged.connect(onTimeHoursChanged)
        hoursToSleepEdit.lineEdit.editingFinished.connect(onTimeHoursChanged)
        
        # Finally, actually setup the display
        updateMasterLayout()
        mainWidget.setLayout(masterLayout)
        self.setCentralWidget(mainWidget)

def updateBedtimeDisplay():
    global bedtime
    wakeTime : str = wakeUpTimeEdit.timeEdit.time().toString()
    hours2Sleep : str = hoursToSleepEdit.getInputtedText()
    bedtime = calculate_bedtime.calculateBedtime(timeStrToDateTime(wakeTime), int(hours2Sleep) )
    print(type(bedtime))
    bedtimeLabel.setText("Bedtime: {}".format(bedtime.time().strftime("%I:%M %p") ))
 

def loadDataFromFileAndUpdateGUI():
    d : dict = load_save_data.loadData()
    print(f"data: {d}")
    wakeUpTimeEdit.setTime(d['wakeupTime'])
    hoursToSleepEdit.setLineEditText(d['hoursOfSleep'])
    notificationlist.clear()
    notificationDisplaysList.clear()
    for n in d['notifications']:
        ne = NotificationEdit(notificationDestroyCallback)
        ne.lineEdit.setText(n)
        notificationDisplaysList.append(ne)
        notificationlist.createNewNotification(n, ne)
        print(f"notificationlist: {notificationlist._internalRep}")
    #updateBedtimeDisplay()
        
        
app = QApplication([])
m = MainWindow()
m.show()
print("loading data...")
loadDataFromFileAndUpdateGUI()
print(f"notificationlist: {notificationlist._internalRep}")
updateMasterLayout()
try:
    app.exec_()
except:
    print("closing")