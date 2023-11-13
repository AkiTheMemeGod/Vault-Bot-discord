import discord
import responses
import tokens
import os
from responses import get_whitelist, put_whitelist
docs = ('.docx', '.pdf', '.pptx', '.xlsx', '.txt')
pics = ('jpeg', 'jpg', 'png', 'webp')
vids = ('.mp4', '.mkv', '.mov')


def get_list(path, filetype):
    listofthings = [str(i+1) + '. ' + file for i, file in enumerate(os.listdir(path)) if file.endswith(filetype)]
    return listofthings


def create_embed(title, description):
    embed = discord.Embed(title=title, description=description, color=discord.Color.pink())
    embed.set_thumbnail(url='attachment://Vault Bot(1).png')
    return embed


async def send_message(message, response, is_private):
    try:
        if isinstance(response, dict) and 'file' in response:
            await message.channel.send(file=discord.File(response['file']))
        else:
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        await client.change_presence(status=discord.Status.idle)

    @client.event
    async def on_message(message):
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if message.author == client.user:
            return

        elif '?bot' in user_message:
            response = await responses.get_response(user_message[1:])
            await send_message(message, response, is_private=True)

        if username == "akithememegod":
            if message.attachments:
                attachment = message.attachments[0]
                if channel == 'upload-files':

                    if attachment.filename.endswith(docs):
                        await attachment.save(f"docs/{attachment.filename}")
                        response = f"{message.author.mention} Attachment {attachment.filename} saved!"
                        await send_message(message, response, is_private=False)

                    if attachment.filename.endswith(pics):
                        await attachment.save(f"pics/{attachment.filename}")
                        response = f"{message.author.mention} Attachment {attachment.filename} saved!"
                        await send_message(message, response, is_private=False)

                    if attachment.filename.endswith(vids):
                        await attachment.save(f"vids/{attachment.filename}")
                        response = f"{message.author.mention} Attachment {attachment.filename} saved!"
                        await send_message(message, response, is_private=False)
                else:
                    pass
            elif '$pic list' in user_message:
                pic_list = get_list('pics', pics)
                if pic_list:
                    embed = create_embed("Picture List", "\n".join(pic_list))
                    file_path = 'Vault Bot(1).png'  # os.path.join("pics", pic_list[0])
                    file = discord.File(file_path)  # ,filename=pic_list[0])
                    await message.channel.send(embed=embed, file=file)
                else:
                    response = "No pictures found."
                    await send_message(message, response, is_private=False)

            elif '$doc list' in user_message:
                doc_list = get_list('docs', docs)
                if doc_list:
                    embed = create_embed("Documents List", "\n".join(doc_list))
                    file_path = 'Vault Bot(1).png'  # os.path.join("pics", pic_list[0])
                    file = discord.File(file_path)  # ,filename=pic_list[0])
                    await message.channel.send(embed=embed, file=file)
                else:
                    response = "No docs found."
                    await send_message(message, response, is_private=False)

            elif '$whitelist' in user_message:
                print("hi")
                if user_message[11:] != "":
                    w = get_whitelist()

                    if user_message[11:]+'\n' in w:
                        response = 'Already Whitelisted'
                        await send_message(message, response, is_private=False)

                    else:
                        w.append(user_message[11:] + '\n')
                        put_whitelist(w)
                        response = f'{message.author.mention} Whitelisted ! '
                        await send_message(message, response, is_private=False)

                else:
                    response = 'No name to be whitelisted ! '
                    await send_message(message, response, is_private=False)

            else:
                response = await responses.get_response(user_message)
                await send_message(message, response, is_private=False)

    client.run(tokens.token)
