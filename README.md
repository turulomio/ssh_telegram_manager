# SSH Telegram Manager
SSH Telegram Manager is a Telegram bot to launch ssh on demand. With this tool, you can avoid to expose your ssh port permanently on Internet.

![Screenshot of a working SSH Telegram Manager bot](https://github.com/turulomio/ssh_telegram_manager/blob/main/doc/telegram_bot.png)

## Installation
### Gentoo

If you use Gentoo, you can find the ebuild in https://github.com/turulomio/myportage/tree/master/app-admin/ssh_telegram_manager

- Get your Telegram Bot token. This is a way to get it https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token
- Copy `/etc/ssh_telegram_manager/ssh_telegram_manager.default` to your `/etc/ssh_telegram_manager/ssh_telegram_manager` and edit your settings.
- Just run `ssh_telegram_manager`. You can use `/etc/init.d/ssh_telegram_manager` to launch daemon or `rc-update add ssh_telegram_manager` to launch it on server start up
- When ssh_telegram_manager is working fine, disable sshd daemon from start with `rc-update del sshd` to hide your ssh port on Internet
- You must use \ssh_start to launch ssh on your Telegram Bot. After 1 minute(you can change in settings) it will be closed.


### Debian

If you use Debian, you can use pip `pip install ssh_telegram_manager`

- Get your Telegram Bot token. This is a way to get it https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token
- Copy https://github.com/turulomio/ssh_telegram_manager/blob/main/etc/ssh_telegram_manager/ssh_telegram_manager.default to your /etc/ssh_telegram_manager/ssh_telegram_manager
- Edit this file to set `systemctl start ssh` and `systemctl stop ssh` as your start and stop command
- Copy https://github.com/turulomio/ssh_telegram_manager/blob/main/etc/systemd/debian/ssh_telegram_manager.service to your /lib/systemd/system/ directory
- Just run ssh_telegram_manager. You can launch daemon with `systemctl start ssh_telegram_manager`. You can launch it on server start with `systemctl enable ssh_telegram_manager`
- When ssh_telegram_manager is working fine, disable ssh daemon from start with `systemctl disable ssh` to hide your ssh port on Internet
- You must use \ssh_start to launch ssh on your Telegram Bot. After 1 minute(you can change in settings) it will be closed.


## Changelog

### 0.5.0
- Upgraded code to python-telegram-bot-20.0 api

### 0.4.0 (2022-10-22)
- Fixed bug when system time is not set correctly
- Added `ssh_telegram_manager.service` for systemd systems
- Improved spanish translation

### 0.3.0 (2022-08-17)
- Now waits for Internet before connecting to Telegram to avoid errors

### 0.1.1 (2022-08-13)
- Basic functionality
