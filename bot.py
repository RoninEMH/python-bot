# bot.py
import os
import time
import json
import gtts
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the voice channel"))


@bot.command()
async def createAllGreetings(ctx):
    otherURL = os.getcwd() + "/Greetings"
    if not os.path.exists(otherURL):
        os.mkdir(otherURL)

    jsonFile1 = open("members.json", "r")
    membersNames = json.load(jsonFile1)

    async for member in ctx.guild.fetch_members():
        print("processing with " + member.name)
        if member.bot:
            await ctx.message.channel.send(member.name + " is a bot")
            continue
        for memName in membersNames["data"]["members"]:
            if memName["id"] == member.id:
                url = os.getcwd() + "/./Greetings/" + memName["name"] + ".mp3"
                try:
                    open(url)
                    await ctx.message.channel.send(memName["name"] + " already has a file")
                except FileNotFoundError:
                    jsonFile2 = open("greetings.json", "r")
                    data = json.load(jsonFile2)
                    new_element = {"id": member.id, "name": memName["name"],
                                   "url": "/./Greetings/" + memName["name"] + ".mp3"}
                    data["data"]["users"].append(new_element)
                    jsonFile2.close()
                    jsonFile3 = open("greetings.json", "w")
                    json.dump(data, jsonFile3)
                    while True:
                        try:
                            tts = memName["name"] + " has joined the channel"
                            saver = gtts.gTTS(lang='en-us', text=tts)
                            saver.save(url)
                            break
                        except ValueError as ve:
                            print("Error")
                            print(ve)
                            continue
                    await ctx.message.channel.send("Created a file for " + memName["name"])
                    jsonFile3.close()
    jsonFile1.close()
    print("done")
    await ctx.message.channel.send("Done")


@bot.command()
async def createAllGoodbyes(ctx):
    otherURL = os.getcwd() + "/GoodByes"
    if os.path.exists(otherURL):
        os.mkdir(otherURL)

    jsonFile1 = open("members.json", "r")
    membersNames = json.load(jsonFile1)

    async for member in ctx.guild.fetch_members():
        print("processing with " + member.name)
        if member.bot:
            await ctx.message.channel.send(member.name + " is a bot")
            continue
        for memName in membersNames["data"]["members"]:
            if memName["id"] == member.id:
                url = os.getcwd() + "/./GoodByes/" + memName["name"] + ".mp3"
                try:
                    open(url)
                    await ctx.message.channel.send(memName["name"] + " already has a file")
                except FileNotFoundError:
                    jsonFile2 = open("goodbyes.json", "r")
                    data = json.load(jsonFile2)
                    new_element = {"id": member.id, "name": memName["name"],
                                   "url": "/./GoodByes/" + memName["name"] + ".mp3"}
                    data["data"]["users"].append(new_element)
                    jsonFile2.close()
                    jsonFile3 = open("goodbyes.json", "w")
                    json.dump(data, jsonFile3)
                    while True:
                        try:
                            tts = memName["name"] + " has left the channel"
                            saver = gtts.gTTS(lang='en-us', text=tts)
                            saver.save(url)
                            break
                        except ValueError as ve:
                            print("Error")
                            print(ve)
                            continue
                    await ctx.message.channel.send("Created a file for " + memName["name"])
                    jsonFile3.close()
    jsonFile1.close()
    print("done")
    await ctx.message.channel.send("Done")


@bot.event
async def on_voice_state_update(member, before, after):
    print(before)
    print(after)

    print(member)

    if member.bot:
        return

    if after.channel is not None and 'General' in after.channel.name:
        print("Hi ", member.name)

    elif 'General' in before.channel.name:
        print("Bye ", member.name)

    if before.self_stream is not after.self_stream:  # or before.self_deaf is not after.self_deaf
        return

    if before.self_mute is not after.self_mute and before.self_deaf is after.self_deaf:
        return

    if before.self_deaf is False and 'General' not in after.channel.name:
        return

    if after.self_deaf is True:
        return

    file = open("greetings.json", "r")
    data = json.load(file)

    for user in data["data"]["users"]:
        if user["id"] == member.id or user["name"] == member.name:
            if after.channel is not None:
                voice_channel = after.channel
                try:
                    open(os.getcwd() + user["url"])
                except FileNotFoundError:
                    print("audio not found for ", member.name)
                    return
                vc = await voice_channel.connect()
                vc.play(
                    discord.FFmpegPCMAudio(executable="ffmpeg",
                                           source=os.getcwd() + user["url"]))
                while vc.is_playing():
                    time.sleep(.1)
                await vc.disconnect()
    file.close()


bot.run(TOKEN)
