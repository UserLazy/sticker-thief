import logging

# noinspection PyUnresolvedReferences,PyPackageRequirements
import os

# noinspection PyUnresolvedReferences,PyPackageRequirements
from telegram import ParseMode
from telegram.ext import ExtBot, Defaults
from telegram.utils.request import Request

from .utils import utils
from .utils.pyrogram import Client
from .database import base
from .bot import StickersBot
from config import config

logger = logging.getLogger(__name__)

stickersbot = StickersBot(
    bot=ExtBot(
        token=config.telegram.token,
        defaults=Defaults(parse_mode=ParseMode.HTML, disable_web_page_preview=True),
        # https://github.com/python-telegram-bot/python-telegram-bot/blob/8531a7a40c322e3b06eb943325e819b37ee542e7/telegram/ext/updater.py#L267
        request=Request(con_pool_size=config.telegram.get('workers', 1) + 4)
    ),
    use_context=True,
    workers=config.telegram.get('workers', 1),
    persistence=utils.persistence_object(config_enabled=config.telegram.get('persistent_temp_data', True)),
)


def main():
    utils.load_logging_config('logging.json')

    if config.pyrogram.enabled:
        logger.info('starting pyrogram client...')
        client.start()

    stickersbot.import_handlers(r'bot/handlers/')
    stickersbot.run(drop_pending_updates=True)


if __name__ == '__main__':
    main()
