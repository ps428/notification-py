# notification-py
`notification-py` is a Python package that provides a simple and convenient way to send notifications to Discord, Slack, and Email. You can send notification to either of these using a single command.

- Total Downloads: [![Downloads](https://static.pepy.tech/badge/notification-py)](https://pepy.tech/project/notification-py)
- Monthly Downloads: [![Downloads](https://static.pepy.tech/badge/notification-py/month)](https://pepy.tech/project/notification-py)


## Motivation
Lately I noticed several critical errors poping up in my python backend, I thought of a simple way to get notified about these failues (be it Stripe webhooks or anything else). So I came up with this idea to create a simple notification package which can be imported and used when unexpected errors are thrown by code.

> Using this package, developers can receive notifications through various combinations of Discord, Slack, and Email. The package supports sending notifications to all three platforms simultaneously, any two of them, or just one platform, depending on the provided credentials and configuration. This flexibility allows developers to customize their notification setup based on their specific requirements and preferences.



## How to install?
To install `notification-py` using pip:

```
pip install notification-py
```


## Usage

### 1. Importing types
To use notification-py in your Python project, you can import the `send_notification` function from the package. :

```
from notification_py.custom_types import (
    DiscordCreds,
    Message,
    Creds,
    EmailCreds,
    MessageDetails,
    SlackCreds,
)       
```

### 2. Creating Message Object:
`Message` object is core to the functionality of the `notification-py` package.
```
message = Message(
    message_details=MessageDetails(
        title="Test Title",
        text="Test Text",
        severity=2,
        source="Test Source",
        filename="Test Filename",
        line_number=0,
        time=datetime.now(),
    ),
    creds=Creds(
        discord=DiscordCreds(
            token="your_discord_bot_token",
            channel_id=your_discord_channel_id,
            team_id=your_discord_team_id,
        ),
        slack=SlackCreds(webhook_url="your_slack_webhook_url"),
        email=EmailCreds(
            email="your_email",
            password="your_email_password",
            smtp_server="your_smtp_server",
            smtp_port=your_smtp_port,
            target_email="target_email",
        ),
    ),
)
```

The Message object consists of two main parts:

1. `message_details`: An instance of `MessageDetails` that contains the details of the notification message, such as the title, text, severity, source, filename, line number, and timestamp.
2. `creds`: An instance of `Creds` that holds the credentials for Discord, Slack, and email notifications.

> These creds are independent of each other and one can just send Discord notifications using this message object (same applies for other combinations of these):
```
message = Message(
    message_details=MessageDetails(
        title="Test Title",
        text="Test Text",
        severity=2,
        source="Test Source",
        filename="Test Filename",
        line_number=0,
        time=datetime.now(),
    ),
    creds=Creds(
        discord=DiscordCreds(
            token="your_discord_bot_token",
            channel_id=your_discord_channel_id,
            team_id=your_discord_team_id,
        ),
        slack=None,
        email=None,
    ),
)

```

### 3. Sending notification:
You can just call this async function `notify` to send notification to all the services at a go. 
```
from notification_py.main import send_notification

async def notify(message):
    await send_notification(message)

```
> Please note that only those services which have valid creds will be notified.

## Creating Credentials
To send notifications to Discord, Slack, and email, you need to provide the necessary credentials. Here's how you can create the credential objects:

### 1. Discord:
1. You can obtain your Discord bot token by simply following this [tutorial](https://www.freecodecamp.org/news/create-a-discord-bot-with-javascript-nodejs/). 
2. Once you have the token and the bot is installed on your Discord server, just get your channel id and id of the [role](https://support.discord.com/hc/en-us/articles/214836687-Role-Management-101) that you want to notify for the notification.

### 2. Slack:
1. Just go to [apps](https://api.slack.com/apps) and create a new app for your workspace.
2. Once app is created, select the channel to enable the webhooks on this [url](https://api.slack.com/apps/A06S2HTV53L/incoming-webhooks)
3. Copy that webhooks url and it's gtg.

### 3. Email (for gmail):
1. Make sure you have 2FA enabled.
2. Just follow along [this discussion](https://support.google.com/accounts/answer/185833?hl=en) to get your `app password` 
3. Once that is done, save the generated password and create email creds like this:
```
email = "YOUR_ID@gmail.com"
password = "GENERATED_APP_PASSWORD"
smtp_server = "smtp.gmail.com"
smtp_port = "587"
target_email = "RECIPIENT_ID@gmail.com"

```

## Sample notifications
### 1. Discord
![Sample Discord Notifications](https://github.com/ps428/notification-py/blob/main/screenshots/discord.png)
### 2. Slack
![Sample Slack Notifications](https://github.com/ps428/notification-py/blob/main/screenshots/slack.png)
### 3. Email
![Sample Email Notifications](https://github.com/ps428/notification-py/blob/main/screenshots/email.png)


# Contact me

To raise any **issues/requests** you may refer the issue page [here](https://github.com/ps428/notification-py/issues).

You may **mail me** here on my [mail id](mailto:pranav.bhawan@gmail.com).

Feel free to **connect with me** on [my LinkedIn](https://www.linkedin.com/in/ps428).

Please do check out my other projects on my **GitHub** [here](http://www.github.com/ps428).

Also I have made many cool Firefox Add ons. They are pretty useful, you may want to check them out [here](https://addons.mozilla.org/en-US/firefox/user/17277929/).

If you like my work, you may want to [buy me a book here](https://www.buymeacoffee.com/ps428).

