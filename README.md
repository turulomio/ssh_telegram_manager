# ssh_telegram_manager
Telegram bot to launch ssh on demand. You can avoid to expose your ssh port constantly on Internet.

## Installation
### Gentoo

If you use Gentoo, you can find the ebuild in https://github.com/turulomio/myportage/tree/master/app-admin/ssh_telegram_manager

- Copy `/etc/ssh_telegram_manager/ssh_telegram_manager.default` to your `/etc/ssh_telegram_manager/ssh_telegram_manager`
- Get your Telegram Bot token. This is a way to get it https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token
- Just run `ssh_telegram_manager`. You can use `/etc/init.d/ssh_telegram_manager` to launch daemon or `rc-update add ssh_telegram_manager` to launch it on server start up`
- When ssh_telegram_manager is working fine, disable sshd daemon from start with `rc-update del sshd` to hide your ssh port on Internet
- If your hostname is mypc, You must use \mypc_start to launch ssh on your Telegram Bot. After 1 minute(you can change in settings) it will be closed.


### Debian

If you use Debian, you can use pip `pip install ssh_telegram_manager`

- Copy https://github.com/turulomio/ssh_telegram_manager/blob/main/etc/ssh_telegram_manager/ssh_telegram_manager.default to your /etc/ssh_telegram_manager/ssh_telegram_manager
- Edit this file to set `systemctl start ssh` and `systemctl stop ssh` as your start and stop command
- Get your Telegram Bot token. This is a way to get it https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token
- Copy https://github.com/turulomio/ssh_telegram_manager/blob/main/etc/systemd/debian/ssh_telegram_manager.service to your /lib/systemd/system/ directory

- Just run ssh_telegram_manager. You can launch daemon with `systemctl start ssh_telegram_manager`. You can launch it on server start with `systemctl enable ssh_telegram_manager`
- When ssh_telegram_manager is working fine, disable ssh daemon from start with `systemctl disable ssh` to hide your ssh port on Internet
- If your hostname is mypc, You must use \mypc_start to launch ssh on your Telegram Bot. After 1 minute(you can change in settings) it will be closed.


## Changelog

### 0.3.0 (2022-08-17)
- Now waits for Internet before connecting to Telegram to avoid errors

### 0.1.1 (2022-08-13)
- Basic functionality
