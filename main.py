import discord
import random
import buttons
import button
from discord.ext import commands
from keep_alive import keep_alive
from discord_components import *
import datetime
import math

Token = ""

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{str(len(client.guilds))} servers,Type .help"))
  print('Bot is ready!')

@client.event
async def on_member_join(member):
  print(f'{member} has left a server :(')

@client.event
async def on_member_remove(member):
  print(f'{member} has left a server :(')

@client.command()
async def ping(ctx):
  await ctx.send('Pong!')

@client.command()
async def clear(ctx, amount=5):
  await ctx.channel.purge(limit=amount)

@client.command()
async def clear_all(ctx, amount=999999999999999999999999999):
  await ctx.channel.purge(limit=amount)

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
  await member.kick(reason=reason)

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
  await member.ban(reason=reason)
  await ctx.send(f'Banned {member.name}#{member.discriminator}')

@client.command()
async def unban(ctx, *, member):
  banned_users =await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')


  for ban_entry in banned_users:
    user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
      return

@client.command(aliases=['8ball'])
async def eightball(ctx, *, question):
  responses  = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful.",
                "Maybe."]
  await ctx.send(f':8ball: Answer: {random.choice(responses)}')

@client.command()
async def deletechannel(ctx, channel: discord.TextChannel):
  mbed = discord.Embed(
    title = 'Success',
    description = f'Channel: {channel} has been deleted',
  )
  if ctx.authour.guild_permissions.manage_channels:
    await ctx.send(embed=mbed)
    await channel.delete()

buttons = [
  [
    Button(style=ButtonStyle.grey, label='1'),
    Button(style=ButtonStyle.grey, label='2'),
    Button(style=ButtonStyle.grey, label='3'),
    Button(style=ButtonStyle.blue, label='x'),
    Button(style=ButtonStyle.red, label='Exit')
  ],
  [
    Button(style=ButtonStyle.grey, label='4'),
    Button(style=ButtonStyle.grey, label='5'),
    Button(style=ButtonStyle.grey, label='6'),
    Button(style=ButtonStyle.blue, label='/'),
    Button(style=ButtonStyle.red, label='<-')
  ],
    [
    Button(style=ButtonStyle.grey, label='7'),
    Button(style=ButtonStyle.grey, label='8'),
    Button(style=ButtonStyle.grey, label='9'),
    Button(style=ButtonStyle.blue, label='+'),
    Button(style=ButtonStyle.red, label='Clear')
  ],
    [
    Button(style=ButtonStyle.grey, label='00'),
    Button(style=ButtonStyle.grey, label='0'),
    Button(style=ButtonStyle.grey, label='.'),
    Button(style=ButtonStyle.blue, label='-'),
    Button(style=ButtonStyle.green, label='+')
  ],
]


def calculator(exp):
  o = exp.replace('x', '*')
  result = ''
  try:
    result=str(eval(o))
  except:
    result='An error occured'
    return result

@client.command()
async def calc(ctx):
  m = await ctx.send(content='Loading Calculator')
  expression = None
  delta = datetime.datetime.utcnow() + datetime.timedelta(minutes = 5)
  e = discord.Embed(title=f'{ctx.author.name}\'s | {ctx.author.id}', description= expression, timestamp=delta)
  await m.edit(components=buttons, embed = e)
  while m.created_at < delta:
    res = await client.wait_for('button_click')
    reslabel = res.component.label
    if res.author.id == int(res.message.embeds[0].title.split('|')[1]) and res.message.embeds[0].timestamp < delta:
      expression = res.message.embeds[0].description
      if expression == 'None' or expression == 'An error occured':
        expression = ''
      if reslabel == 'Exit':
        await res.respond(content= 'Calculator Closed', type=7)
        break
      elif reslabel == '<-':
        expression = expression[:-1]
      elif reslabel == 'Clear':
        expression = None
      elif reslabel == '=':
        expression = calculator(expression)
      else:
        expression += reslabel
        f=discord.Embed(title=f'{res.author.name}\'s calculator|{res.author.id}', description=expression, timestamp=delta)
        await res.respond(content='', embed=f, component=buttons, type=7)


keep_alive()
client.run(Token)
