import random
import time

from discord.ext import commands

import bot_replies as br
import tokens
from dependencies import *

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)


async def send_message(ctx, response, is_private):
    try:
        if isinstance(response, dict) and 'file' in response:
            await ctx.send(file=discord.File(response['file']))
        else:
            await ctx.author.send(response) if is_private else await ctx.send(response)
    except Exception as e:
        print(e)


@bot.command(name='dm')
async def bot_command(ctx):
    response = f"I slid into your dm :wink:"
    await send_message(ctx, response=response, is_private=True)
    await ctx.message.delete()


@bot.command(name='pics', aliases=['piclist'])
async def pic_list_command(ctx):
    username = str(ctx.author)
    pic_list = get_list(directory(username, "pics"), pics)
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
    username = str(ctx.author)
    doc_list = get_list(directory(username, "docs"), docs)
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
    username = str(ctx.author)
    vid_list = get_list(directory(username, "vids"), vids)
    if vid_list:
        embed = create_embed("Videos List", "\n".join(vid_list))
        file_path = 'Vault Bot(1).png'
        file = discord.File(file_path)
        await ctx.send(embed=embed, file=file)
    else:
        response = "No videos found."
        await send_message(ctx, response, is_private=False)


@bot.command(name='whitelist')
async def whitelist_command(ctx, *, arg=""):
    if str(ctx.author)+'\n' in get_whitelist():
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
    else:
        response = "You don't have whitelisting permissions :( !"
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
    username = str(ctx.author)
    if file_type == 'doc':
        x = get_list_for_fetch(directory(username, "docs"), docs)
        if 0 < file_index <= len(x):
            response = {'file': f"{directory(username,'docs')}/{x[file_index - 1]}"}
            await ctx.send(file=discord.File(response['file']))
        else:
            await ctx.send(f"Invalid file index {file_index} for {file_type}")

    elif file_type == 'pic':
        y = get_list_for_fetch(directory(username, "pics"), pics)
        if 0 < file_index <= len(y):
            response = {'file': f"{directory(username,'pics')}/{y[file_index - 1]}"}
            await ctx.send(file=discord.File(response['file']))
        else:
            await ctx.send(f"Invalid file index {file_index} for {file_type}")

    elif file_type == 'vid':
        z = get_list_for_fetch(f"{directory(username,'vids')}", vids)
        if 0 < file_index <= len(z):
            response = {'file': f"{directory(username,'vids')}/{z[file_index - 1]}"}
            await ctx.send(file=discord.File(response['file']))
        else:
            await ctx.send(f"Invalid file index {file_index} for {file_type}")

    else:
        await ctx.send(f"Invalid file type {file_type}")


@bot.command(name='delete')
async def delete_command(ctx, arg, pin=""):
    if str(ctx.author) == 'akithememegod':
        if pin == '273636':
            try:
                if arg.lower() == 'all':
                    await ctx.channel.purge(limit=None)
                    await ctx.send("Nothing happened here :pepehands: :gun:")
                else:
                    try:
                        limit = int(arg)
                        if limit > 0:
                            await ctx.channel.purge(limit=limit + 1)
                        else:
                            await ctx.send("Please provide a positive integer for the number of messages to delete.")
                    except ValueError:
                        await ctx.send("Invalid argument. Use a positive integer or 'all'.")
            except Exception as e:
                print(e)
                await ctx.send("An error occurred while processing the command.")
        elif pin == "":
            await ctx.send("Provide the admin pin to proceed further, try again")
        else:
            await ctx.send("wrong pin !")
    else:
        await ctx.send("You dont have permissions to do that :rofl:")


@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')
    await bot.change_presence(status=discord.Status.idle)


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

    if username+"\n" in get_whitelist():

        if message.attachments:

            attachments = message.attachments
            if channel == 'upload-files':
                print("user authorized")
                for attachment in attachments:
                    if attachment.filename.endswith(docs):
                        await attachment.save(f"{directory(username,'docs')}/{attachment.filename}")

                    if attachment.filename.endswith(pics):
                        await attachment.save(f"{directory(username,'pics')}/{attachment.filename}")

                    if attachment.filename.endswith(vids):
                        await attachment.save(f"{directory(username,'vids')}/{attachment.filename}")

                response = f"{message.author.mention} saved at {time.asctime()}"
                await message.channel.send(response)

                await message.delete()

            else:
                pass
    else:
        response = f"You dont have access to upload things yet! - get whitelisted from the admin :)"
        await message.channel.send(response)

    await bot.process_commands(message)


def run_discord_bot():
    bot.run(tokens.token)



