from .__init__ import __versiondate__, __version__,  __versiondatetime__
from argparse import ArgumentParser, RawTextHelpFormatter
from configparser import ConfigParser
from datetime import datetime
from gettext import translation
from logging import info, ERROR, WARNING, INFO, DEBUG, CRITICAL, basicConfig, warning
from os import path
from pkg_resources import resource_filename
from socket import gethostname, create_connection
from subprocess import run
from sys import exit

from signal import signal,  SIGINT
from time import sleep
from telegram import Update
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes

try:
    t=translation('ssh_telegram_manager', resource_filename("ssh_telegram_manager","locale"))
    _=t.gettext
except:
    _=str
    
def signal_handler( signal, frame):
        print(_("You pressed 'Ctrl+C', exiting..."))
        exit(0)

## Function used in argparse_epilog
## @return String
def argparse_epilog():
    return _("Developed by Mariano Muñoz 2022-{}").format(__versiondate__.year)

## Sets debug sustem, needs
## @param args It's the result of a argparse     args=parser.parse_args()        
def addDebugSystem(level):
    logFormat = "%(asctime)s.%(msecs)03d %(levelname)s %(message)s [%(module)s:%(lineno)d]"
    dateFormat='%F %I:%M:%S'
    logfile="/var/log/ssh_telegram_manager.log"

    if level=="DEBUG":#Show detailed information that can help with program diagnosis and troubleshooting. CODE MARKS
        basicConfig(filename=logfile, level=DEBUG, format=logFormat, datefmt=dateFormat)
    elif level=="INFO":#Everything is running as expected without any problem. TIME BENCHMARCKS
        basicConfig(filename=logfile, level=INFO, format=logFormat, datefmt=dateFormat)
    elif level=="WARNING":#The program continues running, but something unexpected happened, which may lead to some problem down the road. THINGS TO DO
        basicConfig(filename=logfile, level=WARNING, format=logFormat, datefmt=dateFormat)
    elif level=="ERROR":#The program fails to perform a certain function due to a bug.  SOMETHING BAD LOGIC
        basicConfig(filename=logfile, level=ERROR, format=logFormat, datefmt=dateFormat)
    elif level=="CRITICAL":#The program encounters a serious error and may stop running. ERRORS
        basicConfig(filename=logfile, level=CRITICAL, format=logFormat, datefmt=dateFormat)
    info("Debug level set to {}".format(level))


def main():
    
    signal(SIGINT, signal_handler)
    parser=ArgumentParser(description=_('Launches a Telegram bot to start sshd daemon on demand'), epilog=argparse_epilog(), formatter_class=RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--debug', help=_("Debug program information"), choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"], default="INFO")
    args=parser.parse_args()
    
    config_filename="/etc/ssh_telegram_manager/ssh_telegram_manager"
    addDebugSystem(args.debug)
        
    global config
    if not path.exists(config_filename):
        info(_("You must set and configure {0}").format(config_filename))
        info(_("You can find and rename '{0}.default' from source code").format(config_filename))
        return
    
    config = ConfigParser()
    config.read(config_filename)
    info(_("Starting manager"))

    ## Checks for current datetime set correctly due to it not crashes due to SSL telegram certificates
    while True:
        if datetime.now()<=__versiondatetime__:
            info(_("Current system datetime is wrong. I will try again after 10 seconds"))
            sleep(10)
        else:
            break

    ## Checks for Internet
    while True:
        try:
            create_connection(("www.google.com", 80))
            info(_("Internet detected"))
            break
        except OSError:
            warning(_("Internet wasn't detected. I will try again after 10 seconds"))
            sleep(10)
    
    ## Starts connection
    app = ApplicationBuilder().token(config["Telegram"]["Token"]).build()
    app.add_handler(CommandHandler('ssh_start',	start))
    app.run_polling()

    info(_("Stopping manager"))
        
async def start(update: Update, context=ContextTypes.DEFAULT_TYPE) -> None:
    command=config["SSHD"]["command_start"]
    run(command,  shell=True)
    message=_("{0}: sshd daemon was launched with command '{1}'.").format(get_hostname(), command)
    info(message)
    await context.bot.send_message(update.message.chat_id, message)
    sleep(60)

    command=config["SSHD"]["command_stop"]
    run(command,  shell=True)
    message=_("{0}: sshd daemon was closed automatically with command '{1}'.").format(get_hostname(), command)
    info(message)
    await context.bot.send_message(update.message.chat_id, message)


def get_hostname():
    return gethostname()

