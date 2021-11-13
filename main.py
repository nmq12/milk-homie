# Environment Variables
from dotenv import dotenv_values
config = dotenv_values(".env")
NICKNAME=config["NICKNAME"]
TOKEN=config["TOKEN"]

# Communication with Twitch
import re
import socket
from collections import defaultdict
from emoji import demojize, emojize

# The brains
import brain

# Channels to connect to
CHANNELS = ['mick_dilk', 'itswill', 'thanksderm', 'zohi_rs', 'jiksee']
NO_STATIC_RESPONSE = ['itswill']
INTERACT = True

# Bot static responses
STATIC_RESPONSES = [
    ["itswill7", "itswill7"],
    ["PING", "PONG"],
    ["mickdiW", "mickdiW"],
    ["MusicMakeYouLoseControl", "MilkMakesYouLoseControl"],
    ["x0r6ztGiggle", "x0r6ztGiggle"],
    ["HONESTLYSOTRUE", "HONESTLYSOTRUE"],
    ["MonikaBoom", "MonikaBoom"],
    ["Kissahomie", "Kissahomie"]
]

# Global Vars
SERVER='irc.chat.twitch.tv'
PORT=6667
sock = socket.socket()
threads = []
bot = brain.ChatterBot()
data = defaultdict(list)

# Chat text strippers
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
CHAT_AT = re.compile(r"@\w+")
CHAT_LINK = re.compile(r'http\S+')


def main():
    global sock
    try:
        sock.connect((SERVER, PORT))
        sock.send(f"PASS {TOKEN}\r\n".encode('utf-8'))
        sock.send(f"NICK {NICKNAME}\r\n".encode('utf-8'))
        for channel in CHANNELS:
            sock.send(f"JOIN #{channel}\r\n".encode('utf-8'))
        connected = True
    except Exception as e:
        print(str(e))
        connected = False

    while connected:
        resp = sock.recv(2048).decode('utf-8')
        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))
        elif len(resp) > 0 and not resp.lower().startswith(
                (':tmi.twitch.tv', ':milk_homie', ':nightbot', ':streamlabs', ':streamelements', ':soundalerts')
        ):
            print(resp)
            username = re.search(r"\w+", resp).group(0)
            channel = re.search(r"#\w+", resp).group(0)
            message = demojize(CHAT_MSG.sub("", resp))

            if username:
                parsed_message = CHAT_LINK.sub("", CHAT_AT.sub("", message)).strip()

                if INTERACT:
                    if message.startswith(f"@{NICKNAME}"):
                        send_message(sock, channel, f"@{username} {response(parsed_message)}")

                    if channel[1:] not in NO_STATIC_RESPONSE:
                        for static_response in STATIC_RESPONSES:
                            if message.startswith(static_response[0]):
                                send_message(sock, channel, static_response[1])

					# if len(parsed_message) > 0 and not parsed_message.startswith('!'):
					# 	print(f"Username: {username}\nChannel: {channel}\nMessage: {parsed_message}\n")
					# 	data[channel].append(parsed_message)
					# 	if len(data[channel]) >= 25:
					# 		bot.train(data[channel])
					# 		data[channel].clear()

def send_message(sock, channel, msg):
    print('sending message: ', msg, '\n')
    sock.send(f"PRIVMSG {channel} :{emojize(msg)}\r\n".encode('utf-8'))


def response(msg):
    bot_response = bot.get_response(msg)
    return bot_response


if __name__ == "__main__":
    main()
