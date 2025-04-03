import discord
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from discord import app_commands
from discord.ext import commands
import urllib.parse
from colorthief import ColorThief
import requests
from io import BytesIO
from datetime import datetime

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

class AlbumSubmissionModal(discord.ui.Modal, title='Album Submission'):
    spotify_link = discord.ui.TextInput(
        label="Spotify Album Link",
        placeholder="https://open.spotify.com/album/...",
    )
    
    submission_reason = discord.ui.TextInput(
        label="Notes",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=500
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True)
            
            # Validate Spotify link
            if "open.spotify.com/album/" not in self.spotify_link.value.lower():
                return await interaction.followup.send(" Invalid Spotify album link", ephemeral=True)
            
            # Extract album ID
            album_id = urllib.parse.urlparse(self.spotify_link.value).path.split('/')[-1]
            
            try:
                # Fetch album data (including all tracks via pagination)
                album_data = sp.album(album_id)
                total_tracks = album_data['tracks']['total']                
            except Exception as e:
                return await interaction.followup.send(f" Spotify API error: {str(e)}", ephemeral=True)

            def get_dominant_color(image_url):
                response = requests.get(image_url)
                img = BytesIO(response.content)
                color_thief = ColorThief(img)
                dominant_color = color_thief.get_color(quality=1)  # (R, G, B)
                return int(f"0x{dominant_color[0]:02x}{dominant_color[1]:02x}{dominant_color[2]:02x}", 16)
            
            if album_data['images']:
                embed_color = get_dominant_color(album_data['images'][0]['url'])

            embed = discord.Embed(
                title=album_data['name'],
                color=embed_color,
                url=self.spotify_link.value
            )

            release_date = album_data['release_date']
            try:
                if len(release_date) == 4:
                    formatted_date = release_date
                else:
                    date_obj = datetime.strptime(release_date, "%Y-%m-%d" if "-" in release_date else "%Y")
                    formatted_date = date_obj.strftime("%d/%m/%Y")
            except:
                formatted_date = release_date
            
            artists = ", ".join([artist['name'] for artist in album_data['artists']])
            embed.add_field(name="👤  Artist(s)", value=artists, inline=False)
            
            embed.add_field(
                name="💿  Album Info",
                value=f"Released {formatted_date} ∙ {total_tracks} tracks",
                inline=False
            )
            
            embed.add_field(name="📝  Notes", value=self.submission_reason.value, inline=False)
            embed.add_field(name=" ", value=" ", inline=False)
            
            if album_data['images']:
                embed.set_thumbnail(url=album_data['images'][0]['url'])
            embed.set_footer(text=f"Submitted by {interaction.user.display_name}")
            
            message = await interaction.followup.send(embed=embed)
            for emoji in ["⭐"]:
                await message.add_reaction(emoji)
            
        except Exception as e:
            print(f"Error: {e}")
            await interaction.followup.send(" An error occurred", ephemeral=True)

class addalbum(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="addalbum",
        description="Recommend an album for the server to listen to"
    )
    async def addalbum(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AlbumSubmissionModal())

async def setup(bot):
    await bot.add_cog(addalbum(bot))