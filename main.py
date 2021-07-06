# Erik Hale 7/1/2021
# Discord Bot code for: StarGazer

import discord
import requests
import json
import geocoder
import random

TOKEN = {Your token here}
NAME_OF_BOT = "StarGazer"

def help():
    # a help function that returns the different functions that the bot can do
    output = "Hello, i'm " + NAME_OF_BOT + ", here is what I can do for you:\n" + \
             "> \'$iss_loc\' to get the location of the ISS\n" \
             "> \'$iss_ast\' to get the astronauts on the ISS\n" \
             "> \'$ppl_spc\' to get the total amount of people in space\n" \
             "> \'!role (#1)d(#2)\' to get #1 many roles of die with #2 sides"
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

    return

def role_num(message):
    # Role a die sent in by the user
    print(message)
    # Take out the command from the response and just leave the die role
    request = message[6:]
    print(request)

    # Split the die role into the amount of die you are rolling and the amount of sides
    # for each die, randomly
    print(request.split("d")[0] + " " + request.split("d")[1])
    numOfDie = int(request.split("d")[0])
    numOfSides = int(request.split("d")[1])

    # Display output
    total = 0
    output = "You rolled...\n"

    # if there are no sides or no dice to role then the value is zero
    if numOfDie == 0 or numOfSides == 0:
        output += "0"
        return output

    # If there is only 1 die then make the response look nicer
    if numOfDie == 1:
        output += str(random.randint(1, int(numOfSides)))
        return output

    # if the num of dice are more than 1
    for n in range(int(numOfDie)):
        role = random.randint(1, int(numOfSides))
        output += str(role)
        total += role
        if n != int(numOfDie) - 1:
            output += " + " # Add a plus sign to show each role

    output += " = " + str(total)
    return output

class MyClient(discord.Client):

    async def on_ready(self):
        print("Logged on as {0}".format(self.user))

    async def on_message(self, message):
        print("User {0.author}: {0.content}".format(message))

        # This is so that no matter the input sent by the user (even with camel case)
        # would still register and StarGazer would return a response
        message.content = message.content.lower()

        # We don't want the bot to repeat itself or reply to itself
        if message.author.id == self.user.id:
            return

        # if the user asks for the ISS location
        if message.content.startswith('$iss_loc') or \
                message.content.startswith("where is the iss"):
            response = get_location_iss()
            await message.reply(response, mention_author = True)

        if message.content.startswith('$iss_ast') or \
                message.content.startswith("who is on the iss"):
            response = get_people_on_iss()
            await message.reply(response, mention_author = True)

        if message.content.startswith('$ppl_spc') or \
                message.content.startswith("who is in space"):
            response = get_people_in_space()
            await message.reply(response, mention_author = True)

        if message.content.startswith("!role"):
            response = role_num(message.content)
            await message.reply(response, mention_author = True)

        if message.content.startswith("$help"):
            response = help()
            await message.reply(response, mention_author = True)

        if message.content.startswith("givemearole"):
            user = message.author
            role = discord.utils.get(user.guild.roles, name = "Space Enthusiast")
            await user.add_roles(role)

client = MyClient()
client.run(TOKEN)
