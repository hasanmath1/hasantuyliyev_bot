from aiogram import types
from aiogram.handlers import CancelHandler
from aiogram.dispatcher.middlewares import Middleware

from src.loader import bot
from src.config import Config
from src.utils.misc import subscription


class BigBrother(manager.MiddlewareManager):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user.id
            if update.message.text in ['/start', '/help']:
                return
        elif update.callback_query:
            user = update.callback_query.from_user.id
            if update.callback_query.data == "check_subs":
                return
        else:
            return

        result = "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:\n"
        final_status = True
        for channel in Config:
            status = await subscription.check(user_id=user,
                                              channel=channel)
            final_status *= status
            channel = await bot.get_chat(channel)
            if not status:
                invite_link = await channel.export_invite_link()
                result += (f"👉 <a href='{invite_link}'>{channel.title}</a>\n")

        if not final_status:
            await update.message.answer(result, disable_web_page_preview=True)
            raise CancelHandler()
