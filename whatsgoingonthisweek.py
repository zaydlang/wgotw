import discord
import string
import re
import random
from discord.ext import commands
import imaplib
import email
import re
import time
import datetime
from threading import Timer
import schedule

bot = commands.Bot(command_prefix='$')

@bot.event
# When the bot is ready this will be called.
async def on_ready():
    print('owo')

@bot.command()
async def start(ctx):
    await loop(ctx)

async def loop(ctx):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('bellarminebot@gmail.com', 'Bellybot')
    mail.list()
    # Out: list of "folders" aka labels in gmail.
    mail.select("inbox") # connect to inbox.

    mail.select(readonly=1) # Select inbox or default namespace
    date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
    (retcode, messages) = mail.search(None, '(SENTSINCE {0})'.format(date))

    if retcode == 'OK' and len(messages) > 0:
        print(messages[0])
        for num in messages[0].decode('utf-8').split(' '):
            typ, data = mail.fetch(num,'(RFC822)')
            msg = email.message_from_string(data[0][1].decode('utf-8'))
            typ, data = mail.store(num,'+FLAGS','\\Seen')
            if retcode == 'OK':
                wgotw = msg
                print(str(wgotw))

                schedule = []
                for day in days:
                    matches = re.findall(day + '[1-7\- :A-Za-z]*[1-7A-Z a-z]\n', str(wgotw))
                    for match in matches:
                        if (match.count('-') > 0):
                            schedule.append(match)

                print(schedule)
                channel = discord.utils.get(ctx.guild.channels, name="wgotw")
                await channel.send('\n'.join(x for x in schedule))
                
            break
                
    mail.close()

    print("checc")
    
bot.run('NTY1MzUwNDAzNjgwNjMyODU0.XK1J4Q.J7iOo8cLUSV0LFRCphtYwweHRVI')


