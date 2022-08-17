# ssh_telegram_manager
Telegram bot to launch ssh on demand

## Installation
If you use Gentoo, you can find the ebuild in https://github.com/turulomio/myportage/tree/master/app-admin/ssh_telegram_manager

If you use other Linux distribution, you can use pip
`pip install ssh_telegram_manager`

## Configuration
- Copy https://github.com/turulomio/ssh_telegram_manager/blob/main/etc/ssh_telegram_manager/ssh_telegram_manager.default to your /etc/ssh_telegram_manager/ssh_telegram_manager
- If you use systemd you must set `systemctl start sshd` and `systemctl stop sshd` as your start and stop command
- Get your Telegram Bot token. This is a way to get it https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token
- Just run ssh_telegram_manager
- If your hostname is mypc, You must use \mypc_start to launch ssh. After 1 minute(you can change in settings) it will be closed.

## Changelog

### 0.3.0 (2022-08-17)
- Now waits for Internet before connecting to Telegram to avoid errors

### 0.1.1 (2022-08-13)
- Basic functionality