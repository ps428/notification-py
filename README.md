# notification-py
`notification-py` is a Python package that provides a simple and convenient way to send notifications to Discord, Slack, MS Teams, and Email. You can send notification to either of these using a single command.

- Total Downloads: [![Downloads](https://static.pepy.tech/badge/notification-py)](https://pepy.tech/project/notification-py)
- Monthly Downloads: [![Downloads](https://static.pepy.tech/badge/notification-py/month)](https://pepy.tech/project/notification-py)


## Motivation
Lately I noticed several critical errors poping up in my python backend, I thought of a simple way to get notified about these failues (be it Stripe webhooks or anything else). So I came up with this idea to create a simple notification package which can be imported and used when unexpected errors are thrown by code.

> Using this package, developers can receive notifications through various combinations of Discord, Slack, MS Teams, and Email. The package supports sending notifications to all platforms simultaneously, any combination of them, or just one platform, depending on the provided credentials and configuration. This flexibility allows developers to customize their notification setup based on their specific requirements and preferences.



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
    TeamsCreds,
)       
```

### 2. Creating Message Object:
`Message` object is core to the functionality of the `notification-py` package.

> `filename` and `line_number` are optional — you can send generic notifications (e.g. "Customer onboarded") without them, not just code error alerts.

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
        teams=TeamsCreds(webhook_url="your_teams_webhook_url"),
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

1. `message_details`: An instance of `MessageDetails` that contains the details of the notification message, such as the title, text, severity, source, and timestamp. `filename` and `line_number` are optional.
2. `creds`: An instance of `Creds` that holds the credentials for Discord, Slack, MS Teams, and email notifications.

> These creds are independent of each other and one can just send Discord notifications using this message object (same applies for other combinations of these):
```
message = Message(
    message_details=MessageDetails(
        title="Customer Onboarded",
        text="Acme Corp has been successfully onboarded.",
        severity=0,
        source="CRM System",
        time=datetime.now(),
    ),
    creds=Creds(
        discord=DiscordCreds(
            token="your_discord_bot_token",
            channel_id=your_discord_channel_id,
            team_id=your_discord_team_id,
        ),
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
1. Go to [Slack Apps](https://api.slack.com/apps) and click **Create New App**.
2. Choose **From scratch**, give it a name, and select your workspace.
3. In the app settings, go to **Incoming Webhooks** (under Features) and toggle it **On**.
4. Click **Add New Webhook to Workspace**, select the channel you want to post to, and click **Allow**.
5. Copy the generated webhook URL — that's your `webhook_url`.

### 3. MS Teams:
1. In Microsoft Teams, go to the channel where you want to receive notifications.
2. Click **More options (...)** next to the channel and select **Workflows**.
3. Search for and select the **Post to a channel when a webhook request is received** template.
4. Configure the workflow parameters and click **Save**.
5. Copy the generated webhook URL — that's your `webhook_url`.

For more details, see [Send messages in Teams using incoming webhooks](https://support.microsoft.com/en-us/office/send-messages-in-teams-using-incoming-webhooks-323660ec-12ca-40b1-a1d3-a3df47e808c4).

### 4. Email (for gmail):
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

