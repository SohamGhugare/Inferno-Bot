import discord
from discord.ext import commands
import asyncio
import random
import datetime
import inspect

client = commands.Bot(command_prefix="?")

# Bot invite link:
# https://discord.com/api/oauth2/authorize?client_id=761130463968231435&permissions=2147352439&scope=bot


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('?help'))
    print("Bot is online!")

# --------- ALL MEMBER COMMANDS -------------

# User info

@client.command(aliases=['info'])
async def user(ctx, member: discord.Member):
    embed = discord.Embed(title=member.name, description=member.mention, color=discord.Color.green())
    embed.add_field(name='Joined at:', value=member.joined_at.strftime('%a, %#d %B %Y')) 

    #For time also :
    #(embed.add_field(name='Joined at:', value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
    embed.add_field(name="‏‏‎ ‎", value="‏‏‎ ‎")

    embed.add_field(name="Status:", value=member.status)

    embed.add_field(name="Bot:", value=member.bot)
    embed.add_field(name="‏‏‎ ‎", value="‏‏‎ ‎")


    embed.add_field(name="Nicked:", value=member.nick)
    embed.add_field(name="ID:", value=member.id)

    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)


# Ping command

@client.command(aliases=['Ping'])
async def ping(ctx):
    embed = discord.Embed(title='Pong!', description=ctx.author.mention, color=discord.Color.green())
    await ctx.send(embed= embed)


# DM command

@client.command(aliases=['DM', 'Dm'])
#@commands.has_any_role("Programmer", "Admin", "Owner", "Moderator")
async def dm(ctx, member: discord.Member,*, message):
    await member.send(f'**{ctx.author.name}** said {message}')
    await asyncio.sleep(1)
    await ctx.message.delete()

    embed = discord.Embed(title='Success!', color=discord.Color.green())
    embed.add_field(name="Message Sent", value=f"{ctx.author.mention} just sent a DM to {member.mention}")
    await ctx.send(embed=embed)
    



# Clear command

@client.command(aliases=['c', 'C', 'Clear'])
async def clear(ctx, amount=2.0):
    amount = round(amount)
    if amount > 0:
        if amount <= 100:
            await ctx.channel.purge(limit=amount)
            embed = discord.Embed(title='Success!', color=discord.Color.green())
            embed.add_field(name="Cleared messages!", value=f"{amount} messages were deleted by {ctx.author.mention}")
            await ctx.send(embed= embed)
        else:
            embed = discord.Embed(title='Error deleting messages!', color=discord.Color.red())
            embed.add_field(name="Amount too high!", value="Please enter amount less than 100 !")
            await ctx.send(embed= embed)

    else:
            embed = discord.Embed(title='Error deleting messages!', color=discord.Color.red())
            embed.add_field(name="Negative value detected!", value="Please enter a positive amount next time!")
            await ctx.send(embed= embed)


# Member command 

@client.command()
async def members(ctx):
    for x in ctx.guild.members:
        await ctx.send(x)   


# Loop command

@client.command(aliases=['l'])
async def loop(ctx, msg, times: int = 1):
    if times <= 20:
        for x in range(times):
            await ctx.send(msg)

    else:
        embed = discord.Embed(title='Error:', color=discord.Color.red())
        embed.add_field(name="Looping failed!", value='Cannot loop more than 20 times')
        await ctx.send(embed= embed)

# Boom
@client.command()
async def boom(ctx):
    await ctx.channel.purge(limit=5)
    await ctx.send(':regional_indicator_b: :regional_indicator_o: :o2: :regional_indicator_m: :regional_indicator_e: :regional_indicator_d:')


# Say command
@client.command(aliases=['Say'])
async def say(ctx,*, message):
    await ctx.message.delete()
    embed = discord.Embed(title='Chat!', description=f'Someone said: {message}', color=discord.Color.green())
    await ctx.send(embed=embed)


# Laugh command
laugh_gifs = [
    'https://tenor.com/view/jerry-funny-animal-laughing-gif-13124924', 
    'https://tenor.com/view/puffybear-puffy-cute-lol-happy-gif-12628636',
    "https://tenor.com/view/rolling-on-the-floor-laughing-emoji-gif-9682311",
    'https://tenor.com/view/milk-and-mocha-ahahah-lol-lolol-laughing-gif-11455721',
    'https://tenor.com/view/minions-lol-laugh-gif-4519852'
    ]

@client.command(aliases=['Laugh'])
async def laugh(ctx):
    await ctx.send(random.choice(laugh_gifs))


# Invite command

@client.command(aliases=['Invite', 'inv', 'Inv'])
async def invite(ctx):
    embed = discord.Embed(title='[Click here to invite the bot to your server]', description='Invite the bot to your server!', url = 'https://discord.com/api/oauth2/authorize?client_id=761130463968231435&permissions=2147352439&scope=bot',color=discord.Color.green())
    
    await ctx.send(embed = embed)


