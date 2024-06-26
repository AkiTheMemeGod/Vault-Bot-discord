import random
import time

import discord
from discord.ext import commands

import bot_replies as br
import tokens
from dependencies import *

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=get_prefix, intents=intents)


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
    await bot.tree.sync()
    await bot.change_presence(status=discord.Status.idle)

    channel_id = 1176920698640408576
    startup_channel = bot.get_channel(channel_id)

    if startup_channel:
        await startup_channel.purge(limit=None)
        await startup_channel.send("@everyone"
                                   "https://tenor.com/view/getting-online-getting-online-gif-27546602")
    else:
        print("Could not find the specified channel for startup message.")


@bot.command(name='dm')
async def bot_command(ctx):
    response = f" I slid into your dm :wink:"
    await send_message(ctx, response=ctx.author.mention + response, is_private=False)
    await send_message(ctx, response=response + " well Hello there :wink:", is_private=True)


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
    if str(ctx.channel) == 'whitelist-people':
        if str(ctx.author)+'\n' in get_whitelist():
            if arg != "":
                w = get_whitelist()

                if arg+'\n' in w:
                    response = 'Already Whitelisted'
                    await send_message(ctx, response, is_private=False)
                    await ctx.message.delete()

                else:
                    w.append(arg + '\n')
                    put_whitelist(w)
                    response = f'{ctx.author.mention} Whitelisted!'
                    await send_message(ctx, response, is_private=False)
                    await ctx.message.delete()

            else:
                response = 'No name to be whitelisted!'
                await send_message(ctx, response, is_private=False)
        else:
            response = "You don't have whitelisting permissions :( !"
            await send_message(ctx, response, is_private=False)
            await ctx.message.delete()
    else:
        await ctx.message.delete()
        response = ("Wrong channel :no_entry_sign:"
                    " head over to : https://discord.com/channels/1234535098205081670/1238473007739965603")
        await send_message(ctx, response=response, is_private=False)


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
            print(discord.File(response['file']))
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
        if pin == tokens.admin_pin:
            try:
                if arg.lower() == 'all':
                    await ctx.channel.purge(limit=None)
                    await ctx.send("https://tenor.com/view/forget-never-happened-never-mind-men-in-black-gif-14323858974282234206")
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
async def on_message(message):
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f'{username} said: "{user_message}" ({channel})')

    if message.author == bot.user:
        return
    if 'bot' in user_message and str(message.author) != "Aki's Chat-Bot#6062":

        if any(insult in user_message for insult in br.insults):
            await message.channel.send(random.choice(br.savage_bot_replies))

        else:
            await message.channel.send(random.choice(br.bot_responses))

    if message.attachments:
        if channel == 'upload-files':
            attachments = message.attachments
            if username + "\n" in get_whitelist():
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
                response = "You are not whitelisted Yet to upload stuffs here :rofl:"
                await message.channel.send(response)
                await message.delete()

        else:
            response = ("You can't upload files here :no_entry_sign:"
                        "\nhead over to --> https://discord.com/channels/940587857414864976/1173226074075824259")
            await message.channel.send(response)
            await message.delete()

    if f"{get_pre()}change prefix to" in user_message:
        put_prefix(user_message[18:19])
        await message.channel.send(f"{message.author.mention} the prefix has been changed to `{get_pre()}`")

    if "prefix?" == user_message:
        response = f"`{get_pre()}` is the current prefix for the bot-->{bot.user}"
        await message.channel.send(response)

    await bot.process_commands(message)


@bot.event
async def on_shutdown():
    print("hi")
    channel = bot.get_channel(1176920698640408576)

    if channel:
        print("hi")
        await channel.send("I'm going offline. Goodbye!")

try:
    def run_discord_bot():
        bot.run(tokens.token)
except KeyboardInterrupt:
    on_shutdown()
