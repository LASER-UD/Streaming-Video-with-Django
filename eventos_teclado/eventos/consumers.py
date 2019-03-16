import json
import logging
from channels import Channel, Group
from channels.sessions import channel_session

def ws_add(message):
    message.reply_channel.send({"accept": True})
    Group("platzi_piton").add(message.reply_channel)


def ws_message(message):
    try:
        data = json.loads(message['text'])
    except ValueError:
        logging.debug("el formato no parece json=%s", message['text'])
        return
    if data:
        reply_channel = message.reply_channel.name
    return False

def ws_disconnect(message):
    Group("platzi_piton").discard(message.reply_channel)
