import os, json
import discord

app = discord.Client()

json_data = open(os.getcwd() + "/.discord_config").read()
config_json = json.loads(json_data)

token = config_json["token"]
text_channel_general = config_json["text_channel_general"]
footer = config_json["footer"]
chat_link = config_json["chat_link"]
administrator_id = config_json["administrator"]

@app.event
async def on_ready():
    print('Logged in as')
    print(app.user.name)
    print(app.user.id)
    print('------')
    game = discord.Game("Jaram bot | $help")
    await app.change_presence(status=discord.Status.online, activity=game)

@app.event
async def on_message(message):
    if message.author.bot:
        return None

    if message.content == "$help":
        embed = discord.Embed(title="명령어 목록", description="$help - 봇 도움말 불러오기 \n$link - 자람 오픈채팅방 링크 목록 불러오기\n\n다른기능은 추후 추가예정.", color=0x6FA8DC)
        embed.set_footer(text=footer)

        embed2 = discord.Embed(title="To contribute", description="기능을 추가하려면 클릭하세요", url="https://github.com/Taewan-P/jaram-gaming-welcomebot/", color=0x6FA8DC)
        embed2.set_footer(text=footer)
        await message.channel.send(embed=embed)
        await message.channel.send(embed=embed2)

    if message.content == "$link":
        embed4 = discord.Embed(title="자람 오픈채팅방 목록", description=chat_link, color=0xFF9900)
        embed4.set_footer(text=footer)
        
        await message.channel.send(embed=embed4)
        await message.channel.send(administrator_id)

@app.event
async def on_member_join(member):
    channel = member.guild.get_channel(text_channel_general)

    embed3 = discord.Embed(title="Welcome to Jaram Gaming Server!!", description=f"{member.mention}님. 누군지 알 수 있게 간단히 자기소개 부탁드려요~", color=0x6FA8DC)
    embed3.set_footer(text=footer)

    await channel.send(embed=embed3)

app.run(token)
