import os

import discord

docs = ('.docx', '.pdf', '.pptx', '.xlsx', '.txt', '.zip')
pics = ('jpeg', 'jpg', 'png', 'webp')
vids = ('.mp4', '.mkv', '.mov')


def directory(username, what):
    path = f"Vault/{username}/{what}/"
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
