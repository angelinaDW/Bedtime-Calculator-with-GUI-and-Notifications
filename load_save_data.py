FILE_NAME = "settings.txt"
from utils import *
from datetimeUtils import *


def saveData(data: dict):
    print("In savedata")
    print(f"data['notifications']): {data['notifications']}")
    f = open("settings.txt", 'w')
    keys = list(data.keys())
    lines = []
    if 'wakeupTime' in keys:
        lines.append("wakeupTime=" + AMPMToTwentyFourHour(data['wakeupTime']))
    if 'hoursOfSleep' in keys:
        lines.append("hoursOfSleep=" + data['hoursOfSleep'])
    if 'notifications' in keys:
        lines.append("notifications="  + "[" + ",".join(data['notifications'])+ "]")
    lines = [l + "\n" for l in lines]
    print(lines)
    f.writelines(lines)
    print("Settings saved!")

def loadData() -> dict:
    try:
        lines = open(FILE_NAME, "r").readlines()
        resultsDict = {}
        # Note: we have deleted all whitespaces to make it easiser to parse
        # I don't think this will affect newlines, but maybe not
        
        for line in lines:
            line = line.replace(" ", "")
            line = line.rstrip('\n')
            if "wakeupTime" in line:
                timeStr = line[11:]
                resultsDict['wakeupTime'] = timeStr
            elif "hoursOfSleep" in line:
                resultsDict['hoursOfSleep'] = line[13:]
            elif "notifications" in line:

                items : list[str] = line[15: len(line) - 1].split(",")
                resultsDict['notifications'] = items
        return resultsDict
        
    except Exception as e:
        print(e)
        

if __name__ == "__main__":
    #saveData({"wakeupTime" : "9:00:00", "hoursOfSleep" : "5", "notifications":['1','1']})
    print(loadData())