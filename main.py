import asyncio
import datetime
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from motor.motor_asyncio import AsyncIOMotorClient
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, DATABASE_URL, DATABASE_NAME

logging.basicConfig(level=logging.INFO)

bot = Client("OTTNotifier", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

db_client = AsyncIOMotorClient(DATABASE_URL)
db = db_client[DATABASE_NAME]
users_collection = db["users"]
subscriptions_collection = db["subscriptions"]

otts = ["zee5.com", "hotstar.com", "sunnxt.com", "jiocinema.com", "dangalplay.com", "sonyliv.com", "etvwin.com", "amazonprime.com", "netflix.com"]
languages = ["English", "Hindi", "Bengali", "Tamil", "Telugu", "Kannada", "Malayalam"]

@bot.on_message(filters.command("start"))
async def start(client, message):
    user = await users_collection.find_one({"user_id": message.from_user.id})
    if not user:
        await users_collection.insert_one({"user_id": message.from_user.id, "premium": False, "otts": [], "language": "English"})
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("About", callback_data="about"), InlineKeyboardButton("Help", callback_data="help")],
        [InlineKeyboardButton("Plans", callback_data="plans"), InlineKeyboardButton("My Plan", callback_data="myplan")],
        [InlineKeyboardButton("Latest Episodes", callback_data="latest"), InlineKeyboardButton("Search Show", callback_data="search")],
        [InlineKeyboardButton("OTTs", callback_data="select_ott"), InlineKeyboardButton("Language", callback_data="select_language")],
        [InlineKeyboardButton("Support", url="https://t.me/support_bot"), InlineKeyboardButton("Feedback", callback_data="feedback")],
        [InlineKeyboardButton("Contact Admin", url="https://t.me/admin_contact"), InlineKeyboardButton("Referral Program", callback_data="referral")]
    ])
    
    await message.reply_text(
        "**Welcome to OTT Notification Bot! 🎬**\n\n"
        "Stay updated with the latest episodes & movies from your favorite OTT platforms.\n"
        "Use the buttons below to navigate.",
        reply_markup=keyboard
    )

@bot.on_message(filters.command("subscribe"))
async def subscribe(client, message):
    await message.reply("To subscribe, please visit: https://t.me/admin_contact")

@bot.on_message(filters.command("referral"))
async def referral(client, message):
    await message.reply(f"Invite friends and get rewards! Your referral link: https://t.me/your_bot?start={message.from_user.id}")

@bot.on_message(filters.command("download"))
async def download(client, message):
    await message.reply("Downloading feature coming soon! Stay tuned.")

@bot.on_message(filters.command("trending"))
async def trending(client, message):
    await message.reply("Trending shows will be displayed here soon! Stay tuned.")

@bot.on_callback_query()
async def handle_callback(client, callback_query: CallbackQuery):
    data = callback_query.data
    if data == "about":
        await callback_query.message.edit_text("This is an OTT notification bot that helps users stay updated with the latest releases on selected platforms.",
                                               reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start")]]))
    elif data == "help":
        await callback_query.message.edit_text("Use the commands and buttons to navigate and get notifications.",
                                               reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start")]]))
    elif data == "plans":
        await callback_query.message.edit_text("Choose a plan to subscribe to premium services.",
                                               reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start")]]))
    elif data == "latest":
        await callback_query.message.edit_text("Fetching latest episode links... (Feature in development)",
                                               reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start")]]))
    elif data == "search":
        await callback_query.message.edit_text("Search for a show using: `/search [show name]` (Feature in development)",
                                               reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start")]]))
    elif data == "trending":
        await callback_query.message.edit_text("Trending shows will be displayed here soon!", 
                                               reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start")]]))
    elif data == "myplan":
        user = await users_collection.find_one({"user_id": callback_query.from_user.id})
        if user and user.get("premium"):
            expiry = user.get("expiry", "N/A")
            await callback_query.message.edit_text(f"Your premium subscription is active until: {expiry}",
                                                   reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start")]]))
        else:
            await callback_query.message.edit_text("You are not a premium user.",
                                                   reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start")]]))

async def main():
    await bot.start()
    logging.info("Bot is running!")
    await asyncio.sleep(float("inf"))

if __name__ == "__main__":
    asyncio.run(main())
