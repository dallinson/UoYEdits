import socket
import threading
import sys

class IRCClient:

    def __init__(self, server, channel, nickname):
        self._irc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._irc.connect((server,6667))
        print("connecting")
        self._irc.send(bytes("USER " + nickname + " 0 * " + nickname + "\n", "utf-8"))
        self._irc.send(bytes("NICK " + nickname + "\n","utf-8"))
        self._irc.send(bytes("JOIN " + channel + "\n", "utf-8"))
        receiver = message_receiver(self)
        receiver.start()

    def send_msg(self, channel, message):
        self._irc.send(bytes("PRIVMSG " + channel + " :" + message + "\n","utf-8"))


class message_receiver(threading.Thread):
    def __init__(self, irc):
        threading.Thread.__init__(self)
        self._irc = irc._irc

    def run(self):
        self.recv_messages()

    def recv_messages(self):
        while True:
            msg = self._irc.recv(2048)
            msg = msg.decode("utf-8")
            if msg.find("PING") != -1:
                self._irc.send(bytes("PONG " + msg.split()[1] + "\n", "utf-8"))