#!/usr/bin/python

import atexit
import ConfigParser
import signal
import sys
import time

import pyupm_biss0001 as upmMotion
import pyupm_grove as grove
import pyupm_grovespeaker as upmGrovespeaker
import pyupm_i2clcd as lcd

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from wit import Wit

from core.xcamera import takePhoto
from core.xfacerecognition import recognizeFaces
from core.xspeechrecognition import recognizeSpeech
from core.xsay import isay
from core.xvoice import recordAudio
from core.xvoice import playAudio
from core.xwolfram import askWolfram

credentials = ConfigParser.ConfigParser()
credentialsfile = "core/configuration/credentials.config"
credentials.read(credentialsfile)
display = lcd.Jhd1313m1(0, 0x3E, 0x62)
motion = upmMotion.BISS0001(3)
speaker = upmGrovespeaker.GroveSpeaker(6)

def functionMotion(bot, update):
    if (motion.value()):
        moving = "Yes!"
        speaker.playSound('c', True, "med")
    else:
        moving = "No"
    bot.sendMessage(update.message.chat_id, text='Object Moiving? ' + str(luxes))

def functionEcho(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)

def SIGINTHandler(signum, frame):
	raise SystemExit

def exitHandler():
	print "Exiting"
	sys.exit(0)

atexit.register(exitHandler)
signal.signal(signal.SIGINT, SIGINTHandler)

def say(session_id, context, msg):
    print(msg)

def merge(session_id, context, entities, msg):
    return context

def error(session_id, context, e):
    print(str(e))

def witaiMotion(session_id, context):
    luxes = light.value()
    message = "Light value is " + str(luxes)
    isay("english", message)    
    context['forecast'] = 'sunny'
    return context

actions = {
    'say': say,
    'merge': merge,
    'error': error,
    'witaiMotion': witaiMotion,
}

if __name__ == '__main__':

    credential = credentials.get("telegram", "token")
    updater = Updater(credential)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("motion", functionMotion))
    dp.add_handler(MessageHandler([Filters.text], functionEcho))

    updater.start_polling()

    credential = credentials.get("witai", "ServerAccessToken")
    client = Wit(credential, actions)

    session_id = 'my-user-id-42'

    while True:

        if (motion.value()):

            # isay("english", "Hi! This is DhIs! How can I help?")

            display.clear()
            display.setCursor(0,0)
            display.setColor(255, 0, 0)
            # speaker.playSound('c', True, "med")
            display.write("Stop Immediatily! And Smile!")

        else:

            display.clear()
            display.setCursor(0,0)
            display.setColor(0, 0, 0)
            moving = "No"
            display.write("Peace and Calm!")

            # client.run_actions(session_id, message, {})

    #updater.idle()
