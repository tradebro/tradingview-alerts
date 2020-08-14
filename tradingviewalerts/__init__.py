from sanic import Sanic
from sanic.request import Request
from sanic.response import text
from os import environ
from tradingviewalerts.forwarders.base import BaseForwarder
from tradingviewalerts.forwarders.telegram import TelegramForwarder

# Valid options are ['telegram'] - More coming soon
FORWARDER = environ.get('FORWARDER', 'telegram')


def get_forwarder(fwd: str) -> BaseForwarder:
    forwarders = {
        'telegram': TelegramForwarder
    }

    forwarder = forwarders.get(fwd)

    return forwarder()


async def webhook_handler(request: Request):
    forwarder = get_forwarder(FORWARDER)

    await forwarder.send_notification(message=request.json)

    return text('ok')


def create_app():
    app = Sanic('TradingView Alerts')

    app.add_route(webhook_handler, '/webhook', methods=['POST'])

    return app

