# SSH Telegram Manager
SSH Telegram Manager is a Telegram bot designed to launch your SSH daemon on demand. This tool allows you to keep your SSH port closed by default, enhancing security by only exposing it when you explicitly request it via Telegram.

![Screenshot of a working SSH Telegram Manager bot](https://github.com/turulomio/ssh_telegram_manager/blob/main/doc/telegram_bot.png)

## Features
*   **On-demand SSH:** Start your SSH server only when needed via a Telegram command.
*   **Automatic Shutdown:** SSH server automatically closes after a configurable timeout.
*   **External IP Display:** Easily retrieve your server's external IP address via Telegram.
*   **Secure by Default:** Avoid permanent exposure of your SSH port to the internet.

## Installation

1.  **Install the package:**
    ```bash
    pip install ssh_telegram_manager
    ```

2.  **Obtain a Telegram Bot Token:**
    Follow a guide like this one ( https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token ) to get your bot token: How to get Telegram Bot API Token

3.  **Configure the bot:**
    *   Create the configuration directory if it doesn't exist:
        ```bash
        sudo mkdir -p /etc/ssh_telegram_manager/
        ```
    *   Copy the default configuration file to the system-wide configuration path:
        ```bash
        sudo cp /path/to/your/cloned/repo/etc/ssh_telegram_manager/ssh_telegram_manager.default /etc/ssh_telegram_manager/ssh_telegram_manager
        ```
        (Replace `/path/to/your/cloned/repo/` with the actual path where you cloned the `ssh_telegram_manager` repository).
    *   Edit the copied configuration file (`/etc/ssh_telegram_manager/ssh_telegram_manager`) and replace `YOUR_TELEGRAM_BOT_TOKEN` with the token you obtained in step 2.

4.  **Run the bot:**
    ```bash
    ssh_telegram_manager
    ```
    For production environments, it's recommended to run this as a systemd service. A sample `ssh_telegram_manager.service` file is available in the `etc/` directory of the repository.

5.  **Enhance Security (Recommended):**
    Once the `ssh_telegram_manager` is working correctly, disable your SSH daemon from starting automatically at boot. This ensures your SSH port is not permanently exposed to the internet.
    ```bash
    sudo systemctl disable ssh
    ```

## Configuration

The main configuration file is located at `/etc/ssh_telegram_manager/ssh_telegram_manager`.
It uses INI format and contains the following sections:

```ini
[Telegram]
Token = YOUR_TELEGRAM_BOT_TOKEN

[SSHD]
command_start = systemctl start sshd
command_stop = systemctl stop sshd
timeout = 60
```

*   **`[Telegram]`**
    *   `Token`: Your Telegram Bot API token. This is mandatory for the bot to connect to Telegram.

*   **`[SSHD]`**
    *   `command_start`: The shell command executed to start your SSH daemon. Default is `systemctl start sshd`. Adjust if your system uses a different command (e.g., `service ssh start`).
    *   `command_stop`: The shell command executed to stop your SSH daemon. Default is `systemctl stop sshd`. Adjust if your system uses a different command.
    *   `timeout`: The number of seconds the SSH daemon will remain active after being started by the `/ssh_start` command. After this period, `command_stop` will be executed. Default is `60` seconds.

## Usage

Interact with your bot on Telegram using the following commands:

*   `/ssh_start`: Starts the SSH daemon on the server. It will automatically shut down after the configured `timeout` period. The bot will send a confirmation message with the server's hostname and the command executed.
*   `/ip`: Displays the external IP address of the server where the bot is running. This is useful if your server's IP changes or if you need to quickly share it.
