import discord
import responses
import tokens

docs = ('.docx', '.pdf', '.pptx', '.xlsx', '.txt')
pics = ('jpeg', 'jpg', 'png', 'webp')
vids = ('.mp4', '.mkv', '.mov')

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
        x = 'peace'
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

        elif message.attachments:  # Check for attachments
            attachment = message.attachments[0]
            if channel == 'upload-files':
                if attachment.filename.endswith(docs):
                    await attachment.save(f"docs/{attachment.filename}")
                    response = f"Attachment {attachment.filename} saved!"
                    await send_message(message, response, is_private=False)
                if attachment.filename.endswith(pics):
                    await attachment.save(f"pics/{attachment.filename}")
                    response = f"Attachment {attachment.filename} saved!"
                    await send_message(message, response, is_private=False)
                if attachment.filename.endswith(vids):
                    await attachment.save(f"vids/{attachment.filename}")
                    response = f"Attachment {attachment.filename} saved!"
                    await send_message(message, response, is_private=False)
            else:
                pass

        else:
            response = await responses.get_response(user_message)
            await send_message(message, response, is_private=False)

    client.run(tokens.token)
