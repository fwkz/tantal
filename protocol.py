from autobahn.twisted.websocket import WebSocketServerProtocol
import navigator


class MyServerProtocol(WebSocketServerProtocol):

    def __init__(self):
        self.keyID = None
    
    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        self.keyID = payload

        if isBinary:
            print("Binary message received: {0} bytes".format(len(self.keyID)))
        else:
            print("Text message received: {0}".format(self.keyID.decode('utf8')))

        if not self.is_key_valid():
            self.keyID = "Invalid Key!"

        self.steering_wheel()

        ## echo back message verbatim
        self.sendMessage(self.keyID, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

    def is_key_valid(self):
        valid_keys = ["left", "up", "right", "down", "37", "38", "39", "40", "0"]
        if self.keyID in valid_keys:
            return True
        else:
            return False
    
    def steering_wheel(self):
        if self.keyID in ["left", "37"]:
            navigator.left()
        elif self.keyID in ["up", "38"]:
            navigator.forward()
        elif self.keyID in ["right", "39"]:
            navigator.right()
        elif self.keyID in ["down", "40"]:
            navigator.backward()
        elif self.keyID in ["0"]:
            navigator.stop()