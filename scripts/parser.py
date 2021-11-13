import json
import random
import re

data = json.load(open('db.json', 'r', encoding='utf-8'))
writer = open('../data/input.txt', 'w', encoding='utf-8')


# TEXT STRIPPERS #
def stripper(text):
    # Don't include usernames or timestamps
    strip_tmi_link = re.compile(r':\w+!\w+.tmi.twitch.tv PRIVMSG #\w+ :')
    # Removes the majority of sub emotes (which the bot can't use)
    strip_camel_emotes = re.compile(r'(\s[a-z]+[A-Z\d]+[a-z\d]*)|[\W\D]([a-z]+[A-Z\d]+[a-z\d]*\s)')
    # Remove links to prevent the bot from inadvertently advertising
    strip_links = re.compile(r'^.*((http)s?|www\.\w+\.(com|org|net|ca|me|co)|[\d\w]+\.(com|org|net|ca|me|co)).*$',
                             flags=re.MULTILINE | re.IGNORECASE)
    # Attempts to remove common bot messages
    strip_sub_notifs = re.compile(r'^.*(subscribed\s(at|to|for|with)|has\sbeen\slive\sfor|subscribed\sfor\d+)\s.*$',
                                  flags=re.MULTILINE | re.IGNORECASE)
    # Attempts to remove all invalid characters
    strip_invalid = re.compile(r'')
    # Strip out bots first
    text = strip_tmi_link.sub('', text)
    text = strip_camel_emotes.sub('', text)
    text = strip_links.sub('', text)
    text = strip_sub_notifs.sub('', text)

    return text


def is_ascii(s):
    return len(s) == len(s.encode())


for d in data:
    stripped_text = stripper(d['text'])
    if not is_ascii(stripped_text):
        print(stripped_text)
        print("ASCII DETECTED")
    else:
        writer.write(stripped_text + '\n')

print('Data imported from db.json to input.txt')