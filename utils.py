import asyncio
import logging
import traceback
import aiohttp
from pyrogram import Client
from config import OWNER_ID, PING_INTERVAL, REPLIT
from database.users import filter_users
from database import db
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helpers import temp
from slugify import slugify
import requests
from bs4 import BeautifulSoup

logging.getLogger().setLevel(logging.INFO)

async def ping_server():
    """Keeps the server alive by pinging it at intervals."""
    while True:
        await asyncio.sleep(PING_INTERVAL)
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(REPLIT) as resp:
                    logging.info(f"Pinged server with response: {resp.status}")
        except TimeoutError:
            logging.warning("Couldn't connect to the site URL..!")
        except Exception:
            traceback.print_exc()

async def notifier(client: Client):
    """Fetches and notifies users about new OTT releases."""
    while True:
        await asyncio.sleep(temp.SLEEP_TIME)
        try:
            tasks = [asyncio.ensure_future(sub_func(url, client)) for url in temp.NOTIFY_URLS]
            await asyncio.gather(*tasks)
        except Exception as e:
            logging.exception(e, exc_info=True)

async def sub_func(url, client):
    """Handles content fetching and notification sending."""
    image_url, msg, episode_url = "", "", ""
    changed_content = await fetch_link_data(url)

    if changed_content:
        title = changed_content['title']
        _url = episode_url = changed_content['url']
        image_url = changed_content.get('image_url', '')
        msg = f'**Title: {title}\nLink: {_url}**'
    
    if image_url and msg and episode_url:
        share_url = "https://telegram.me/share/url?url={}"
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Share', url=share_url.format(episode_url))]])
        if episode_url not in temp.DONE_URLS:
            await serial_broadcast(client, url, image_url, msg, reply_markup)
            temp.DONE_URLS.append(episode_url)

async def fetch_link_data(url):
    """Fetches link data from supported OTT platforms."""
    handlers = {
        "zee5.com": zee5_link_handler,
        "hotstar.com": hotstar_link_handler,
        "sunnxt.com": sunnxt_link_handler,
        "jiocinema.com": jiocinema_link_handler,
        "sonyliv.com": sonyliv_link_handler,
        "dangalplay.com": dangalplay_link_handler,
        "etvwin.com": etvwin_link_handler,
    }
    for domain, handler in handlers.items():
        if domain in url:
            return await handler(url)
    return None

async def serial_broadcast(client: Client, serial_url, image_url, caption, reply_markup=None):
    """Sends broadcast messages about new episodes to premium users."""
    users = await filter_users({"has_access": True, "banned": False})
    async for user in users:
        notify_url = await db.filter_notify_url({"api_url": serial_url})
        async for url in notify_url:
            if url["lang"] in user["allowed_languages"]:
                try:
                    await client.send_photo(user['user_id'], image_url, caption, reply_markup=reply_markup)
                except Exception as e:
                    logging.error(e)

async def get_response(url, headers=None):
    """Fetches JSON response from an OTT platform API."""
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, raise_for_status=True) as response:
            return await response.json()

async def get_soup(url):
    """Fetches and parses HTML response."""
    headers = {'User-Agent': 'Mozilla/5.0'}
    html_content = requests.get(url, headers=headers).content
    return BeautifulSoup(html_content, 'html.parser')

async def zee5_link_handler(url):
    """Handles Zee5 OTT platform link extraction."""
    response = await get_response(url)
    return {"title": response["title"], "url": response["url"], "image_url": response["image"]}

async def hotstar_link_handler(url):
    """Handles Hotstar OTT platform link extraction."""
    response = await get_response(url)
    return {"title": response["title"], "url": response["url"], "image_url": response["image"]}

async def sunnxt_link_handler(url):
    """Handles SunNXT OTT platform link extraction."""
    response = await get_response(url)
    return {"title": response["title"], "url": response["url"], "image_url": response["image"]}

async def jiocinema_link_handler(url):
    """Handles JioCinema OTT platform link extraction."""
    response = await get_response(url)
    return {"title": response["title"], "url": response["url"], "image_url": response["image"]}

async def sonyliv_link_handler(url):
    """Handles SonyLIV OTT platform link extraction."""
    response = await get_response(url)
    return {"title": response["title"], "url": response["url"], "image_url": response["image"]}

async def dangalplay_link_handler(url):
    """Handles DangalPlay OTT platform link extraction."""
    response = await get_response(url)
    return {"title": response["title"], "url": response["url"], "image_url": response["image"]}

async def etvwin_link_handler(url):
    """Handles ETVWin OTT platform link extraction."""
    response = await get_response(url)
    return {"title": response["title"], "url": response["url"], "image_url": response["image"]}
