from .__init__ import __versiondate__, __version__,  __versiondatetime__
from argparse import ArgumentParser, RawTextHelpFormatter
from configparser import ConfigParser
from datetime import datetime
from gettext import translation
from logging import info, ERROR, WARNING, INFO, DEBUG, CRITICAL, basicConfig, warning
from os import path
from importlib.resources import files
from signal import signal,  SIGINT
from socket import gethostname, create_connection
from subprocess import run
from sys import exit
from telegram import Update
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes
from time import sleep

try:
    t=translation('ssh_telegram_manager', files("ssh_telegram_manager") / 'locale')
    _=t.gettext
except:
    _=str
    
def signal_handler(signal_number, frame):
    """
    Handles the SIGINT signal (Ctrl+C) to gracefully exit the application.

    Args:
        signal_number (int): The signal number received.
        frame (frame): The current stack frame.
    """
    print(_("You pressed 'Ctrl+C', exiting..."))
    exit(0)

def argparse_epilog() -> str:
    """
    Generates the epilog string for the ArgumentParser, including copyright information.

    Returns:
        str: The epilog string.
    """
    return _("Developed by Mariano Muñoz 2022-{}").format(__versiondate__.year)

def addDebugSystem(level: str):
    """
    Configures the logging system based on the specified debug level.

    Args:
        level (str): The desired logging level (e.g., "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL").
                     Logs are written to /var/log/ssh_telegram_manager.log.
    """
    logFormat = "%(asctime)s.%(msecs)03d %(levelname)s %(message)s [%(module)s:%(lineno)d]"
    dateFormat='%F %I:%M:%S'
    logfile="/var/log/ssh_telegram_manager.log"

    if level=="DEBUG": # Show detailed information that can help with program diagnosis and troubleshooting.
        basicConfig(filename=logfile, level=DEBUG, format=logFormat, datefmt=dateFormat)
    elif level=="INFO": # Everything is running as expected without any problem.
        basicConfig(filename=logfile, level=INFO, format=logFormat, datefmt=dateFormat)
    elif level=="WARNING": # The program continues running, but something unexpected happened, which may lead to some problem down the road.
        basicConfig(filename=logfile, level=WARNING, format=logFormat, datefmt=dateFormat)
    elif level=="ERROR": # The program fails to perform a certain function due to a bug.
        basicConfig(filename=logfile, level=ERROR, format=logFormat, datefmt=dateFormat)
    elif level=="CRITICAL": # The program encounters a serious error and may stop running.
        basicConfig(filename=logfile, level=CRITICAL, format=logFormat, datefmt=dateFormat)
def main():
    """
    Main entry point for the SSH Telegram Manager application.
    Initializes the bot, handles command-line arguments, sets up logging,
    performs initial checks (datetime, internet connectivity), and starts
    the Telegram bot polling.
    """
    
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

    # Checks for current datetime set correctly due to it not crashes due to SSL telegram certificates
    while True:
        if datetime.now()<=__versiondatetime__:
            info(_("Current system datetime is wrong. I will try again after 10 seconds"))
            sleep(10)
        else:
            break

    # Checks for Internet connectivity before starting the bot.
    while True:
        try:
            create_connection(("www.google.com", 80))
            info(_("Internet detected"))
            break
        except OSError:
            warning(_("Internet wasn't detected. I will try again after 10 seconds"))
            sleep(10)
    
    # Starts the Telegram bot connection and polling.
    app = ApplicationBuilder().token(config["Telegram"]["Token"]).build()
    app.add_handler(CommandHandler('ssh_start',	start))
    app.add_handler(CommandHandler('ip', ip_command))
    app.run_polling()

    info(_("Stopping manager"))
        
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Telegram command handler for /ssh_start.
    Starts the SSH daemon, waits for a configured timeout, and then stops it.

    Args:
        update (Update): The incoming Telegram update.
        context (ContextTypes.DEFAULT_TYPE): The context object for the current update.
    """
    command=config["SSHD"]["command_start"]
    run(command,  shell=True)
    message=_("{0}: sshd daemon was launched with command '{1}'.").format(get_hostname(), command)
    info(message)
    await context.bot.send_message(update.message.chat_id, message)
    
    timeout = int(config["SSHD"].get("timeout", 60)) # Get timeout from config, default to 60 seconds
    sleep(timeout)

    command=config["SSHD"]["command_stop"]
    run(command,  shell=True)
    message=_("{0}: sshd daemon was closed automatically with command '{1}'.").format(get_hostname(), command)
    info(message)
    await context.bot.send_message(update.message.chat_id, message)

async def ip_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the external IP address of the server."""
    info(_("Received /ip command."))
    try:
        # Use curl to get the external IP address. -s makes it silent.
        result = run(["curl", "-s", "ifconfig.me"], capture_output=True, text=True, check=True)
        external_ip = result.stdout.strip()
        
        if external_ip:
            message = _("{0}: External IP address is: {1}").format(get_hostname(), external_ip)
            info(message)
            await context.bot.send_message(update.message.chat_id, message)
        else:
            error_message = _("{0}: Could not retrieve external IP address.").format(get_hostname())
            warning(error_message)
            await context.bot.send_message(update.message.chat_id, error_message)
    except Exception as e:
        error_message = _("{0}: Error retrieving external IP address: {1}").format(get_hostname(), str(e))
        warning(error_message)
        await context.bot.send_message(update.message.chat_id, error_message)

def get_hostname() -> str:
    """
    Retrieves the hostname of the current machine.

    Returns:
        str: The hostname.
    """
    return gethostname()
