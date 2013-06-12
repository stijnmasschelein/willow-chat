from willow.willow import*
import os

def session (me):
    nameInput = "newMessage"
    nameOutput = "conversationArea"
    myConversationsDicts = []

    add(open("chat.html"))

    # Make a conversation unless it already exists.
    clients = [me]
    if me % 2:
        clients.append(me - 1)
    else:
        clients.append(me + 1)

    fullList = conversation.List
    myConversations = [C for C in fullList if set(clients) == set(C.clients)]

    if len(myConversations) == 0:
        newConversation = conversation(clients)
    else:
        newConversation = myConversations[0]
    newInput = textArea(nameInput, me)
    newOutput = textArea(nameOutput, me)
    newConversation.addOutput(newOutput)
    myConversationsDicts.append({"conversation":newConversation,
    "input":newInput, "output":newOutput})

    # everything is ready now for the chat to start.
    while True:
        take({"tag":"click", "id": "submitMessage", "client":me})
        newMessage = {"client":me, "text":newInput.read()}
        if newMessage["text"] != "":
            newConversation.updateConversation(newMessage)
            newInput.update("")

### Every client can in principle get access to these objects. The advantage is
### that the data is more or less kept in the python program not on the board.
### The disadvantage is that it might screw with the coordination. Maybe store
### the pure text somewhere on the board.

class textArea (object):

    def __init__(self, name, client):
        self.client = client
        self.name = name

    ### Functions to handle the text area
    def read(self):
        self.text = peek("#"+self.name, self.client)
        return self.text

    def update(self, newText):
        poke("value", newText, "#"+self.name, self.client)

class conversation (object):

    Id = 0
    List = []

    # These functions are only for instances
    def __init__(self, allClients):
        conversation.Id += 1
        self.id = conversation.Id
        self.clients = allClients
        self.outputList = []
        put({"id":self.id, "conversation":""})
        conversation.List.append(self)

    def addOutput(self, area):
        self.outputList.append(area)

    def updateConversation(self, newMessage):
        msg = take({"id":self.id})
        self.current = msg["conversation"]
        self.current += str(newMessage["client"]) + ":" + "\t" + newMessage["text"]
        self.current += "\n"

        ### Update the textareas for all the relevant clients
        for textArea in self.outputList:
            textArea.update(self.current)

        ### Make the conversation available for changes and updates
        put({"id":self.id, "conversation":self.current})

run(session)
