import nextcord
import numpy as np
import tensorflow as tf
from tensorflow import keras
from nextcord.ext import commands
import re
import string
import nltk
model = keras.models.load_model("cf-python/model")
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
        tester = list(clean(message.content))
        #tester is the thing put into the dataset
        print(model.predict(tester))

class MyClient(nextcord.Client):
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello World!')   
bot.run('OTk1NTA3NzQyNzY2Nzk3MDAw.GpIm-C.RE9tOEVfBE7cGKankkzizWELglf5ioZ9HoilBI')