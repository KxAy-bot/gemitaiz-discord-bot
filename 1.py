import random
import os
import time
import nextcord
import datetime
from nextcord.ext import commands, tasks
from nextcord import Embed, Color, client

with open(r'nomi.txt', encoding="utf8") as f:
    nomi = f.read().splitlines()
with open(r'cognomi.txt', encoding="utf8") as l:
    cognomi = l.read().splitlines()

intents = nextcord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True

client = commands.Bot(command_prefix='%', intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} è operativo')

    OrarioDelProduce.start()


@client.command()
async def muovi(ctx, member: nextcord.Member, channel: nextcord.VoiceChannel):
    await member.move_to(channel)
    await ctx.send(f"Hey Gemitaiz, ho spostato {member.mention} in {channel}, proprio come mi hai chiesto!")
    print(f'{member} è stato spostato in {channel}')


@commands.cooldown(1, 30, commands.BucketType.user)
@client.command()
async def kick(ctx, member: nextcord.Member):
    await member.disconnect()
    await ctx.send(f"Hey Gemitaiz, ho kickkato {member.mention}. Spero che per te sia stata una scelta saggia🥶")
    print(f'{member} è stato disconnesso')


@client.command()
async def fragola(ctx):
    member = ctx.author
    await ctx.send(f'Parlando con un abitante del Lago Duria per capire quale nome dare a {member.mention}')
    nome = random.choice(nomi)
    cognome = random.choice(cognomi)
    username = nome.lower() + " " + cognome.lower()
    time.sleep(2)
    await member.edit(nick=username)
    await ctx.send(f'Bene, dopo una lunga sessione di duro lavoro, abbiamo deciso che il tuo nome ora è {username}')


@commands.cooldown(1, 30, commands.BucketType.user)
@client.command()
async def zitti(ctx, channel: nextcord.VoiceChannel):
    utente = ctx.author
    await ctx.send(f"È il Gemitaiz te rispondo ancora che voi? C'è ancora un pò de silenzio pe voi")
    for member in channel.members:
        await member.edit(mute=True)
    time.sleep(10)
    for member in channel.members:
        await member.edit(mute=False)
    await ctx.send(f"jkjk me l'ha chiesto {utente.mention}")


@client.command()
async def CursedDice(ctx):
    dado = random.randint(1, 6)
    user = ctx.author
    guild = ctx.guild
    if dado == 1:
        await ctx.send(f'{user.mention} ha rollato il dado ed è uscito {dado}')
        await user.disconnect()
    elif dado == 2:
        await ctx.send(f'{user.mention} ha rollato il dado ed è uscito {dado}')
        await user.edit(mute=True)
        time.sleep(10)
        await user.edit(mute=False)
    elif dado == 3:
        await ctx.send(f'{user.mention} ha rollato il dado ed è uscito {dado}')
        canali = ctx.guild.voice_channels
        canale = random.choice(canali)
        user = ctx.author
        await user.move_to(canale)
    elif dado == 4:
        await ctx.send(f"{user.mention} ha rollato il dado ed è uscito {dado}, Admin per 20 secondi!")
        guild = ctx.guild
        role = guild.get_role(1070799934498017310)
        await user.add_roles(role)
        time.sleep(20)
        await user.remove_roles(role)
    elif dado == 5:
        await ctx.send(f'{user.mention} ha rollato il dado ed è uscito {dado}')
        await ctx.send(f"ahahaahahah {user.mention}, non hai vinto un cazzo")
    elif dado == 6:
        await ctx.send(f'{user.mention} ha rollato il dado ed è uscito {dado}')
        vcs = 0
        while vcs < 20:
            await user.edit(mute=True)
            await user.edit(mute=False)
            vcs += 1


@client.command()
async def CursedHelp(ctx):
    await ctx.send("""CursedDice è una funzione che ti permette di tirare i "dadi maledetti" e subire il loro effetto:
        numero 1: vieni disconnesso
        numero 2: vieni mutato per 10 secondi
        numero 3: vieni spostato randomicamente in uno dei canali vocali del server
        numero 4: diventi admin per 10 secondi
        numero 5: non vinci nulla
        numero 6: vieni mutato per 20 volte ad intervalli molto corti""")


@client.command()
async def occhicoltello(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    source = nextcord.PCMVolumeTransformer(nextcord.FFmpegPCMAudio('arachidi.mp3', options="-loglevel panic"), 0.5)
    ctx.voice_client.play(source)
    time.sleep(4)
    await ctx.voice_client.disconnect()


@client.command()
async def cringe(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    source = nextcord.PCMVolumeTransformer(nextcord.FFmpegPCMAudio('oldcarhorn.mp3', options="-loglevel panic"), 0.5)
    ctx.voice_client.play(source)


@client.command()
async def esci(ctx):
    await ctx.voice_client.disconnect()


@client.command()
async def kaiju(ctx):
    user = ctx.author
    percentuale = random.randint(1, 100)
    if 80 <= percentuale <= 89:
        await ctx.send(f"{user.mention}, oggi sei all'{percentuale}% Kaiju")
    else:
        await ctx.send(f"{user.mention}, oggi sei al {percentuale}% Kaiju")


@commands.cooldown(1, 3, commands.BucketType.user)
@client.command()
async def smash(ctx):
    percentuale = random.randint(1, 100)
    server = ctx.guild
    membri = server.members
    tag = random.choice(membri)
    await ctx.send(f"{tag.mention} è uno smash al {percentuale}%")
    if 0 <= percentuale <= 49:
        await ctx.send("emmmhhh.... pass")
    if 50 <= percentuale <= 89:
        await ctx.send("emmmhhh.... smash")
    if 90 <= percentuale <= 100:
        await ctx.send("emhhhh..... smashone")


@client.command()
async def stato(ctx, status: str):
    await client.change_presence(activity=nextcord.Game(name=status))


@tasks.loop(minutes=1)
async def OrarioDelProduce():
    channel = client.get_channel(868249742616952912)
    orario = str(datetime.datetime.now().time().hour) + ':' + str(datetime.datetime.now().time().minute) + ':00'
    manda = str(datetime.time(hour=8, minute=8))

    if orario == manda:
        await channel.send("8:08, l'orario del pro duce")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = Embed(title=f"Hey {ctx.author} non provare a fare extrabeat",
                   description=f"Riprova tra {error.retry_after:.2f}s.", color=Color.red(),
                   url="https://www.ilcorrieredellacitta.com/wp-content/uploads/2019/11/gemitaiz.jpg")
        await ctx.send(embed=em)


@client.command()
async def inviti(ctx, usr: nextcord.Member):
    inviti_totali = 0
    for i in await usr.guild.invites():
        if i.inviter == usr:
            inviti_totali += 1
    if inviti_totali >= 1:
        await ctx.send(f"{usr.mention} ha creato {inviti_totali} inviti, con {i.uses} utilizzi. {i.created_at}, {i.channel}")
    else:
        await ctx.send(f"{usr.mention} non ha creato inviti")


client.run(os.environ["DISCORD_TOKEN"])