# import requests
# import os
import asyncio

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import discord
from discord.ext import commands

# from webserver import keep_alive

intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="$",
                   description="Description of commands",
                   intents=intents)
bot.remove_command("help")

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration (optional)
options.add_argument("--no-sandbox")

cookie = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_D829271B68A84ACB6CD4F7BCA2D888F4A48C324BD196C7CEB8310E8A7B1B3F88E68C0A790758262187F0FA3E2F428E72FA74FC61BDCACF6971BD6339C57533931BCC40AC5EF60BC6E8EEB6F907D91DEF18F91E747002AF6416CA8B57F52496F1131566B5ABB7AB8263EF893C113AD5837F76D54A0F2406D6158A5C3973BFE47EC20FD98B324E07D64C033D7FCBF15A3BF497EE0EDBEBBAB6264218957BCAC9302268613ED578C2A40410C7B56C1A61C69E3D6EA1389456B212F101FE2BE8020A82D53F93030A7E923E37B7931932BF2095243F4C10A6EDD8AC0BDCFE5B88F913916EA2808D41FDDF9E8A478771ADE26849E4D4753623B2449C74C622FDC3E337D05EEA20900183036C8C5269D8AF73BB8C64A7D653B50E846BB598F69035EC7C626769C6BC0D4C59AFDF5616D441AC3F1745F1C911B1780D7E33A0573AD0FF3D54CBCB7254CC2603A5C1B166201F88A448B9EF4648DCE02F94E90C7C0832CAAE0F25AFBFD688CE3837CBC549C419F346B17DA0A0C5F27244DE87033C541F9F0E2A0C5F77B2D5AABAD2116CC094A3C36EDC9805A93F1EA93AEF54DEE95F7FD81ECFC03E1B7F148243057D453438AAFDD1DE7DF840420E2300B11301AC0FC9AF53971ABE1FC305B709B9A40482751B33E44019F2939C31DEF7CEF495442DD5B8C40B9A58007DC1234CB252011A5CC7900F67E0FB834C210CB89ECEDC23D319E285F5781DE8CDCF0BC8F30D05E86243811FE565E0CB83ACB5ED8C4A3B856C00C0EC9E2F8AB326451271BD0E7565C0A6CD03EF19C24557A8EEF7AAF4E57966974B14E8ADA688F148E1E4ACEE60BB8AF217A47648D4903B39C008163CE70AFFD3D0C9DC93A23168E93965AF226737A34401CB5E5B6BC7DAF00FE5931F45AC50B81778E687D9A0DE57227AFEDA95829A4747C11A599EEB46BD6292402DC2F98AB91054B17A4E6F09F4B796D02D7468033ACA8D19A59EDC2E2CF6EC9B34014E60EDEC15FA8B068634923033899CD2FAAE15B459A4230402C50BB55C8B80993846E9A790CC7F575169B31DF32807CEE62615929B6B14413F7EB11DEB6C7CD3B7E86EA67351B45A4E7A4A020E9700F66A2B31BA159C68A35ABBB105E473D5CFD406CF698512AC0474F13413BB15ECA16111AE0A6330203954"
discord_id = 734186978454798478
user_link = "https://www.roblox.com/users/167018321/profile"
bot_token = "ODIwMzI4NDIyMjgyNzU2MTA2.YEzkYA.b7N_zoWU9h0xcDqpHO7_kHS4G8o"

cookie_data = {
    "name": ".ROBLOSECURITY",
    "value": cookie,
    "domain": "roblox.com",
    "path": "/",
    "secure": True,
    "httpOnly": False
}

browser = webdriver.Chrome(options=options)
browser.get(user_link)
browser.add_cookie(cookie_data)
browser.refresh()

was_offline = True


@bot.event
async def on_connect():
    pass


@bot.command(name="shutdown")
@commands.is_owner()
async def shutdown(ctx):
    await bot.logout()
    quit()


@bot.event
async def on_ready():
    global data

    print('We have logged in as {0.user}'.format(bot))

    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="out for commands"))

    permissions = discord.Permissions.all()
    permissions.manage_channels = False
    permissions.manage_emojis = False
    permissions.manage_roles = False
    permissions.view_audit_log = False
    permissions.manage_webhooks = False
    permissions.manage_nicknames = False
    permissions.priority_speaker = False
    permissions.administrator = False

    while True:
        try:
            await LoopFunction()
        except Exception:
            pass


async def LoopFunction():
    global was_offline

    userToContact = bot.get_user(discord_id)
    # targetMember = bot.get_guild(int(os.environ['SERVER_ID'])).get_member(int(int(os.environ['DISCORD_TARGET_ID'])))

    # response = str(
    #     requests.get(user_link, cookies={'.ROBLOSECURITY': cookie}).content).strip()

    browser.refresh()
    response = browser.page_source.strip()

    robloxStatus = None
    # discordStatus = None
    # < span
    # data - testid = "presence-icon"
    # title = "Website"
    #
    # class ="online icon-online" > < / span >
    messageToSend = "**Roblox**: "

    # print(response)

    if "profile-avatar-status online icon-online" in response:
        robloxStatus = "online"
    elif "profile-avatar-status game icon-game" in response:
        robloxStatus = "in game"
    else:
        robloxStatus = "offline"

    # discordStatus = targetMember.status

    channel = userToContact.dm_channel
    if channel is None:
        await userToContact.create_dm()
        channel = userToContact.dm_channel

    recent_message = None

    async for message in channel.history(limit=10):
        if message.author != bot.user:
            continue
        recent_message = message.content
        break

    if robloxStatus != "in game":
        messageToSend += robloxStatus
    else:
        x = int(response.find('data-testid="presence-icon" title='))
        start = x + 35
        y = int(response.find('class="profile-avatar-status game icon-game"', x + 35))
        end = y - 2
        gameName = response[start:end]

        messageToSend += robloxStatus + ": __" + gameName + "__"

    # if targetMember.activity == None and str(discordStatus) == "online":
    #     messageToSend += ";\n**Discord**: __online__,"
    # else:
    #     messageToSend += ";\n**Discord**: " + str(discordStatus) + ", "
    #     if targetMember.activity == None:
    #         messageToSend = messageToSend[0: len(messageToSend) - 1]

    # if targetMember.activity != None:
    #     activityType = str(targetMember.activity.type)
    #     messageToSend += activityType[13:len(activityType)] + ", __" + targetMember.activity.name + "__"

    # print(messageToSend)
    # print(recent_message)
    if messageToSend != recent_message and (robloxStatus != "offline" or was_offline):
        await userToContact.send(messageToSend)
    was_offline = robloxStatus == "offline"

    await asyncio.sleep(5)
    # requests.get("https://anotherbottest.thevideo.repl.co")


# keep_alive()
bot.run(bot_token)