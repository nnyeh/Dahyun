import os
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
from bs4 import BeautifulSoup
import json

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

class MediaSubmissionModal(discord.ui.Modal, title='Media Submission'):
    link = discord.ui.TextInput(
        label="Link",
        placeholder="Spotify album or IMDb/TMDB title URL",
        required=True
    )

    submission_reason = discord.ui.TextInput(
        label="Notes",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=500
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            url_value = (self.link.value or "").strip()
            lower_url = url_value.lower()
            is_spotify_album = ("open.spotify.com/album/" in lower_url) or lower_url.startswith("spotify:album:")
            imdb_id = None
            try:
                import re
                m = re.search(r"(tt\d+)", lower_url)
                if m:
                    imdb_id = m.group(1)
            except Exception:
                imdb_id = None

            def get_dominant_color(image_url: str, default: int = 0x4A5FC3) -> int:
                try:
                    response = requests.get(image_url, timeout=10)
                    response.raise_for_status()
                    img = BytesIO(response.content)
                    color_thief = ColorThief(img)
                    r, g, b = color_thief.get_color(quality=1)
                    return int(f"0x{r:02x}{g:02x}{b:02x}", 16)
                except Exception:
                    return default

            def minutes_to_hm(total_minutes: int) -> str:
                try:
                    total_minutes = int(total_minutes)
                    h = total_minutes // 60
                    m = total_minutes % 60
                    return f"{h}h {m}m"
                except Exception:
                    return None

            def parse_omdb_runtime(runtime_str: str) -> str:
                try:
                    if not runtime_str or runtime_str == 'N/A':
                        return None
                    num = ''.join(ch for ch in runtime_str if ch.isdigit())
                    if not num:
                        return None
                    return minutes_to_hm(int(num))
                except Exception:
                    return None

            if is_spotify_album:

                if lower_url.startswith("spotify:album:"):
                    album_id = url_value.split(":")[-1]
                else:
                    album_id = urllib.parse.urlparse(url_value).path.split('/')[-1]
                try:
                    album_data = sp.album(album_id)
                    total_tracks = album_data['tracks']['total']
                except Exception as e:
                    return await interaction.followup.send(f" Spotify API error: {str(e)}")

                embed_color = 0x4A5FC3
                if album_data.get('images'):
                    embed_color = get_dominant_color(album_data['images'][0]['url'], default=embed_color)

                embed = discord.Embed(
                    title=album_data['name'],
                    color=embed_color,
                    url=url_value
                )

                release_date = album_data.get('release_date', '')
                try:
                    if len(release_date) == 4:
                        formatted_date = release_date
                    else:
                        date_obj = datetime.strptime(release_date, "%Y-%m-%d" if "-" in release_date else "%Y")
                        formatted_date = date_obj.strftime("%d/%m/%Y")
                except Exception:
                    formatted_date = release_date

                artists = ", ".join([artist['name'] for artist in album_data.get('artists', [])]) or "Unknown"
                embed.add_field(name="👤  Artist(s)", value=artists, inline=False)
                embed.add_field(name="💿  Album Info", value=f"Released {formatted_date} ∙ {total_tracks} tracks", inline=False)
                try:
                    tracks_obj = album_data.get('tracks') or {}
                    items = tracks_obj.get('items') or []
                    lines = []
                    for t in items:
                        tname = (t.get('name') or '').strip() or 'Unknown track'
                        lines.append(tname)
                        if len("\n".join(lines)) > 950:
                            lines.pop()
                            break
                    added = len(lines)
                    if total_tracks and isinstance(total_tracks, int) and total_tracks > added:
                        lines.append(f"… +{total_tracks - added} more")
                    if lines:
                        embed.add_field(name="🎵  Tracks", value="\n".join(lines), inline=False)
                except Exception:
                    pass
                embed.add_field(name="📝  Notes", value=self.submission_reason.value, inline=False)
                embed.add_field(name=" ", value=" ", inline=False)

                if album_data.get('images'):
                    embed.set_thumbnail(url=album_data['images'][0]['url'])
                embed.set_footer(text=f"Submitted by {interaction.user.display_name}")

                message = await interaction.followup.send(embed=embed)
                for emoji in ["⭐"]:
                    try:
                        await message.add_reaction(emoji)
                    except Exception:
                        pass
                return

            tmdb_key = os.getenv("TMDB_API_KEY")
            poster_url = None
            title = None
            year = None
            plot = None
            rating = None
            genre = None
            runtime = None
            director = None
            actors = None
            total_seasons = None
            rating_source = None
            tmdb_error = None
            data = None
            tmdb_media_type = None  # 'movie' or 'tv'
            tmdb_id = None

            if tmdb_key and imdb_id:
                try:
                    params = {
                        'api_key': tmdb_key,
                        'external_source': 'imdb_id'
                    }
                    resp = requests.get(f'https://api.themoviedb.org/3/find/{imdb_id}', params=params, timeout=10)
                    data = resp.json()
                    movie_results = data.get('movie_results') or []
                    tv_results = data.get('tv_results') or []
                    if movie_results:
                        tmdb_media_type = 'movie'
                        tmdb_id = movie_results[0].get('id')
                    elif tv_results:
                        tmdb_media_type = 'tv'
                        tmdb_id = tv_results[0].get('id')
                    else:
                        tmdb_error = 'Not found on TMDb via IMDb id'
                except Exception:
                    tmdb_error = 'Failed to contact TMDb (find)'

            if not tmdb_id and tmdb_key and ('themoviedb.org/movie/' in lower_url or 'themoviedb.org/tv/' in lower_url):
                try:
                    import re
                    path = urllib.parse.urlparse(url_value).path
                    m = re.search(r"/(movie|tv)/(\d+)", path)
                    if m:
                        tmdb_media_type = 'movie' if m.group(1) == 'movie' else 'tv'
                        tmdb_id = int(m.group(2))
                except Exception:
                    pass

            details = None
            credits = None
            if tmdb_key and tmdb_id and tmdb_media_type in ('movie', 'tv'):
                try:
                    params = {'api_key': tmdb_key, 'append_to_response': 'credits'}
                    if tmdb_media_type == 'movie':
                        r = requests.get(f'https://api.themoviedb.org/3/movie/{tmdb_id}', params=params, timeout=10)
                    else:
                        r = requests.get(f'https://api.themoviedb.org/3/tv/{tmdb_id}', params=params, timeout=10)
                    details = r.json()
                    credits = details.get('credits') or {}

                    if tmdb_media_type == 'movie':
                        title = title or details.get('title') or details.get('original_title')
                        rd = details.get('release_date') or ''
                        if rd and not year:
                            year = rd.split('-')[0]
                        plot = plot or details.get('overview')
                        if not rating and details.get('vote_average') is not None:
                            rating = f"{details['vote_average']:.1f}"
                            rating_source = 'TMDb'
                        gs = details.get('genres') or []
                        if gs and not genre:
                            genre = ", ".join([g['name'] for g in gs if g.get('name')])
                        if not runtime and isinstance(details.get('runtime'), int):
                            runtime = minutes_to_hm(details['runtime'])
                        crew = (credits.get('crew') or [])
                        directors = [c['name'] for c in crew if c.get('job') == 'Director' and c.get('name')]
                        if directors:
                            director = ", ".join(directors)
                        cast = (credits.get('cast') or [])
                        if cast:
                            actors = ", ".join([c['name'] for c in cast[:5] if c.get('name')])
                    else:
                        title = title or details.get('name') or details.get('original_name')
                        fad = details.get('first_air_date') or ''
                        if fad and not year:
                            year = fad.split('-')[0]
                        plot = plot or details.get('overview')
                        if not rating and details.get('vote_average') is not None:
                            rating = f"{details['vote_average']:.1f}"
                            rating_source = 'TMDb'
                        gs = details.get('genres') or []
                        if gs and not genre:
                            genre = ", ".join([g['name'] for g in gs if g.get('name')])
                        ert = details.get('episode_run_time') or []
                        if not runtime and isinstance(ert, list) and ert:
                            runtime = minutes_to_hm(ert[0])
                        creators = details.get('created_by') or []
                        if creators and not director:
                            director = ", ".join([c['name'] for c in creators if c.get('name')])
                        cast = (credits.get('cast') or [])
                        if cast:
                            actors = ", ".join([c['name'] for c in cast[:5] if c.get('name')])
                        total_seasons = details.get('number_of_seasons') or total_seasons

                    if not poster_url:
                        pp = details.get('poster_path')
                        bp = details.get('backdrop_path')
                        if pp:
                            poster_url = f"https://image.tmdb.org/t/p/w500{pp}"
                        elif bp:
                            poster_url = f"https://image.tmdb.org/t/p/w500{bp}"
                except Exception:
                    tmdb_error = 'Failed to contact TMDb (details)'
                    omdb_error = 'Failed to contact OMDb'

            if (not tmdb_id or not details) and 'imdb.com/title/' in lower_url:
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
                    }
                    html_resp = requests.get(url_value, headers=headers, timeout=10)
                    html_resp.raise_for_status()
                    soup = BeautifulSoup(html_resp.text, 'html.parser')
                    ld_json = None
                    for script in soup.find_all('script', type='application/ld+json'):
                        try:
                            obj = json.loads(script.string or '{}')
                            if isinstance(obj, list) and obj:
                                obj = obj[0]
                            if isinstance(obj, dict) and obj.get('@type') in ('Movie', 'TVSeries', 'TVEpisode'):
                                ld_json = obj
                                break
                        except Exception:
                            continue

                    def iso8601_to_text(dur: str) -> str:
                        try:
                            if not isinstance(dur, str) or not dur.startswith('PT'):
                                return None
                            h = m = 0
                            import re
                            mh = re.search(r"(\d+)H", dur)
                            mm = re.search(r"(\d+)M", dur)
                            if mh:
                                h = int(mh.group(1))
                            if mm:
                                m = int(mm.group(1))
                            return f"{h}h {m}m"
                        except Exception:
                            return None

                    if ld_json:
                        title = title or ld_json.get('name')
                        date_published = ld_json.get('datePublished')
                        if date_published and not year:
                            year = date_published.split('-')[0]
                        plot = plot or ld_json.get('description')
                        agg = ld_json.get('aggregateRating') or {}
                        if not rating and agg.get('ratingValue'):
                            rating = str(agg.get('ratingValue'))
                            rating_source = 'IMDb'
                        g = ld_json.get('genre')
                        if g and not genre:
                            if isinstance(g, list):
                                genre = ", ".join(g)
                            else:
                                genre = str(g)
                        dur = ld_json.get('duration')
                        if dur and not runtime:
                            runtime = iso8601_to_text(dur) or runtime
                        if not director:
                            d = ld_json.get('director')
                            if isinstance(d, list):
                                director = ", ".join([p.get('name') for p in d if isinstance(p, dict) and p.get('name')])
                            elif isinstance(d, dict):
                                director = d.get('name')
                        if not actors:
                            a = ld_json.get('actor')
                            if isinstance(a, list):
                                actors = ", ".join([p.get('name') for p in a if isinstance(p, dict) and p.get('name')])
                            elif isinstance(a, dict):
                                actors = a.get('name')
                        ld_type = ld_json.get('@type')
                        if ld_type == 'Movie':
                            omdb_type = 'movie'
                        elif ld_type in ('TVSeries', 'TVEpisode'):
                            omdb_type = 'series'
                        if not poster_url:
                            img = ld_json.get('image')
                            if isinstance(img, str):
                                poster_url = img
                            elif isinstance(img, dict):
                                poster_url = img.get('url')

                    if not title:
                        og_title = soup.find('meta', property='og:title')
                        if og_title and og_title.get('content'):
                            title = og_title['content']
                    if not poster_url:
                        og_img = soup.find('meta', property='og:image')
                        if og_img and og_img.get('content'):
                            poster_url = og_img['content']
                except Exception:
                    pass

            embed_color = 0x4A5FC3
            if poster_url:
                embed_color = get_dominant_color(poster_url, default=embed_color)

            omdb_type = omdb_type if 'omdb_type' in locals() else ''
            if not omdb_type:
                if tmdb_media_type == 'movie':
                    omdb_type = 'movie'
                elif tmdb_media_type == 'tv':
                    omdb_type = 'series'
            if omdb_type == 'movie':
                inferred_type = 'film'
            elif omdb_type in ('series', 'tv', 'episode'):
                inferred_type = 'show'
            else:
                inferred_type = 'film' if 'imdb.com/title/' in lower_url else 'media'

            title_text = title or ("Film" if inferred_type == "film" else ("Show" if inferred_type == "show" else "Media"))
            embed = discord.Embed(
                title=title_text,
                url=url_value,
                color=embed_color
            )

            if inferred_type == "film":
                if year or runtime:
                    embed.add_field(name="🎬  Details", value=" ∙ ".join([v for v in [year, runtime] if v]), inline=False)
                if director and director != 'N/A':
                    embed.add_field(name="🎞️  Director", value=director, inline=True)
                if actors and actors != 'N/A':
                    embed.add_field(name="👥  Cast", value=actors, inline=False)
            elif inferred_type == "show":  # show
                if year or total_seasons:
                    seasons_txt = f"{total_seasons} season(s)" if total_seasons and total_seasons != 'N/A' else None
                    embed.add_field(name="📺  Details", value=" ∙ ".join([v for v in [year, seasons_txt] if v]), inline=False)
                if actors and actors != 'N/A':
                    embed.add_field(name="👥  Cast", value=actors, inline=False)

            if genre and genre != 'N/A':
                embed.add_field(name="🏷️  Genre", value=genre, inline=True)
            if rating and rating != 'N/A':
                label = f"⭐  {rating_source}" if rating_source else "⭐  Rating"
                embed.add_field(name=label, value=rating, inline=True)
            if plot and plot != 'N/A':
                embed.add_field(name="📝  Summary", value=plot, inline=False)
            if (imdb_id or ('themoviedb.org' in lower_url)) and tmdb_error:
                embed.add_field(name="ℹ️  Metadata", value=f"TMDb: {tmdb_error}", inline=False)

            embed.add_field(name="📝  Notes", value=self.submission_reason.value, inline=False)
            embed.add_field(name=" ", value=" ", inline=False)

            if poster_url:
                embed.set_thumbnail(url=poster_url)
            embed.set_footer(text=f"Submitted by {interaction.user.display_name}")

            message = await interaction.followup.send(embed=embed)
            for emoji in ["⭐"]:
                try:
                    await message.add_reaction(emoji)
                except Exception:
                    pass
            return

        except Exception as e:
            print(f"Error: {e}")
            try:
                await interaction.followup.send(" An error occurred")
            except Exception:
                pass

class addmedia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="addmedia",
        description="Recommend media for the server"
    )
    async def addmedia(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_modal(MediaSubmissionModal())
        except Exception as e:
            try:
                await interaction.response.send_message(" Couldn't open the submission form. Please try again in a moment.", ephemeral=True)
            except Exception:
                pass

async def setup(bot):
    await bot.add_cog(addmedia(bot))