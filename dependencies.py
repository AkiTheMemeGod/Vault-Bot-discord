import os

import discord
from discord.ui import View

docs = ('.docx', '.pdf', '.pptx', '.xlsx', '.txt', '.zip')
pics = ('jpeg', 'jpg', 'png', 'webp')
vids = ('.mp4', '.mkv', '.mov')
files = {"docs": docs, 'pics': pics, "vids": vids}


def directory(username, what):
    try:
        path = f"Vault/{username}/{what}"
        if os.path.exists(path):
            return path
        else:
            if os.path.exists(f"Vault/{username}"):
                pass
            else:
                os.mkdir(f"Vault/{username}")
            if os.path.exists(path):
                pass
            else:
                os.mkdir(path)
                return path
    except Exception as e:
        print(e)


def get_whitelist(filepath="whitelist.txt"):
    with open(filepath, 'r') as file:
        whites = file.readlines()
    return whites


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


class MySelectDoc(View):
    @discord.ui.select(
        placeholder="Choose a Document",
        options=[discord.SelectOption(label=file,
                                      value=str(index)) for index, file in enumerate(
            get_list_for_fetch(directory("akithememegod", "docs"), files["docs"]))])
    async def select_callback(self, interaction, select):
        select.disabled = True
        file = select.values[0]
        username = str(interaction.user)
        file_list = get_list_for_fetch(directory(username, "docs"), docs)

        print(file_list)

        if file_list[int(file)] in file_list:
            if not file_list:
                await interaction.response.edit_message(f"No {file} found.")
                return
            response = {'file': f"{directory(username, 'docs')}/{file_list[int(file)]}"}
            await interaction.channel.send(file=discord.File(response['file']))
            await interaction.message.delete()

        else:
            await interaction.user.send(f"Invalid file type {file}")


class MySelectPic(View):
    @discord.ui.select(
        placeholder="Choose a Picture",
        options=[discord.SelectOption(label=file,
                                      value=str(index)) for index, file in enumerate(
            get_list_for_fetch(directory('akithememegod', "pics"), files["pics"]),
            start=0)])
    async def select_callback(self, interaction, select):
        select.disabled = True
        file = select.values[0]
        print(file)
        username = str(interaction.user)
        file_list = get_list_for_fetch(directory(username, "pics"), pics)
        print(file_list)

        if file_list[int(file)] in file_list:
            if not file_list:
                await interaction.response.edit_message(f"No {file} found.")
                return
            response = {'file': f"{directory(username, 'pics')}/{file_list[int(file)]}"}
            await interaction.channel.send(file=discord.File(response['file']))
            await interaction.message.delete()

        else:
            await interaction.user.send(f"Invalid file type {file}")


class MySelectVid(View):
    @discord.ui.select(
        placeholder="Choose a Video",
        options=[discord.SelectOption(label=file,
                                      value=str(index)) for index, file in enumerate(
            get_list_for_fetch(directory("akithememegod", "vids"), files["vids"]),
            start=0)])
    async def select_callback(self, interaction, select):
        select.disabled = True
        file = select.values[0]
        username = str(interaction.user)
        file_list = get_list_for_fetch(directory(username, "vids"), vids)
        print(file_list)

        if file_list[int(file)] in file_list:
            if not file_list:
                await interaction.response.edit_message(f"No {file} found.")
                return
            response = {'file': f"{directory(username, 'vids')}/{file_list[int(file)]}"}
            await interaction.channel.send(file=discord.File(response['file']))
            await interaction.message.delete()
        else:
            await interaction.user.send(f"Invalid file type {file}")


'''def get_select_options(file_list):
    # Check if file_list is empty or contains the default option
    if not file_list or (len(file_list) == 1 and file_list[0] == "loading"):
        return [default_option]

    return [
        discord.SelectOption(label=file, value=str(index))
        for index, file in enumerate(file_list, start=0)
    ]
'''