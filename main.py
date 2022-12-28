import nextcord
import numpy as np
import requests
from nextcord.ext import commands
import re
import string
import nltk
from dotenv import load_dotenv
load_dotenv()
nltk.download('stopwords')
from nltk.corpus import stopwords
web_address = re.compile(r"(?i)http(s):\/\/[a-z0-9.~_\-\/]+")
user = re.compile(r"(?i)@[a-z0-9_]+")
regex_list = [web_address, user]

bot = commands.Bot(command_prefix='$')
def clean(input):
    """clean from stopwords and other stuff, convert to list, back to string"""
    if isinstance(input, float):
        input = 'a'
    STOPWORDS = stopwords.words('english') 
    # Check characters to see if they are in punctuation
    nopunc = [char for char in input if char not in string.punctuation and all(regex.search(char.lower()) is None for regex in regex_list)]
  
    # Join the characters again to form the string.
    nopunc = ''.join(nopunc)
    
    # Now just remove any stopwords
    return ' '.join([word for word in nopunc.split() if word.lower() not in STOPWORDS])
  
@bot.event
async def on_message(message):
    if message.author == bot:
        return
    else:
        url = 'http://localhost:8501/1/models/model:predict'
        tester = [clean(message.content)]
        data = {"instances":tester}
        response = requests.get(url, data=data,headers={})["predictions"]
        print('test: your score is ', response)
        #tester is the thing put into the dataset
        await message.channel.send('test: your score is ', response)

class MyClient(nextcord.Client):
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello World!')   
bot.run("TOKEN")