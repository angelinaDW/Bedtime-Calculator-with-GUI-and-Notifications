import time
import datetime
import re
import enum
from datetimeUtils import*

def calculateBedtime(wakeuptime:datetime.datetime, hoursOfSleep: int) -> datetime.datetime:
    assert type(wakeuptime) == datetime.datetime
    return wakeuptime - datetime.timedelta(hours=hoursOfSleep)

def getBedtime(wakeUpTime: datetime.time, hoursOfSleep: int) -> str:
    print(f"wakeUpTime:  {wakeUpTime}")
    # Sets bedtime
    bedtime = timePlusTimeDelta(wakeUpTime, datetime.timedelta(hours=-int(hoursOfSleep)))
    return get24HourTimeAsAMPM(str(bedtime))

def timePlusTimeDelta(time : datetime.time, tDelta : datetime.timedelta) -> datetime.time:
    return (datetime.datetime.combine(datetime.datetime.now().date(),time) + tDelta).time()


def timeStrToDateTime(time: str) -> datetime.datetime:
    today: datetime = datetime.datetime.now()
    tommorow: datetime = datetime.datetime(today.year, today.month, today.day + 1)
    
    def dateTimeFromTimeStr(dayInfo:datetime.datetime, timeStr: str) -> datetime.datetime:
        timeObj : datetime.time = datetime.datetime.strptime(timeStr, '%H:%M:%S').time()
        return datetime.datetime( dayInfo.year, dayInfo.month, dayInfo.day, timeObj.hour, timeObj.minute, timeObj.second)

    dt1 = dateTimeFromTimeStr(today, time)
    dt2 = dateTimeFromTimeStr(tommorow, time)

    
    # Return whichever version is the closest to now, and isn't negative
    now = datetime.datetime.now()
    diff1 : float = (dt1 - now).total_seconds()
    diff2 : float = (dt2 - now).total_seconds()
    if diff1 < 0 and diff2 < 0:
        raise Exception("Something has gone very wrong!!!")
    elif diff1 < 0:
        return dt2
    else: # Both are positive
        # Return whichever is sooner
        if diff1 < diff2:
            return dt1
        else:
            return dt2

def get24HourTimeAsAMPM(_24hr : str):
    '''
    Takes in a 24 hour time in the format (hr):(min)[:(sec)] and returns it as (hr):(min)[:(sec)] AM or PM
    '''
    ampm : str = None
    if _24hr[1] == ":":
        _24hr = "0" + _24hr
    
    h: int = int(_24hr[0:2])
    assert h >= 0 and h < 24
    ampm = "AM" if h >= 0 and h <= 11 else "PM"
    
    if ampm == "AM":
        if h == 0:
            h = 12
    else:
        if h != 12:
            h = h - 12
    return str(h) + _24hr[2:] + ampm

def getAMPMAs24Hr(ampm : str):
    raise NotImplementedError()