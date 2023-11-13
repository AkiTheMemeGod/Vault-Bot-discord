import os
import random as rd
import bot_replies as br


def get_info(filepath):
    x = []
    for i,n in enumerate(os.listdir(filepath)):
        x.append(f"{i+1}. {n}+\n")
    return x


def put_info(filepath, where):
    with open(filepath, 'w') as file:
        tds = get_info(where)
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
        return {'file': f"docs/{p_message[7:]}.pdf"}

    if "$list docs" in p_message:
        put_info('doc_list.txt', 'docs')
        return {'file': 'doc_list.txt'}

    if p_message == "$list pics":
        put_info('pic_list.txt', 'pics')
        return {'file': 'pic_list.txt'}

    if "$pic" in p_message:
        return {'file': f"pics/{p_message[5:]}"}

    if message == '$restart':
        os.system('python main.py')
        exit()
