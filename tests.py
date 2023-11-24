async def fetch_callback(interaction: discord.Interaction, file_type: str):
    await interaction.followup.send(f"Fetching {file_type}...")

    username = str(interaction.user)

    if file_type == 'doc':
        x = get_list_for_fetch(directory(username, "docs"), docs)
    elif file_type == 'pic':
        x = get_list_for_fetch(directory(username, "pics"), pics)
    elif file_type == 'vid':
        x = get_list_for_fetch(directory(username, "vids"), vids)
    else:
        await interaction.followup.send(f"Invalid file type {file_type}")
        return

    if x:
        response = {'file': f"{directory(username, file_type + 's')}/{x[0]}"}
        await interaction.followup.send(file=discord.File(response['file']))
    else:
        await interaction.followup.send(f"No {file_type}s found.")

@bot.command(name='fetch')
async def fetch_command(ctx):
    options = [
        discord.SelectOption(label='Documents', value='doc'),
        discord.SelectOption(label='Pictures', value='pic'),
        discord.SelectOption(label='Videos', value='vid')
    ]

    select = discord.ui.Select(placeholder="Please select a file type", options=options)
    view = discord.ui.View()
    view.add_item(select)

    interaction = await ctx.send("Please select a file type:", view=view)

    def check(i):
        return i.user == ctx.author and i.custom_id == select.custom_id

    try:
        response = await bot.wait_for("select_option", check=check, timeout=60.0)
        await fetch_callback(response, response.values[0])
    except asyncio.TimeoutError:
        await ctx.send("You took too long to make a selection.")


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

'''@bot.command(name='fetch')
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
        await ctx.send(f"Invalid file type {file_type}")'''