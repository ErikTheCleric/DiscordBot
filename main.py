# Erik Hale 7/1/2021
# Discord Bot code for: StarGazer
import asyncio

import discord
import requests
import json
import geocoder
import random
import asyncio

TOKEN = "ODYwMDE3NzMxNDY5MzEyMDEw.YN1H7Q.MFnobGAQHpwfFwxz8tV1O5pw9_Y"
client = discord.Client(); # This is the connection to discord

def get_quote():
    response = requests.get ("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

def get_location_iss():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    request = json.loads(response.text)

    # Get the longitude and the latitude of the ISS
    long = request["iss_position"]["longitude"]
    lat = request["iss_position"]["latitude"]

    # Access google to find the location using long and lat
    g = geocoder.geocodefarm([lat, long], method='reverse')
    print("Yes its this one: " + str(g.city))

    # Create the output to be returned: success, Lat, Long, state, country
    output = "Where is the ISS right now?\nRequest status: " + request["message"] + \
             "\n> Long:  " + request["iss_position"]["longitude"] + "\n> Lat: " \
             + request["iss_position"]["latitude"] + "\n> State: " + \
             str(g.state) + "\n> Country: " + str(g.country)
    return output

@client.event
async def on_ready():
    print("We have logged user in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('testbot?'):
        await message.channel.send('Hello!')

    if message.content.startswith("$inspire"):
        quote = get_quote()
        await message.channel.send(quote)

    if message.content.startswith('whats the best videogame?'):
        await message.channel.send('ZERORANGER!!!')

    if message.content.startswith('$iss_loc'):
        response = get_location_iss()
        await message.channel.send(response)

    if message.content.startswith('!hello'):
        await message.reply("Hello!", mention_author=True)

client.run(TOKEN)