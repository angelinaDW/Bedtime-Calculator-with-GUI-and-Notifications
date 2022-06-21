from turtle import ondrag
from qtpy.QtWidgets import *
from plyer import notification
import time
from datetimeUtils import secondsFromNowUntilDT
import datetime
import threading

# Class for actually storing notification data
# Actually, instead of having a unique ID to bind each notification to each notificationEdit, why not just bind based on the number of minutes before?
# It would not ever make sense to have more than one notification go off at the same time
# Should we allow the user to have negative amounts of minutesBefore?

class NotificationsList():

    def __init__(self):
        self._internalRep = {} # Key = minutesBefore, value=notificationEdit
        self._stop : threading.Event = threading.Event()
    def clear(self):
        self._internalRep.clear()
        
    def getCurrentTimeAsStr() -> str:
        now = datetime.now()
        return now.strftime("%H:%M:%S")
    
    def secondsBetween(time1: str, time2: str) -> int:
        # Returns an int representing the time, in seconds, between two 24-hour times
        print(f"Time1: {time1} time2: {time2}")
        hourDif = abs(int(time2[0:2]) -  int(time1[0:2]))
        minDif = abs(int(time2[3:5]) - int(time1[3:5])) 
        secDif = abs(int(time2[6:]) - int(time1[6:])) 
        
        return hourDif*60*60 + minDif*60 + secDif
    
    def waitUntilNextNotification(self, bedtime: datetime.datetime):
        secondsToWait = -1
        i = 0
        self._stop.clear()
        while i < len(list(self._internalRep.keys())):
            nextNotification : int = int(list(self._internalRep.keys())[i])
            secondsToWait = (bedtime - datetime.datetime.now()).total_seconds() - 60*(nextNotification)
            if secondsToWait >= 0:
                break
            else:
                i += 1
        if i >= len(list(self._internalRep.keys())):
            # If there were no future notifications to show...
            print("All notification times have expired")
            return
        print("Operation successful!")
        print("Waiting {} seconds".format(secondsToWait))
        self._stop.wait(secondsToWait)
        if (self._stop.isSet()):
            return
        #time.sleep(secondsToWait)
        print("Alarm going off")
        notification.notify( title="It's almost time for bed!", app_name = "Bedtime Notifier", message="Time to go to bed in {} minutes".format(list(self._internalRep.keys())[0]), app_icon= r"icon.ico")

    def createNewNotification(self, minutesBefore, notificationEdit):
        self._internalRep[minutesBefore] = notificationEdit

    def destroy(self, minutesBefore: int):
        # Attempts to destroy the notification set to go off x minutes before
        try:
            del self._internalRep[minutesBefore]
        except:
            print("There wasn't a minutesbefore associated with this")

    def sort(self):
        self._internalRep = dict(sorted(self._internalRep.items()))

class NotificationEdit(QWidget):

    def __init__(self, notificationDestroyCallback):
        '''
        LABEL TEXTEDIT LABEL

        Features
        - input validation for minBefore(should an integer)
        '''
        super(NotificationEdit, self).__init__()
        layout = QHBoxLayout()

        self.leftLabel = QLabel("Notification ")
        self.lineEdit = QLineEdit()
        self.rightLabel = QLabel(" minutes before")
        self.deleteButton = QPushButton("X")
        def onDestroy():
            notificationDestroyCallback(self)
        self.deleteButton.clicked.connect(onDestroy)
        

        layout.addWidgets(self.leftLabel, self.lineEdit, self.rightLabel, self.deleteButton)

        # Finally, update the layout
        self.setLayout(layout)
    
    def minutesBefore(self) -> str:
        return self.lineEdit.text()

if __name__ == "__main__":
    notification.notify( title="It's almost time for bed!", app_name = "Bedtime Notifier", message="Time to go to bed in  minutes", app_icon= r"icon.ico")
