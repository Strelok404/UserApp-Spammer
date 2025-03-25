import discord
from discord.ext import commands
from discord import app_commands
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import requests
from datetime import datetime
import ssl
import asyncio
import whois
import socket

TOKEN = "" # Put Your Token Bot
OPENCAGE_API_KEY = "" # Put The API KEY
IPINFO_API_KEY = "" # Put The API KEY

intents = discord.Intents.default()
intents.messages = True
intents.dm_messages = True

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

@bot.tree.command(name="dm_spammer", description="Send multiple DMs to a user")
async def dm_spammer(interaction: discord.Interaction, user: discord.User, message: str):
    """Send multiple DMs to a user (only with their permission)"""

    times = 15

    await interaction.response.defer(ephemeral=True)
    
    try:
        for _ in range(times):
            await user.send(message)
            await asyncio.sleep(0.30) 
        await interaction.followup.send(f"Successfully sent {times} direct messages to {user.name}!", ephemeral=True)
    except discord.Forbidden:
        await interaction.followup.send(f"I can't send direct messages to {user.name}. Make sure they haven't blocked me.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Error sending message: {str(e)}", ephemeral=True)

@bot.tree.command(name="url_info", description="Get basic information about a URL")
async def url_info(interaction: discord.Interaction, url: str):
    try:
        response = requests.get(url)
        content_length = len(response.content)
        content_type = response.headers.get("Content-Type", "Unknown")
        status_code = response.status_code
        
        embed = discord.Embed(title=f"Information about {url}", color=discord.Color.green())
        embed.add_field(name="🌍 Status Code", value=status_code, inline=False)
        embed.add_field(name="📄 Content Type", value=content_type, inline=False)
        embed.add_field(name="📏 Content Length", value=f"{content_length} bytes", inline=False)
        
        await interaction.response.send_message(embed=embed)
    except requests.RequestException as e:
        await interaction.response.send_message(f"❌ Error: {e}")

@bot.tree.command(name="trojan_spam", description="Spam of TrojanSquad")
async def fl00d_embed(interaction: discord.Interaction, message: str):
    image_url = "https://media.discordapp.net/attachments/1306126318806499388/1353455372504924170/Screenshot_2025_01_01-1.png?ex=67e1b70a&is=67e0658a&hm=1321d073229cb7dda800119ce169fc141e5665db1eac5fc2913c8458e84cc5ee&=&format=webp&quality=lossless&width=973&height=544"  
    await interaction.response.send_message("Flood de Trojan$quad inciado", ephemeral=True)
    for _ in range(5):
        embed = discord.Embed(title="⸸                Server Spammed By Trojan$quad                ⸸                                        #Trojan$quad𝐎n𝐓op", description=message, color=0x4B0082)
        embed.set_image(url=image_url)  
        await interaction.followup.send(content="[ ||@everyone|| ]\n https://discord.gg/czTRvRVpUE", embed=embed)

@bot.tree.command(name="fl00d", description="Send 5 messages in any server where the user has access")
async def fl00d(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("Flood iniciado", ephemeral=True)
    for _ in range(5):
        await interaction.followup.send(message)

def get_lat_long(country):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={country}&key={OPENCAGE_API_KEY}"
    response = requests.get(url).json()
    if response["results"]:
        lat = response["results"][0]["geometry"]["lat"]
        lng = response["results"][0]["geometry"]["lng"]
        return lat, lng
    return "Unknown", "Unknown"

@bot.tree.command(name="phonelookup", description="Find details about a phone number")
async def phonelookup(interaction: discord.Interaction, phone_number: str):
    try:
        num = phonenumbers.parse(phone_number, None)
        valid = phonenumbers.is_valid_number(num)
        formatted = phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        country = geocoder.description_for_number(num, "en")
        operator = carrier.name_for_number(num, "en")
        time_zones = timezone.time_zones_for_number(num)
        latitude, longitude = get_lat_long(country)
        
        embed = discord.Embed(title=f"Lookup for {phone_number}", color=discord.Color.dark_grey())
        embed.add_field(name="✅ Valid", value=str(valid), inline=False)
        embed.add_field(name="📞 Formatted Number", value=formatted, inline=False)
        embed.add_field(name="🌍 Country", value=country, inline=False)
        embed.add_field(name="📡 Operator", value=operator if operator else "Unknown", inline=False)
        embed.add_field(name="⏰ Timezone", value=", ".join(time_zones) if time_zones else "Unknown", inline=False)
        embed.add_field(name="🌍 Latitude", value=str(latitude), inline=False)
        embed.add_field(name="🌍 Longitude", value=str(longitude), inline=False)
        
        embed.set_footer(text=f"Requested by {interaction.user.display_name}")
        
        await interaction.response.send_message(embed=embed)
    except:
        await interaction.response.send_message("❌ Número inválido o no se pudo procesar.")

def get_ip_info(address):
    url = f"https://ipinfo.io/{address}/json?token={IPINFO_API_KEY}"
    response = requests.get(url).json()
    return response

@bot.tree.command(name="lookup", description="Find details about an IP or Domain")
async def lookup(interaction: discord.Interaction, address: str):
    try:
        data = get_ip_info(address)
        
        embed = discord.Embed(
            title=f"**Lookup for {address}**",
            description=f"**Command used by {interaction.user.display_name}**",
            color=discord.Color(0x2F3136)  
        )

        embed.add_field(name="🌍 **IP Address**", value=data.get('ip', 'N/A'), inline=False)
        embed.add_field(name="✅ **Status**", value="success", inline=False)
        embed.add_field(name="🇺🇸 **Country**", value=data.get('country', 'N/A'), inline=True)
        embed.add_field(name="🌍 **Country Code**", value=data.get('country', 'N/A'), inline=True)
        embed.add_field(name="🏙️ **City**", value=data.get('city', 'N/A'), inline=True)
        embed.add_field(name="🏞️ **Region**", value=data.get('region', 'N/A'), inline=True)
        embed.add_field(name="📍 **Zip Code**", value=data.get('postal', 'N/A'), inline=True)
        embed.add_field(name="🌐 **Latitude**", value=data.get('loc', 'N/A').split(',')[0], inline=True)
        embed.add_field(name="🌐 **Longitude**", value=data.get('loc', 'N/A').split(',')[1], inline=True)
        embed.add_field(name="🕒 **Timezone**", value=data.get('timezone', 'N/A'), inline=True)
        embed.add_field(name="💻 **ISP**", value=data.get('org', 'N/A'), inline=True)
        embed.add_field(name="🏢 **Organization**", value=data.get('org', 'N/A'), inline=True)
        embed.add_field(name="🔢 **AS Number**", value=data.get('asn', {}).get('asn', 'N/A'), inline=True)
        embed.add_field(name="📈 **AS Name**", value=data.get('asn', {}).get('name', 'N/A'), inline=True)
        embed.add_field(name="📱 **Mobile**", value="False", inline=True)
        embed.add_field(name="🔒 **Proxy**", value="False", inline=True)
        embed.add_field(name="🌐 **Hosting**", value="True", inline=True)

        embed.set_footer(text=f"Requested by {interaction.user.display_name} | Hoy a las {datetime.now().strftime('%H:%M')}")

        await interaction.response.send_message(embed=embed)
    
    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {str(e)}")



bot.run(TOKEN)
