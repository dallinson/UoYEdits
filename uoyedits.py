import json
from sseclient import SSEClient as EventSource
import socket
import irc
import configparser
import os


def valid_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except BaseException:
        return False


def is_uoy_ip(address):
    return valid_ip(address) and (address[0:7] == "144.32.")

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config_file.conf")

config = configparser.ConfigParser()
config.read(config_path)



irc_config = config["irc_config"]
irc_client = irc.IRCClient(irc_config["server"], '#' + irc_config["channel"], irc_config["nickname"])
url = 'https://stream.wikimedia.org/v2/stream/recentchange'
for event in EventSource(url):
    if event.event == 'message':
        try:
            change = json.loads(event.data)
        except ValueError:
            pass
        else:
            if change['wiki'] == 'enwiki' and is_uoy_ip(change['user']):
                print('{user} edited {title}'.format(**change))
                irc_client.send_msg(
                    '#' + irc_config["channel"],
                    "{title} Wikipedia article edited anonymously from the University of York".format(
                        **change))
