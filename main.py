import discord
from discord.ext import commands
import tokens
import os
import random
import bot_replies as br

docs = ('.docx', '.pdf', '.pptx', '.xlsx', '.txt', '.zip')
pics = ('jpeg', 'jpg', 'png', 'webp')
vids = ('.mp4', '.mkv', '.mov')
greetings = ('hello', 'hi', 'hey', 'yo', 'sup', 'morning', 'afternoon', 'evening', 'hola', 'ciao', 'bonjour', 'hallo', 'howdy', 'aloha', 'greetings', 'yo', 'hiya', 'salut', 'hail', 'hi')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

# this must be visible in the raspberry pi

def get_whitelist(filepath="whitelist.txt"):
    with open(filepath, 'r') as file:
        todos = file.readlines()
    return todos


def put_whitelist(tds, filepath="whitelist.txt"):
    with open(filepath, 'w') as file:
        file.writelines(tds)


def get_list(path, filetype):
    list_of_things = [str(i+1)+'.' + file for i, file in enumerate(os.listdir(path)) if file.endswith(filetype)]
    return list_of_things


def get_list_for_fetch(path, filetype):
    list_of_things = [file for file in os.listdir(path) if file.endswith(filetype)]
    return list_of_things


def create_embed(title, description):
    embed = discord.Embed(title=title, description=description, color=discord.Color.pink())
    embed.set_thumbnail(url='attachment://Vault Bot(1).png')
    return embed


async def send_message(ctx, response, is_private):
    try:
        if isinstance(response, dict) and 'file' in response:
            await ctx.send(file=discord.File(response['file']))
        else:
            await ctx.author.send(response) if is_private else await ctx.send(response)
    except Exception as e:
        print(e)


@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')
    await bot.change_presence(status=discord.Status.idle)


@bot.command(name='dm')
async def bot_command(ctx):
    await send_message(ctx, response=random.choice(br.bot_responses), is_private=True)


@bot.command(name='pics', aliases=['piclist'])
async def pic_list_command(ctx):
    pic_list = get_list('pics', pics)
    if pic_list:
        embed = create_embed("Picture List", "\n".join(pic_list))
        file_path = 'Vault Bot(1).png'
        file = discord.File(file_path)
        await ctx.send(embed=embed, file=file)
    else:
        response = "No pictures found."
        await send_message(ctx, response, is_private=False)


@bot.command(name='docs', aliases=['doclist'])
async def doc_list_command(ctx):
    doc_list = get_list('docs', docs)
    if doc_list:
        embed = create_embed("Documents List", "\n".join(doc_list))
        file_path = 'Vault Bot(1).png'
        file = discord.File(file_path)
        await ctx.send(embed=embed, file=file)
    else:
        response = "No documents found."
        await send_message(ctx, response, is_private=False)


@bot.command(name='vids', aliases=['vidlist'])
async def doc_list_command(ctx):
    vid_list = get_list('vids', vids)
    if vid_list:
        embed = create_embed("Videos List", "\n".join(vid_list))
        file_path = 'Vault Bot(1).png'
        file = discord.File(file_path)
        await ctx.send(embed=embed, file=file)
    else:
        response = "No videos found."
        await send_message(ctx, response, is_private=False)


@bot.command(name='whitelist')
async def whitelist_command(ctx, *, arg):
    if arg != "":
        w = get_whitelist()

        if arg+'\n' in w:
            response = 'Already Whitelisted'
            await send_message(ctx, response, is_private=False)

        else:
            w.append(arg + '\n')
            put_whitelist(w)
            response = f'{ctx.author.mention} Whitelisted!'
            await send_message(ctx, response, is_private=False)
    else:
        response = 'No name to be whitelisted!'
        await send_message(ctx, response, is_private=False)

'''
@bot.command(name='roll')
async def roll_command(ctx, max_value: int):
    response = str(random.randint(1, max_value))
    await ctx.send(response)


@bot.command(name='rdwalls')
async def rdwalls_command(ctx):
    file_path = f"wallpapers/{random.choice(os.listdir('wallpapers'))}"
    response = {'file': file_path}
    await ctx.send(file=discord.File(response['file']))'''


@bot.command(name='fetch')
async def fetch_command(ctx, file_type: str, file_index: int):
    if file_type == 'doc':
        x = get_list_for_fetch('docs', docs)
        if 0 < file_index <= len(x):
            response = {'file': f"docs/{x[file_index - 1]}"}
            await ctx.send(file=discord.File(response['file']))
        else:
            await ctx.send(f"Invalid file index {file_index} for {file_type}")

    elif file_type == 'pic':
        y = get_list_for_fetch('pics', pics)
        if 0 < file_index <= len(y):
            response = {'file': f"pics/{y[file_index - 1]}"}
            await ctx.send(file=discord.File(response['file']))
        else:
            await ctx.send(f"Invalid file index {file_index} for {file_type}")

    elif file_type == 'vid':
        z = get_list_for_fetch('vids', vids)
        if 0 < file_index <= len(z):
            response = {'file': f"vids/{z[file_index - 1]}"}
            await ctx.send(file=discord.File(response['file']))
        else:
            await ctx.send(f"Invalid file index {file_index} for {file_type}")

    else:
        await ctx.send(f"Invalid file type {file_type}")


@bot.event
async def on_message(message):
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f'{username} said: "{user_message}" ({channel})')

    if message.author == bot.user:
        return
    if 'bot' in user_message:

        if any(insult in user_message for insult in br.insults):
            await message.channel.send(random.choice(br.savage_bot_replies))

        else:
            await message.channel.send(random.choice(br.bot_responses))

    if username == "akithememegod":
        if message.attachments:

            attachment = message.attachments[0]
            if channel == 'upload-files':

                if attachment.filename.endswith(docs):
                    await attachment.save(f"docs/{attachment.filename}")
                    response = f"{message.author.mention} Attachment {attachment.filename} saved!"
                    await message.channel.send(response)

                if attachment.filename.endswith(pics):

                    await attachment.save(f"pics/{attachment.filename}")
                    response = f"{message.author.mention} Attachment {attachment.filename} saved!"
                    await message.channel.send(response)

                if attachment.filename.endswith(vids):
                    await attachment.save(f"vids/{attachment.filename}")
                    response = f"{message.author.mention} Attachment {attachment.filename} saved!"
                    await message.channel.send(response)
            else:
                pass

    await bot.process_commands(message)


def run_discord_bot():
    bot.run(tokens.token)



