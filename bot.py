#-*-coding: UTF-8 -*-
import os, json
import discord, asyncio

app = discord.Client()

# Read Config JSON
json_data = open(os.getcwd() + "/jaram-bot-token/.discord_config", encoding='utf-8').read()
config_json = json.loads(json_data)

token = config_json["token"]
text_channel_general = config_json["text_channel_general"]
footer = config_json["footer"]
chat_link = config_json["chat_link"]
administrator_id = config_json["administrator"]
mstatus = 0

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
    global mstatus
    if message.author.bot:
        if mstatus == 1:
            await message.add_reaction("\u2b55") # O
            await message.add_reaction("\u274c") # X
            mstatus = mstatus - 1
        else:
            return None

    if message.content == "$help":
        embed = discord.Embed(title="명령어 목록", description="$help - 봇 도움말 불러오기 \n$link - 자람 오픈채팅방 링크 목록 불러오기\n$contribute - 자람봇에 기여하기(링크)\n$admin - 관리자 소환하기(기술적 문제나 문의사항 처리)\n\n*다른기능은 추후 추가예정.*", color=0x6FA8DC)
        embed.set_footer(text=footer)

        await message.channel.send(embed=embed)

    if message.content == "$link":
        embed4 = discord.Embed(title="자람 오픈채팅방 목록", description=chat_link, color=0xFF9900)
        embed4.set_footer(text=footer)

        await message.channel.send(embed=embed4)

    if message.content == "$admin":
        mstatus = mstatus + 1
        embed5 = discord.Embed(title="관리자를 호출하시겠습니까?", description="관리자를 호출하실려면 :o:, 아니면 :x:를 눌러주세요.", color=0xFFD966)
        embed5.set_footer(text=footer)
        
        await message.channel.send(embed=embed5)

        def check(reaction, user):
            return user == message.author and (str(reaction.emoji) == "\u2b55" or str(reaction.emoji) == "\u274c")

        try:
            reaction, user = await app.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await message.channel.send("시간초과!")

        else:
            if str(reaction.emoji) == "\u2b55":
                await message.channel.send(administrator_id)
            elif str(reaction.emoji) == "\u274c":
                await message.channel.send("싫음 말구.")

    if message.content == "$contribute":
        embed2 = discord.Embed(title="To contribute", description="기능을 추가는 언제든지 환영입니다~", url="https://github.com/Taewan-P/jaram-gaming-welcomebot/", color=0x6FA8DC)
        embed2.set_footer(text=footer)

        await message.channel.send(embed=embed2)


@app.event
async def on_member_join(member):
    channel = member.guild.get_channel(text_channel_general)

    embed3 = discord.Embed(title="Welcome to Jaram Gaming Server!!", description=f"{member.mention}님. 누군지 알 수 있게 간단히 자기소개 부탁드려요~", color=0x6FA8DC)
    embed3.set_footer(text=footer)

    await channel.send(embed=embed3)

app.run(token)
