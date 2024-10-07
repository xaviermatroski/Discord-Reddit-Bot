import random
import requests
import discord
from discord import app_commands
from discord.ext import commands
from redvid import Downloader
import subprocess
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv(".env")

# Global variables-----------------------------------------------------
CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
SECRET_KEY = os.getenv('REDDIT_SECRET_KEY')
SUBREDDITS = ['Unexpected', 'funny', 'Animemes']

# Basic initializations-------------------------------------------------
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

data = {
    'grant_type': 'password',
    'username': os.getenv('REDDIT_USERNAME'),
    'password': os.getenv('REDDIT_PASSWORD')
}

headers = {'User-agent': 'MyAPI/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

TOKEN = res.json()['access_token']
headers['Authorization'] = f"bearer {TOKEN}"


# Functions to download and merge files----------------------------------
def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        print(f"Failed to download {url}")


def merge_audio_video(video_file, audio_file, output_file):
    command = ['ffmpeg', '-i', video_file, '-i', audio_file, '-c:v', 'copy', '-c:a', 'aac', output_file]
    subprocess.run(command)


# Reddit work(pulling data from the above declared subreddits)--------------------------------------------
read_posts = []
see_posts = []

for subreddit in SUBREDDITS:
    res = requests.get(f'https://oauth.reddit.com/r/{subreddit}/hot?raw_json=1', headers=headers).json()

    for data in res['data']['children'][1:]:  # Skip the first post
        post = {
            'title': data['data']['title'],
            'body': data['data']['selftext'],
            'media_url': None  # Default to None if no media is found
        }

        # Check for Reddit videos
        if data['data'].get('secure_media') and 'reddit_video' in data['data']['secure_media']:
            media_url = {
                'video_url': data['data']['secure_media']['reddit_video']['fallback_url'],
                'audio_url': "https://v.redd.it/" +
                             data['data']['secure_media']['reddit_video']['fallback_url'].split("/")[
                                 3] + "/DASH_AUDIO_128.mp4"
            }
            post['media_url'] = media_url
            see_posts.append(post)

        # Check for GIFs
        elif ('preview' in data['data'] and
              'images' in data['data']['preview'] and
              'variants' in data['data']['preview']['images'][0] and
              'gif' in data['data']['preview']['images'][0]['variants']):
            post['media_url'] = data['data']['preview']['images'][0]['variants']['gif']['source']['url']
            see_posts.append(post)

        # Check for images
        elif ('preview' in data['data'] and
              'images' in data['data']['preview']):
            post['media_url'] = data['data']['preview']['images'][0]['source']['url']
            see_posts.append(post)

        # If the post is just text
        else:
            read_posts.append(post)


# Discord work------------------------------------------------------------------
class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

        try:
            guild = discord.Object(id=os.getenv('DISCORD_ID'))
            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} commands to guild {guild.id}")

        except Exception as e:
            print(f"Error syncing commands: {e}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('hello'):
            await message.channel.send(f"Hi There {message.author}")


intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

Guild_ID = discord.Object(id=os.getenv('DISCORD_ID'))


@client.tree.command(name='hello', description='Say hello!', guild=Guild_ID)
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hi There!")


@client.tree.command(name='k', description='Imma give you what you want', guild=Guild_ID)
async def k(interaction: discord.Interaction, query: str):
    if query == 'read':
        my_ans = random.choice(read_posts)
        read_posts.remove(my_ans)
        await interaction.response.send_message(f"{my_ans['title']}\n{my_ans['body']}")
    elif query == 'see':
        my_ans = random.choice(see_posts)
        print(my_ans)
        see_posts.remove(my_ans)
        if isinstance(my_ans['media_url'], dict):
            await interaction.response.defer()

            download_file(my_ans['media_url']['video_url'], 'video.mp4')
            download_file(my_ans['media_url']['audio_url'], 'audio.mp3')

            merge_audio_video('video.mp4', 'audio.mp3', 'output.mp4')

            await interaction.followup.send(file=discord.File('output.mp4'))

            os.remove('video.mp4')
            os.remove('audio.mp3')
            os.remove('output.mp4')
        else:
            await interaction.response.send_message(my_ans['media_url'])
    elif query == 'quantity':
        await interaction.response.send_message(f"My inventory: {len(read_posts) + len(see_posts)}")
    else:
        await interaction.response.send_message("Type query as either 'read' or 'see' or 'quantity'")


client.run(os.getenv('DISCORD_CLIENT_ID'))
