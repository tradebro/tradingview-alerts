from os import environ
from tradingviewalerts.forwarders.base import BaseForwarder
from string import Template
from sanic.log import logger
import telepot

# Telegram Forwarder Env Vars
TELEGRAM_TOKEN = environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = environ.get('TELEGRAM_CHAT_ID')

TEMPLATE = '''<b>TradingView Alerts</b>

New alert has come, details below.

Action: <b>$action</b>

Pair: $pair
Exchange: $exchange
Last Price: $close

Indicator: $indicator

Written with 💚 by contributors
<a href="https://github.com/tistaharahap/tradingview-alerts">TradingView Alerts</a>'''


class TelegramForwarder(BaseForwarder):
    async def send_message(self, message: str):
        if not TELEGRAM_TOKEN:
            logger.error('Required env var TELEGRAM_TOKEN must be set')
            return
        if not TELEGRAM_CHAT_ID:
            logger.error('Required env var TELEGRAM_CHAT_ID must be set')
            return

        bot = telepot.Bot(token=TELEGRAM_TOKEN)

        bot.sendMessage(chat_id=TELEGRAM_CHAT_ID,
                        text=message,
                        parse_mode='HTML')

    async def send_notification(self, message: dict):
        if not TelegramForwarder.is_valid_message(message=message):
            logger.error('Not a valid alert message')
            return

        template = Template(TEMPLATE)
        message_html = template.substitute(message)

        await self.send_message(message=message_html)
