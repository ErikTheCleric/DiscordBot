# Erik Hale 7/1/2021
# Discord Bot code for: StarGazer

# This Discord bot (using your own TOKEN from your discord bot) relays different
#   space quandaries like who is in space at the moment or the different types of
#   objects and their quantities in space. This is all done through a variety of
#   APIs, which pulls the information from the interface and reformat the data
#   to be friendlier to Discord. There is also a unique "promotion" of roles:
#   Whenever you ask a question you are promoted to a higher tier of role.

# Future features to work on:
#   > More space links and APIs (perhaps more about planets and their facts)
#       > Calculate how far away the ISS is to you?
#   > Pre-adding the roles into a server that are necessary for the promotions: Done

# One thing that I have added was permissions, below are all the permissions and the
# website to have a guide to add more or take away some. I have OR-ed the values together
# and placed that in the permssions tab:
# 0x40 | 0x200 | 0x400 | 0x1 | 0x4000000 | 0x800 | 0x4000 | 0x8000 | 0x10000 | 0x20000 | 0x40000 | 0x100000 | 0x200000
# website: https://discord.com/developers/docs/topics/permissions

import discord
import requests
import json
import geocoder
from discord.utils import get

TOKEN = (Your Discord Token Here)
NAME_OF_BOT = "StarGazer"

# The Permissions for the created roles
permissions = 70766145

# The different ranks and roles for promotion
RANK1 = "Space Enthusiast"
RANK2 = "Outerspace Explorer"
RANK3 = "Certified Astronaut"
rank = [RANK1, RANK2, RANK3]

client = discord.Client()

def help():
    # a help function that returns the different functions that the bot can do
    output = "Hello, i'm " + NAME_OF_BOT + ", here is what I can do for you:\n" + \
             "> - \'$loc_iss\' to get the location of the ISS\n" \
             "> - \'$ppl_iss\' to get the astronauts on the ISS\n" \
             "> - \'$ppl_spc\' to get the total amount of people in space\n" \
             "> - \'$obj_spc\' to get the number of objects in space\n"
    return output

def get_people_on_iss():
    # Using an api, retrieve who is aboard the ISS
    response = requests.get("http://api.open-notify.org/astros.json")
    request = json.loads(response.text)
    numOfAstro = 0

    # format the astronauts and return the people in the ISS
    outputPre = "Who is on the ISS right now?\nRequest status: " + request["message"] + "\n"
    outputPost = ""
    for n in range(request["number"]):
        if(request["people"][n]["craft"] == "ISS"):
            outputPost += "> " + request["people"][n]["name"] + "\n"
            numOfAstro += 1     # Increase the number for the num of astronauts on ISS
    outputPre += "> There are " + str(numOfAstro) + " people on the ISS:\n"
    return outputPre + outputPost

def get_people_in_space():
    # Using an api, retrieve who is in space
    response = requests.get("http://api.open-notify.org/astros.json")
    request = json.loads(response.text)

    # format the astronauts and return the people in space
    output = "Who is in space right now?\nRequest status: " + request["message"] + "\n"
    output += "There are " + str(request["number"]) + " people in space:\n"

    #iterate through the list and store the astronauts into the output
    for n in range(request["number"]):
        output += "> " + request["people"][n]["name"] + " aboard " + request["people"][n]["craft"] + "\n"

    return output

def get_location_iss():
    # Using this api, retrieve where the ISS is and load it into "request"
    response = requests.get("http://api.open-notify.org/iss-now.json")
    request = json.loads(response.text)

    #Get the longitude and the latitude of the ISS from request
    long = request["iss_position"]["longitude"]
    lat = request["iss_position"]["latitude"]

    # Access google to find the location using long and lat by reverse searching it
    g = geocoder.geocodefarm([lat, long], method='reverse')

    # Create the output to be returned: success, Lat, Long, state, country
    output = "Where is the ISS right now?\nRequest status: " + request["message"] + \
             "\n> Long:  " + request["iss_position"]["longitude"] + "\n> Lat: " \
             + request["iss_position"]["latitude"] + "\n> State: " + \
             str(g.state) + "\n> Country: " + str(g.country)
    return output

