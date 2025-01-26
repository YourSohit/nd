import os
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Script(object):
    START_MESSAGE = os.environ.get("START_MESSAGE", """**Hello 👋\n\nI am a Notification Bot designed to provide you with the latest OTT serial and movie links as soon as they are released!**\n\n"""
        """📺 **Available OTTs:**\n🔥 [Hotstar](https://hotstar.com)\n💞 [Zee5](https://zee5.com)\n🎬 [JioCinema](https://www.jiocinema.com)\n📺 [SonyLIV](https://www.sonyliv.com)\n🎥 [SunNXT](https://www.sunnxt.com)\n✨ [DangalPlay](https://www.dangalplay.com)\n🎭 [ETVWin](https://www.etvwin.com)\n\n💳 **Subscribe for Premium Access** to receive instant notifications!""")

    HELP_MESSAGE = os.environ.get("HELP_MESSAGE", """**Need Help? 🤔**\n\n"""
        """This bot fetches the latest episode and movie links from the supported OTT platforms in real-time!\n\n"""
        """🔹 **Commands Available:**\n/start - Start the bot\n/help - Get this help message\n/myplan - Check your subscription\n/subscribe - Get premium access\n/latest - Get the newest episode links\n/search [show name] - Search for a specific show\n/feedback - Provide feedback\n/trending - View trending shows\n/request - Request a missing show\n/report - Report a broken link\n/settings - Customize bot preferences\n/contact - Contact Admin for support""")

    ABOUT_MESSAGE = os.environ.get("ABOUT_MESSAGE", """**About Me 🤖**\n\n"""
        """I am an OTT Notification Bot designed to keep you updated with the latest episodes and movies from various streaming platforms.\n\n"""
        """✨ **Supported OTTs:**\n🔥 Hotstar\n💞 Zee5\n🎬 JioCinema\n📺 SonyLIV\n🎥 SunNXT\n✨ DangalPlay\n🎭 ETVWin\n\n"""
        """🤝 **Developed by:** [YourAdmin](https://t.me/YourAdmin)""")

    SUBSCRIPTION_REMINDER_MESSAGE = """**Your subscription is about to expire soon.**\n\n"""
        """To continue receiving the latest notifications, please renew your subscription. Contact @YourAdmin:\n\n"""
        """📌 **User ID:** {user_id}\n"""
        """📅 **Subscription Date:** {subscription_date}\n"""
        """⏳ **Expiry Date:** {expiry_date}\n"""
        """🕒 **Remaining Period:** {time_remaining}\n"""
        """🚫 **Banned:** {banned_status}"""

    HELP_REPLY_MARKUP = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Help', callback_data='help_command'),
            InlineKeyboardButton('Language', callback_data='lang_command'),
        ],
        [
            InlineKeyboardButton('About', callback_data='about_command'),
            InlineKeyboardButton('My Plan', callback_data='info_command'),    
        ],
        [
            InlineKeyboardButton('Trending', callback_data='trending_command'),
            InlineKeyboardButton('Subscribe', url='https://t.me/YourAdmin'),
        ],
        [
            InlineKeyboardButton('Request Show', callback_data='request_command'),
            InlineKeyboardButton('Report Issue', callback_data='report_command'),
        ],
        [
            InlineKeyboardButton('Settings', callback_data='settings_command'),
            InlineKeyboardButton('Support', url='https://t.me/support_chat'),
        ],
        [
            InlineKeyboardButton('Contact Admin', url='https://t.me/YourAdmin'),
            InlineKeyboardButton('Close', callback_data='delete'),    
        ],
    ])

    HOME_BUTTON_MARKUP = InlineKeyboardMarkup([
        [InlineKeyboardButton('Home', callback_data='start_command')]
    ])
