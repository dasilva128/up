# (c) @Savior_128

import os

class Config(object):
    API_ID = int(os.environ.get("API_ID", 0))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    GOFILE_API = os.environ.get("GOFILE_API", "")
    STREAMTAPE_API_PASS = os.environ.get("STREAMTAPE_API_PASS", "")
    STREAMTAPE_API_USERNAME = os.environ.get("STREAMTAPE_API_USERNAME", "")
    PIXELDRAIN_API_KEY = os.environ.get("PIXELDRAIN_API_KEY", "")  # کلید API جدید برای Pixeldrain
    SESSION_NAME = os.environ.get("SESSION_NAME", "CloudManagerBot")
    BOT_OWNER = int(os.environ.get("BOT_OWNER", 0))
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", 0))
    DOWNLOAD_DIR = os.environ.get("DOWNLOAD_DIR", "./downloads")
    HELP_TEXT = """
Send me any Media & Choose Upload Server,
I will Upload the Media to that server.

Currently I can Upload to:
> GoFile.io
> Streamtape.com
> Pixeldrain.com

**Commands:**
- `/start`: Start the bot
- `/help`: Show this help message
- Inline commands: `!godel`, `!stdel`, `!strename`, `!stremote`, `!show`, `!strmdel`

Also I can do a lot of things from Inline!
__Check Below Buttons >>>__
"""
    PROGRESS = """
Percentage: {0}%
Done ✅: {1}
Total 🌀: {2}
Speed 🚀: {3}/s
ETA 🕰: {4}
"""