# Reminder command
@client.command(case_insensitive = True, aliases = ["remind", "remindme", "remind_me"])
@commands.bot_has_permissions(attach_files = True, embed_links = True)
async def reminder(ctx, time, *, reminder):
    print(time)
    print(reminder)
    user = ctx.message.author
    embed = discord.Embed(color=0x55a7f7, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text="If you have any questions, suggestions or bug reports, please DM me on discord: ShadowX#3244 ", icon_url=f"{client.user.avatar_url}")
    seconds = 0
    if reminder is None:
        embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.') # Error message
    if time.lower().endswith("d"):
        seconds += int(time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    if time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"
    if seconds == 0:
        embed.add_field(name='Warning',
                        value='Please specify a proper duration.')
    elif seconds < 300:
        embed.add_field(name='Warning',
                        value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
    elif seconds > 7776000:
        embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
    else:
        await ctx.send(f"Alright {ctx.author.mention}, I will remind you about {reminder} in {counter}.")
        await asyncio.sleep(seconds)
        await ctx.send(f"Hi {ctx.author.mention}, you asked me to remind you about {reminder} {counter} ago.")
        return
    await ctx.send(embed=embed)


# Eval command
@client.command(name='eval', pass_context=True)
async def eval_(ctx, *, command):
    if ctx.author.id == 698225613617496094:
        res = eval(command)
        if inspect.isawaitable(res):
            await res
        else:
            res
        comp = await ctx.send("Completed")
        await asyncio.sleep(2)
        await comp.delete()

# ----------- MODERATION COMMANDS ---------------

# Kick command

@client.command(aliases=['Kick'])
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason= "No reason provided"):
    await member.send(f"You have been kicked by {ctx.author.name}, Reason: {reason}")
    embed = discord.Embed(title='Kicked!', description=f'{member.name} has been kicked by {ctx.author.mention}', color=discord.Color.red())
    await ctx.send(embed=embed)
    await member.kick(reason=reason)


# Ban command

@client.command(aliases=['Ban'])
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member, *, reason= "No reason provided"):
    await member.send(f"You have been banned by {ctx.author.name}, Reason: {reason}")
    embed = discord.Embed(title='Banned!', description=f'{member.name} has been banned by {ctx.author.mention}', color=discord.Color.red())
    await ctx.send(embed=embed)
    await member.ban(reason=reason)


# Unban command
    
@client.command(aliases=['Unban'])
@commands.has_permissions(ban_members=True)
async def unban(ctx,*,member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split('#')
    
    for banned_entry in banned_users:
        user = banned_entry.user

        if (user.name, user.discriminator) == (member_name, member_disc):
            await ctx.guild.unban(user)
            embed = discord.Embed(title='Unbanned!', description=f'{member.name} has been unbanned by {ctx.author.mention}', color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(title='Error unbanning!', description=f'{member} was not found !', color=discord.Color.red())
        await ctx.send(embed=embed)


# Mute command

@client.command(aliases=['Mute'])
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(muted_role)

    embed = discord.Embed(title='Muted!', description=f'{member.name} has been muted by {ctx.author.mention}', color=discord.Color.red())
    await ctx.send(embed=embed)


# Unmute command

@client.command(aliases=['Unmute'])
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(muted_role)

    embed = discord.Embed(title='Unmuted!', description=f'{member.name} has been unmuted by {ctx.author.mention}', color=discord.Color.red())
    await ctx.send(embed=embed)


# ----------- EVENTS ------------

@client.event
async def on_message(message):
    if message.content.lower() == "noob" :
        await message.channel.send(f'{message.author.mention} *have a look at yourself before calling others noob!*')

    elif  message.content.lower() == "stfu" :
        await message.channel.send(f'{message.author.mention} no u stfu :rofl: ')
    
    elif  message.content.lower() == "lol":
        await message.add_reaction('😆')

    elif  message.content.lower() == "lmao" :
        await message.add_reaction('🤣')

    await client.process_commands(message)


# Help command

client.remove_command('help')
@client.command(aliases=['Help'])
async def help(ctx):
    embed = discord.Embed(title='Commands:', color=discord.Color.green())
    
    embed.add_field(name="?help", value='Shows this message')
    embed.add_field(name="?user", value='Shows the pinged user info')
    embed.add_field(name="?ping", value='Shows whether bot is online')
    embed.add_field(name="?dm", value='DMs the msg to the member')
    embed.add_field(name="?clear", value='Clears messages')
    embed.add_field(name="?loop", value='Loops a message')
    embed.add_field(name="?laugh", value='Sends laugh gif')
    embed.add_field(name="?say", value='Says msg secretly')
    embed.add_field(name="?boom", value='Booms the chat')
    embed.add_field(name="?modhelp", value='Sends a list of moderation commands to your DMs') 
    embed.add_field(name="?invite", value='Sends an invite link of the bot') 
    embed.add_field(name="?remind", value='Adds a local reminder for your task') 

    embed.set_footer(icon_url = ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
    await ctx.send(embed= embed)
   

@client.command()
@commands.has_permissions(kick_members = True)
async def modhelp(ctx):
    embed = discord.Embed(title='Moderation:', description='Sent a list of moderation commands to your DMs!', color=discord.Color.green())
    await ctx.send(embed = embed)
    modEmbed = discord.Embed(title='Moderation Commands:', color=discord.Color.green())
    modEmbed.add_field(name="Kick", value='?kick <mention> <reason> ', inline = False)
    modEmbed.add_field(name="Ban", value='?ban <mention> <reason> ', inline = False)
    modEmbed.add_field(name="Unban", value='?unban <mention> <reason> ', inline = False)
    modEmbed.add_field(name="Mute", value='?mute <mention> <reason> ', inline = False)
    modEmbed.add_field(name="Unmute", value='?unmute <mention> <reason> ', inline = False)
    modEmbed.add_field(name="NOTE", value='For muting and unmuting you should have a role name "Muted" in your server which has send messages disabled', inline = False)
    await ctx.author.send(embed = modEmbed)




client.run(BOT_TOKEN)
    
