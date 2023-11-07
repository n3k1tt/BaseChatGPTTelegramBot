import datetime

class AllUsers():
    def __init__(self):
        self.Users={}
        self.cooldown=25
    def addUser(self,id):
        self.Users[id]={"lastMessage": datetime.datetime.now().timestamp()-self.cooldown,"context": []}
    def getContext(self,id,Umessage):
        self.Users[id]['context'].append({"role":"user", "content": Umessage})
        return self.Users[id]['context']
    def addToContext(self,id,Smessage):
        self.Users[id]['context'].append({"role": "assistant", "content": Smessage})
        return self.Users[id]['context']
    def userExist(self,id):
        return id in self.Users
    def mayMessage(self,id):
        return self.Users[id]["lastMessage"]+self.cooldown-datetime.datetime.now().timestamp()<0