def get_objects_in_space():
    # Using an api, return the amount of objects in space
    response = requests.get("https://api.le-systeme-solaire.net/rest/knowncount/")
    request = json.loads(response.text)
    #print(len(request["knowncount"]))

    # prepare an output to return
    output = "What objects are in space right now?\nHere are the amounts and when " \
             "they were last updated:\n"

    # iterate through the list and place the data into the output
    for i in range(len(request["knowncount"])):
        output += "> - " + str(request["knowncount"][i]["knownCount"]) +  \
                  " " + request["knowncount"][i]["id"] + "(s) since: " + \
                  request["knowncount"][i]["updateDate"] + "\n"
    return output

@client.event
async def on_ready():
    print("{0.user} logging in".format(client))

@client.event
async def on_message(message):

    # Message has an author and the role may be altered at the end because of their response
    messageTag = False
    print("User {0.author}: {0.content}".format(message))

    # To have the "promoting roles" idea, we need to make sure that there are
    # the roles, so we will create them if they aren't there already
    for i in rank:
        color = 0xffffff
        if get(message.guild.roles, name=i):
            color = 0xffffff # it's already a role and thus doesn't need to be created again
        else:
            if(i == RANK1):
                color = 0x229954
            if(i == RANK2):
                color = 0x6495ED
            if(i == RANK3):
                color = 0xFF0800
            await message.guild.create_role(name=i, color=discord.Color(color),
                                            permissions = discord.Permissions(permissions))

    # We don't want the bot to talk to itself
    if message.author == client.user:
        return

    # if the user asks for the ISS location
    if message.content.startswith('$loc_iss') or \
            message.content.startswith("where is the iss"):
        response = get_location_iss()
        messageTag = True  # The user has asked a space question!
        await message.reply(response, mention_author=True)

    # if the user asks about the people in the ISS at the moment
    if message.content.startswith('$ppl_iss') or \
            message.content.startswith("who is on the iss"):
        response = get_people_on_iss()
        messageTag = True  # The user has asked a space question!
        await message.reply(response, mention_author=True)

    # if the user asks about the people in space (All of them)
    if message.content.startswith('$ppl_spc') or \
            message.content.startswith("who is in space"):
        response = get_people_in_space()
        messageTag = True  # The user has asked a space question!
        await message.reply(response, mention_author=True)

    # If the user wants to know about the different functions
    if message.content.startswith("$help"):
        response = help()
        await message.reply(response, mention_author=True)

    # if someone wants to know what objects are in space
    if message.content.startswith("$obj_spc") or \
            message.content.startswith("what objects are in space"):
        response = get_objects_in_space()
        messageTag = True  # The user has asked a space question!
        await message.reply(response, mention_author=True)

    # Turn off the bot
    if message.content.startswith("$stopTheBot"):
        print("Exit command recieved")
        await client.close()

        # If someone asks questions using the bot, they are given some extra roles and are promoted based on their
        # questions and how frequently they ask quesetions
    if messageTag == True:
        user = message.author
        if discord.utils.get(user.roles, name=RANK3):
            user = message.author  # Placeholder for now
        elif discord.utils.get(user.roles, name=RANK2):
            await user.add_roles(discord.utils.get(user.guild.roles, name=RANK3))
            await user.remove_roles(discord.utils.get(user.guild.roles, name=RANK2))
        elif discord.utils.get(user.roles, name=RANK1):
            await user.add_roles(discord.utils.get(user.guild.roles, name=RANK2))
            await user.remove_roles(discord.utils.get(user.guild.roles, name=RANK1))
        else:
            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=RANK1))
        messageTag = False

client.run(TOKEN)
