#-*-coding: UTF-8 -*-
import os, json, re
import discord, asyncio

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

app = discord.Client()

# Read Config JSON
json_data = open(os.getcwd() + "/jaram-bot-token/.discord_config", encoding='utf-8').read()
config_json = json.loads(json_data)

token = config_json["token"]
text_channel_general = config_json["text_channel_general"]
footer = config_json["footer"]
chat_link = config_json["chat_link"]
administrator_id = config_json["administrator"]
github_icon = config_json["github_icon"]

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
        embed.set_footer(text=footer, icon_url=github_icon)

        await message.channel.send(embed=embed)

    if message.content == "$link":
        embed4 = discord.Embed(title="자람 오픈채팅방 목록", description=chat_link, color=0xFF9900)
        embed4.set_footer(text=footer, icon_url=github_icon)

        await message.channel.send(embed=embed4)

    if message.content == "$admin":
        mstatus = mstatus + 1
        embed5 = discord.Embed(title="관리자를 호출하시겠습니까?", description="관리자를 호출하실려면 :o:, 아니면 :x:를 눌러주세요.", color=0xFFD966)
        embed5.set_footer(text=footer, icon_url=github_icon)

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
        embed2.set_footer(text=footer, icon_url=github_icon)

        await message.channel.send(embed=embed2)

    if message.content == "$owsearch":
        embed6 = discord.Embed(title="Overwatch 점수 검색", description="'배틀태그#숫자' 형식으로 입력해주세요.", color=0x82CC62)
        embed6.set_footer(text=footer, icon_url=github_icon)

        await message.channel.send(embed=embed6)

        def check(m):
            return m.author == message.author and m.channel == message.channel

        try:    
            m = await app.wait_for('message',timeout=25.0, check=check)
        except asyncio.TimeoutError:
            await message.channel.send("시간초과!")
        else:
            battletag_bool = bool(re.search('.[#][0-9]', m.content))
            if battletag_bool:
                battletag = m.content.replace("#", "-")
                req = Request("https://playoverwatch.com/ko-kr/career/pc/" + battletag)
                res = urlopen(req)

                bs = BeautifulSoup(res, "html.parser")
                scores = bs.findAll("div", attrs={"class": "competitive-rank-level"})

                competitive_score = [i.text for i in scores[:3]]
                if not competitive_score:
                    await message.channel.send("비공개 프로필 또는 존재하지 않습니다. 배틀태그와 뒤에 숫자를 다시 확인해 주세요.")
                else:
                    await message.channel.send("돌격 : " + competitive_score[0] + "\n공격 : " + competitive_score[1] + "\n지원 : " + competitive_score[2])

            else:
                # Invalid
                await message.channel.send("Invalid BattleTag!!!!")

@app.event
async def on_member_join(member):
    channel = member.guild.get_channel(text_channel_general)

    embed3 = discord.Embed(title="Welcome to Jaram Gaming Server!!", description=f"{member.mention}님. 누군지 알 수 있게 간단히 자기소개 부탁드려요~", color=0x6FA8DC)
    embed3.set_footer(text=footer, icon_url=github_icon)

    await channel.send(embed=embed3)

app.run(token)
