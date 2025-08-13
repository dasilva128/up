# (c) @Savior_128

import os
import time
import asyncio
from configs import Config
from pyrogram import Client, filters, errors
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQueryResultArticle, \
    InputTextMessageContent, InlineQuery
from pyrogram.enums import ParseMode
from core.display_progress import progress_for_pyrogram, humanbytes

Bot = Client(Config.SESSION_NAME, bot_token=Config.BOT_TOKEN, api_id=Config.API_ID, api_hash=Config.API_HASH)


@Bot.on_message(filters.command("start"))
async def start_handler(_, cmd):
    await cmd.reply_text(
        "HI, I am Cloud Uploads Manager Bot!\n\nSend me any media file, and I will upload it to Telegram and provide a download link.\n\nCheck > /help < for more info.",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Developer", url="https://t.me/Savior_128"),
                 InlineKeyboardButton("Support Group", url="https://t.me/linux_repo")],
                [InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")],
                [InlineKeyboardButton("Bot's Source Code", url="https://github.com/Savior_128/Cloud-UPManager-Bot")]
            ]
        )
    )


@Bot.on_message(filters.command("help"))
async def help_handler(_, cmd):
    await cmd.reply_text(
        """
Send me any media file, and I will upload it to Telegram and provide a download link.

**Commands:**
- `/start`: Start the bot
- `/help`: Show this help message

**Note**: The maximum file size is 2GB (4GB for premium accounts). Files are stored in Telegram and can be accessed via the provided link.
""",
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Support Group", url="https://t.me/linux_repo"),
                 InlineKeyboardButton("Developer", url="https://t.me/Savior_128")]
            ]
        )
    )


@Bot.on_message(filters.private & filters.media)
async def upload_to_telegram(_, message):
    await message.reply_text(
        "Uploading your file to Telegram...",
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        quote=True
    )
    try:
        # دانلود فایل به سرور محلی
        dl_loc = os.path.join(Config.DOWNLOAD_DIR, str(message.from_user.id))
        os.makedirs(dl_loc, exist_ok=True)
        c_time = time.time()
        progress_msg = await message.reply_text("Downloading to my server...", parse_mode=ParseMode.MARKDOWN)
        the_media = await Bot.download_media(
            message=message,
            file_name=dl_loc,
            progress=progress_for_pyrogram,
            progress_args=(
                "Downloading ...",
                progress_msg,
                c_time
            )
        )
        await progress_msg.delete(True)

        # آپلود فایل به کانال لاگ
        uploaded_msg = await Bot.send_document(
            chat_id=Config.LOG_CHANNEL,
            document=the_media,
            caption=f"Uploaded by [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n\n**File Name**: {os.path.basename(the_media)}",
            parse_mode=ParseMode.MARKDOWN,
            disable_notification=True
        )

        # ایجاد لینک دانلود
        chat_id = Config.LOG_CHANNEL
        message_id = uploaded_msg.id
        download_link = f"https://t.me/c/{str(chat_id).replace('-100', '')}/{message_id}"

        # ارسال لینک به کاربر
        await message.reply_text(
            f"**File Name**: `{os.path.basename(the_media)}`\n\n**Download Link**: `{download_link}`",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Open Link", url=download_link)]]
            )
        )

        # ثبت لاگ
        await Bot.send_message(
            chat_id=Config.LOG_CHANNEL,
            text=f"#TELEGRAM_UPLOAD:\n\n[{message.from_user.first_name}](tg://user?id={message.from_user.id}) Uploaded to Telegram !!\n\n**File Name**: {os.path.basename(the_media)}\n**URL**: {download_link}",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_to_message_id=uploaded_msg.id
        )

        # حذف فایل موقت
        try:
            os.remove(the_media)
        except:
            pass

    except errors.FileTooLarge:
        await message.reply_text(
            "File is too large! Telegram supports up to 2GB (4GB for premium accounts).",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as err:
        await message.reply_text(
            f"Something went wrong!\n\n**Error**: `{err}`",
            parse_mode=ParseMode.MARKDOWN
        )


Bot.run()