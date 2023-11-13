import os
import random as rd
import bot_replies as br

docs = ('.docx', '.pdf', '.pptx', '.xlsx', '.txt')
pics = ('jpeg', 'jpg', 'png', 'webp')
vids = ('.mp4', '.mkv', '.mov')


def get_list(path, filetype):
    things = [file for file in os.listdir(path) if file.endswith(filetype)]
    return things


def get_whitelist(filepath="whitelist.txt"):
    with open(filepath, 'r') as file:
        todos = file.readlines()
    return todos


def put_whitelist(tds, filepath="whitelist.txt"):
    with open(filepath, 'w') as file:
        file.writelines(tds)


async def get_response(message: str) -> str or dict:
    p_message = message.lower()

    if 'bot' in p_message:

        if any(insult in p_message for insult in br.insults):
            return rd.choice(br.savage_bot_replies)

        else:
            return rd.choice(br.bot_responses)

    if '$roll' in message:
        return str(rd.randint(1, int(message[6:])))

    if p_message == '$help':
        return br.helps

    if p_message == '$rdwalls':
        return {'file': f"wallpapers/{rd.choice(os.listdir('wallpapers'))}"}

    if "$fetch" in p_message:

        if p_message[7:10] == "doc":
            x = get_list('docs', docs)

            if p_message[7:] != "":
                return {'file': f"docs/{x[int(p_message[11:])-1]}"}

            else:
                return f"Invalid file name {p_message[7:]}"

        if p_message[7:10].endswith(pics):
            y = get_list('pics', pics)

            if p_message[7:] != "":
                return {'file': f"pics/{y[int(p_message[11:])-1]}"}

            else:
                return f"Invalid file name {p_message[7:]}"

        if p_message[7:10].endswith(vids):
            z = get_list('vids', vids)

            if p_message[7:] != "":
                return {'file': f"vids/{z[int(p_message[11:])-1]}"}

            else:
                return f"Invalid file name {p_message[7:]}"

    if message == '$restart':
        os.system('python main.py')
        exit()
