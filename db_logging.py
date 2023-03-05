import dbwork
import os
class dblogger:
    def __init__(self, appName, connection):
        self.appName = appName
        self.connection = connection

    def LogInfo(self, message):
        self.__AddLog(message, "Info")

    def LogError(self, message):
        self.__AddLog(message, "Error")

    def LogDebug(self, message):
        self.__AddLog(message, "Debug")


    def __AddLog(self, message, type):
        appName = self.appName
        newLog = {}
        if type == "Info":
            newLog = {
                'application_name': appName,
                'host':os.environ['COMPUTERNAME'],
                'level':"Info",
                'message':message
        }
        elif type == "Error":
            newLog = {
                'application_name': appName,
                'host': os.environ['COMPUTERNAME'],
                'level': "Error",
                'message': message
            }
        elif type == "Debug":
            newLog = {
                'application_name': appName,
                'host': os.environ['COMPUTERNAME'],
                'level': "Debug",
                'message': message
            }

        dbwork.newLog(conn=self.connection,
                      application_name=newLog['application_name'],
                      host=newLog['host'],
                      level=newLog['level'],
                      message=newLog['message'])