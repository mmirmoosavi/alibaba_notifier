# Alibaba Notifier


# Description:

🚀 Stay ahead of the curve with the AliBaba Notifier! 🛫

The AliBaba Notifier is a Python project designed to help travelers find the best flight deals from Iran to international destinations. With real-time flight price monitoring and Telegram alerts, you'll never miss an opportunity to save on your next trip.

Key Features:

✈️ Real-time Flight Data: Retrieve the latest flight details from the Alibaba website.

📈 Price Tracking: Monitor flight prices, so you can book at the perfect moment.

📬 Telegram Notifications: Get price drop alerts delivered directly to your Telegram channel.

🔒 Secure: Built with your privacy in mind. Your data is safe and never shared.

🕒 Customizable: Set your own price threshold to trigger notifications.

👨‍💻 Open Source: Feel free to contribute or adapt it to your needs.


## Prerequisites

Before running the Docker container, ensure you have the following prerequisites installed on your system 
(system or server should not have Iran IP because of Telegram Filtering) :

- Docker: [Install Docker](https://docs.docker.com/get-docker/)

## Getting Started

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo

   
2. create your Telegram Bot here https://t.me/BotFather and get bot token id 
3. create a Telegram Channel and add Telegram bot to channel to notify.
4. get chanel_chat_id from there https://api.telegram.org/bot<your_bot_token>/getUpdates 
( if you add the bot on your channel you can see channel chat id in json "result" section)

5. create .env file on your-repo
6. add BOT_TOKEN and also CHANNEL_CHAT_ID in and departure Date on your env file
7. build docker image

    ```bash
   docker build -t aliba_notifier .

8. run docker container

    ```bash
   docker run --env_file=.env alibaba_notifier

