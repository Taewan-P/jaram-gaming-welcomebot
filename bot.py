#-*-coding: UTF-8 -*-
import os, json, re, random
import discord, asyncio

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib import parse

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
        embed = discord.Embed(title="명령어 목록", description="$help - 봇 도움말 불러오기 \n$link - 자람 오픈채팅방 링크 목록 불러오기\n$contribute - 자람봇에 기여하기(링크)\n$admin - 관리자 소환하기(기술적 문제나 문의사항 처리)\n$owsearch - 오버워치 전적 검색\n$team.split - 팀 분배 기능!! (1,2팀으로 분할가능)\n\n*다른기능은 추후 추가예정.*", color=0x6FA8DC)
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
        embed2 = discord.Embed(title="To contribute", description="기능 추가는 언제든지 환영입니다~", url="https://github.com/Taewan-P/jaram-gaming-welcomebot/", color=0x6FA8DC)
        embed2.set_footer(text=footer, icon_url=github_icon)

        await message.channel.send(embed=embed2)

    if message.content == "$owsearch":
        embed6 = discord.Embed(title="Overwatch 점수 검색", description="'배틀태그#숫자' 형식으로 입력해주세요.", color=0x82CC62)
        embed6.set_footer(text=footer, icon_url=github_icon)
        embed6.set_image(url="https://bnetcmsus-a.akamaihd.net/cms/blog_header/q4/Q4K237E1EGPI1467079634956.jpg")

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
                async with message.channel.typing():
                    req = Request("https://playoverwatch.com/ko-kr/career/pc/" + parse.quote(battletag))
                    res = urlopen(req)

                    bs = BeautifulSoup(res, "html.parser")
                    roles = bs.findAll("div", attrs={"class": "competitive-rank-tier"})
                    scores = bs.findAll("div", attrs={"class": "competitive-rank-level"})
                    public_status = bs.findAll("p", attrs={"class": "masthead-permission-level-text"})

                competitive_roles = [i.get("data-ow-tooltip-text") for i in roles[:len(roles)//2]]
                competitive_score = [i.text for i in scores[:len(scores)//2]]
                competitive_score_pretty = []

                # B S G P D M GM UKN
                def tier_status(r):
                    return {"B": "<:overwatch_bronze:637619081410772992> ", "S": "<:overwatch_silver:637619187115753496> ", "G": "<:overwatch_gold:637619348910899250> ", "P": "<:overwatch_platinum:637619477030109195> ", "D": "<:overwatch_diamond:637619833995001866> ", "M": "<:overwatch_master:637619988965883904> ", "GM": "<:overwatch_grandmaster:637620080070623244> ", "UKN": ":question: "}.get(r, ":question: ")

                for a in competitive_score:
                    try:    
                        if int(a) < 1500:
                            competitive_score_pretty.append(tier_status("B") + a)
                        elif int(a) > 1500 and int(a) < 2000:
                            competitive_score_pretty.append(tier_status("S") + a)
                        elif int(a) > 2000 and int(a) < 2500:
                            competitive_score_pretty.append(tier_status("G") + a)
                        elif int(a) > 2500 and int(a) < 3000:
                            competitive_score_pretty.append(tier_status("P") + a)
                        elif int(a) > 3000 and int(a) < 3500:
                            competitive_score_pretty.append(tier_status("D") + a)
                        elif int(a) > 3500 and int(a) < 4000:
                            competitive_score_pretty.append(tier_status("M") + a)
                        elif int(a) > 4000 and int(a) < 5000:
                            competitive_score_pretty.append(tier_status("GM") + a)
                        else:
                            competitive_score_pretty.append(tier_status("B") + a)
                    except ValueError:
                        competitive_score_pretty.append(tier_status("B") + a)

                if not public_status:
                    await message.channel.send("프로필이 존재하지 않습니다. 배틀태그와 뒤에 숫자를 다시 확인해 주세요.")
                else:
                    if public_status[0].text == "비공개 프로필":
                        await message.channel.send("비공개 프로필입니다. 프로필 공개 설정을 공개로 바꾼 뒤에 사용해 주세요.")
                    else:
                        score_result = ""
                        if len(competitive_roles) == 0 and len(competitive_score) == 0:
                            score_result = "아직 배치를 덜본것 같군요! 점수가 없습니다."
                        else:
                            for i in range(len(competitive_roles)):
                                score_result = score_result + competitive_roles[i] + " : " + competitive_score_pretty[i] + "\n"
                            score_result = score_result + "입니다."

                        embed7 = discord.Embed(title=battletag.split("-")[0] + " 님의 현재 시즌 경쟁전 점수", description=score_result, color=0x82CC62)
                        embed7.set_footer(text=footer, icon_url=github_icon)

                        await message.channel.send(embed=embed7)

            else:
                # Invalid
                await message.channel.send("Invalid BattleTag!!!!")

    if message.content == "$team.split":
        # Check if the user is in a voice channel
        if message.author.voice is None:
            await message.channel.send("이 기능을 사용하려면 보이스 채널에 들어가 있어야 합니다!")
        else:
            member_list = message.author.voice.channel.members
            member_list_name = [i.name + "#" + i.discriminator + "-" + str(i.id) for i in member_list if not i.bot]

            num = 1
            member_list_str = "제외할 인원이 없으면 0 을 입력해 주세요.\n\n"
            for s in member_list_name:
                member_list_str = member_list_str + str(num) + ". " + s.split("-")[0] + "\n"
                num = num + 1
            embed8 = discord.Embed(title="팀 분배에서 제외할 인원의 번호를 입력하세요. (여러명 선택 불가능 ㅠ, 자연수만 입력할것.)", description=member_list_str, color=0x6FA8DC)
            embed8.set_footer(text=footer, icon_url=github_icon)

            await message.channel.send(embed=embed8)

            def check(m):
                return m.author == message.author and m.channel == message.channel

            try:    
                m = await app.wait_for('message',timeout=25.0, check=check)
            except asyncio.TimeoutError:
                await message.channel.send("시간초과!")
            else:
                number_bool = bool(re.search('[1-9]\d*', m.content))
                if number_bool:
                    if int(m.content) > len(member_list_name):
                        await message.channel.send("그런 번호를 가진 사람은 없다네. 처음부터 다시 하도록.")
                    else:
                        async with message.channel.typing():
                            pop_num = int(m.content)
                            member_list_name.pop(pop_num-1)
                            random.shuffle(member_list_name)
                            team_a = member_list_name[:len(member_list_name)//2]
                            team_b = member_list_name[len(member_list_name)//2:]

                            num = 1
                            team_a_str = ""
                            team_b_str = ""

                            for a in team_a:
                                team_a_str = team_a_str + str(num) + ". " + a.split("-")[0] + "\n"
                                num = num + 1

                            num = 1
                            for b in team_b:
                                team_b_str = team_b_str + str(num) + ". " + b.split("-")[0] + "\n"
                                num = num + 1

                        embed9 = discord.Embed(title="A팀", description=team_a_str, color=0x6FA8DC)
                        embed10 = discord.Embed(title="B팀", description=team_b_str, color=0x6FA8DC)
                        embed9.set_footer(text=footer, icon_url=github_icon)
                        embed10.set_footer(text=footer, icon_url=github_icon)

                        await message.channel.send(embed=embed9)
                        await message.channel.send(embed=embed10)

                elif m.content == "0":
                    async with message.channel.typing():
                        random.shuffle(member_list_name)
                        team_a = member_list_name[:len(member_list_name)//2]
                        team_b = member_list_name[len(member_list_name)//2:]

                        num = 1
                        team_a_str = ""
                        team_b_str = ""

                        for a in team_a:
                            team_a_str = team_a_str + str(num) + ". " + a.split("-")[0] + "\n"
                            num = num + 1

                        num = 1
                        for b in team_b:
                            team_b_str = team_b_str + str(num) + ". " + b.split("-")[0] + "\n"
                            num = num + 1

                    embed9 = discord.Embed(title="A팀", description=team_a_str, color=0x6FA8DC)
                    embed10 = discord.Embed(title="B팀", description=team_b_str, color=0x6FA8DC)
                    embed9.set_footer(text=footer, icon_url=github_icon)
                    embed10.set_footer(text=footer, icon_url=github_icon)

                    await message.channel.send(embed=embed9)
                    await message.channel.send(embed=embed10)

                else:
                    await message.channel.send("자연수를 입력하라고")

@app.event
async def on_member_join(member):
    channel = member.guild.get_channel(text_channel_general)

    embed3 = discord.Embed(title="Welcome to Jaram Gaming Server!!", description=f"{member.mention}님. 누군지 알 수 있게 간단히 자기소개 부탁드려요~", color=0x6FA8DC)
    embed3.set_footer(text=footer, icon_url=github_icon)

    await channel.send(embed=embed3)

app.run(token)
