import nextcord
import requests
from nextcord.ext import commands
import re
import string
import nltk
import tensorflow as tf
import tensorflow_hub as hub
from dotenv import load_dotenv
import os
load_dotenv()
nltk.download('stopwords')
from nltk.corpus import stopwords
web_address = re.compile(r"(?i)http(s):\/\/[a-z0-9.~_\-\/]+")
user = re.compile(r"(?i)@[a-z0-9_]+")
regex_list = [web_address, user]

bot = commands.Bot(command_prefix='$')

embed = hub.KerasLayer("https://tfhub.dev/google/nnlm-en-dim50/2",input_shape=[],dtype=tf.string,trainable=True)
model = tf.keras.Sequential([
    embed,
    tf.keras.layers.Dense(32,activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(32,activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

weight_dir = os.path.dirname("model/")
weights = tf.train.latest_checkpoint(weight_dir)

model.load_weights(weights)

def clean(inp):
    """clean from stopwords and other stuff, convert to list, back to string"""
    if isinstance(inp, float):
        inp = 'a'
    STOPWORDS = stopwords.words('english') 
    # Check characters to see if they are in punctuation
    nopunc = [char for char in inp.split("\n") if char not in string.punctuation and all(re.search(regex, char.lower()) is None for regex in regex_list)]
  
    # Join the characters again to form the string.
    nopunc = ''.join(nopunc)
    
    # Now just remove any stopwords
    return ' '.join([word for word in nopunc.split() if word.lower() not in STOPWORDS])
  
@bot.event
async def on_message(message):
    if message.author.bot == True:
        pass
    else:
        tester = [clean(message.content)]
        response = model.predict(tester)
        print('test: your score is ', response)
        #tester is the thing put into the dataset
        await message.channel.send(f'test: your score is {response}')

class MyClient(nextcord.Client):
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello World!')   

@bot.command
def false_pos():
    pass

@bot.command
def false_neg():
    pass




bot.run("token")