# Discord Reddit Bot

A simple Python-powered Discord bot that serves memes and posts from subreddits to your Discord server.

## Features
- Fetches and posts content from specific subreddits directly into your Discord server.
- Supports both images and videos (with audio merged using FFmpeg).

## Setup Instructions

### Prerequisites
1. **Discord Bot Setup**:  
   - Create or use an existing server on Discord.
   - Head to the [Discord Developer Portal](https://discord.com/developers/applications) and create a bot. Obtain the **Discord Bot Token** and **Client ID**.
   
2. **Reddit App Setup**:  
   - Create a Reddit app by visiting [Reddit's Developer Console](https://www.reddit.com/prefs/apps). You’ll need the **Reddit Client ID** and **Secret Key**.

3. **FFmpeg Installation**:  
   - Install FFmpeg on your system to allow video and audio merging for posts containing both.

### Configuration

1. Create a `.env` file in your project directory with the following details:

    ```bash
    REDDIT_CLIENT_ID = 'your_reddit_client_id'
    REDDIT_SECRET_KEY = 'your_reddit_secret_key'
    REDDIT_USERNAME = 'your_reddit_username'
    REDDIT_PASSWORD = 'your_reddit_password'
    DISCORD_ID = 'your_discord_id'
    DISCORD_CLIENT_ID = 'your_discord_client_id'
    ```

2. Install required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Ensure FFmpeg is installed and accessible in your system’s PATH.

### Running the Bot

Once the setup is complete, run the bot using:

```bash
python main.py
```

## What the Bot Does

- This bot fetches posts from subreddits that you define and shares them in your Discord server.
- It handles image and video posts (including merging video and audio for Reddit videos).

## Commands
To use the bot, type the following commands in your server's text channel:
- /k read: Displays text posts from the specified subreddit.
- /k see: Shows other formats (images, GIFs, videos) available.

## References

- [Creating a Discord Bot](https://www.youtube.com/watch?v=CHbN_gB30Tw)
- [Creating a Reddit App](https://www.youtube.com/watch?v=FdjVoOf9HN4)
- [Installing FFmpeg](https://www.youtube.com/watch?v=4jx2_j5Seew)

## Notes
Feel free to modify or extend this bot to fit your needs. You can use it to share memes or any other content from Reddit subreddits in your Discord server.
