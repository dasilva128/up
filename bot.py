# (c) @Savior_128

import os
import time
import asyncio
import aiohttp
from configs import Config
from pyrogram import Client, filters, errors
from core.display_progress import progress_for_pyrogram, humanbytes
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQueryResultArticle, \
    InputTextMessageContent, InlineQuery

Bot = Client(Config.SESSION_NAME, bot_token=Config.BOT_TOKEN, api_id=Config.API_ID, api_hash=Config.API_HASH)

# ... (بقیه کدها بدون تغییر باقی می‌مانند تا بخش آپلود)

@Bot.on_message(filters.private & filters.media)
async def _main(_, message):
    await message.reply_text(
        "Where do you want to upload?",
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Upload to GoFile.io", callback_data="uptogofile"),
                 InlineKeyboardButton("Upload to Streamtape", callback_data="uptostreamtape")],
                [InlineKeyboardButton("Upload to Pixeldrain", callback_data="uptopixeldrain")]  # دکمه جدید
            ]
        ),
        quote=True
    )

# ... (بقیه کدها بدون تغییر باقی می‌مانند تا بخش CallbackQuery)

@Bot.on_callback_query()
async def button(bot, data: CallbackQuery):
    cb_data = data.data
    if cb_data == "uptogofile":
        # کد موجود برای GoFile.io بدون تغییر
        pass
    elif cb_data == "uptostreamtape":
        # کد موجود برای Streamtape بدون تغییر
        pass
    elif cb_data == "uptopixeldrain":
        downloadit = data.message.reply_to_message
        a = await data.message.edit("Downloading to my Server ...", parse_mode=ParseMode.MARKDOWN,
                                    disable_web_page_preview=True)
        dl_loc = os.path.join(Config.DOWNLOAD_DIR, str(data.from_user.id))
        os.makedirs(dl_loc, exist_ok=True)
        c_time = time.time()
        the_media = await bot.download_media(
            message=downloadit,
            file_name=dl_loc,
            progress=progress_for_pyrogram,
            progress_args=("Downloading ...", a, c_time)
        )
        await a.delete(True)
        try:
            async with aiohttp.ClientSession() as session:
                files = {'file': open(the_media, 'rb')}
                headers = {'Authorization': f'Bearer {Config.PIXELDRAIN_API_KEY}'}
                response = await session.post("https://pixeldrain.com/api/file", data=files, headers=headers)
                data_f = await response.json()
                if response.status == 200 and data_f.get('success'):
                    file_id = data_f['id']
                    download_url = f"https://pixeldrain.com/u/{file_id}"
                    filename = os.path.basename(the_media)
                    await data.message.reply_to_message.reply_text(
                        f"**File Name:** `{filename}`\n\n**Download Link:** `{download_url}`",
                        parse_mode=ParseMode.MARKDOWN,
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("Open Link", url=download_url)]]
                        )
                    )
                    forwarded_msg = await data.message.reply_to_message.forward(Config.LOG_CHANNEL)
                    await bot.send_message(
                        chat_id=Config.LOG_CHANNEL,
                        text=f"#PIXELDRAIN_UPLOAD:\n\n[{data.from_user.first_name}](tg://user?id={data.from_user.id}) Uploaded to Pixeldrain !!\n\n**URL:** {download_url}",
                        reply_to_message_id=forwarded_msg.message_id,
                        parse_mode=ParseMode.MARKDOWN,
                        disable_web_page_preview=True
                    )
                else:
                    await data.message.reply_to_message.reply_text(
                        f"Failed to upload to Pixeldrain!\n\n**Error:** {data_f.get('message', 'Unknown error')}",
                        parse_mode=ParseMode.MARKDOWN,
                        disable_web_page_preview=True
                    )
                os.remove(the_media)
        except Exception as err:
            await data.message.reply_to_message.reply_text(
                f"Something went wrong!\n\n**Error:** `{err}`",
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
    elif cb_data == "deletestream":
        # کد موجود برای حذف فایل Streamtape
        pass
    elif cb_data == "showcreds":
        # کد موجود برای نمایش تنظیمات
        pass

Bot.run()