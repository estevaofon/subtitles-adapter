#!/usr/bin/python

import datetime
class TimeOperations:
    def createTime(self,h,m,s):
        return datetime.datetime(100,1,1,h,m,s).time()

    def addSecs(self,tm, secs):
        fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
        fulldate = fulldate + datetime.timedelta(seconds=secs)
        return fulldate.time()

    def subSecs(self,tm, secs):
        fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
        fulldate = fulldate - datetime.timedelta(seconds=secs)
        return fulldate.time()

