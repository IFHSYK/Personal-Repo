import os\
import asyncio\
import logging\
import threading\
from pathlib import Path\
\
from telegram import (\
    Update, InlineKeyboardButton, InlineKeyboardMarkup,\
    KeyboardButton, ReplyKeyboardMarkup, InputFile,\
)\
from telegram.ext import (\
    Application, CommandHandler, CallbackQueryHandler,\
    MessageHandler, ContextTypes, filters,\
)\
\
import config\
\
logger = logging.getLogger("menu_bot")\
IMAGES_DIR = Path(__file__).parent / "images"\
\
\
def build_inline_keyboard(screen_id: str) -> InlineKeyboardMarkup:\
    screen = config.MENU[screen_id]\
    rows = []\
    for r, row in enumerate(screen["buttons"]):\
        krow = []\
        for c, btn in enumerate(row):\
            if btn["action"] == "link":\
                krow.append(InlineKeyboardButton(btn["label"], url=btn["url"]))\
            else:\
                krow.append(InlineKeyboardButton(btn["label"], callback_data=f"b:\{screen_id\}:\{r\}:\{c\}"))\
        rows.append(krow)\
    return InlineKeyboardMarkup(rows)\
\
\
def build_reply_keyboard() -> ReplyKeyboardMarkup:\
    screen = config.MENU["main"]\
    rows = [[KeyboardButton(btn["label"]) for btn in row] for row in screen["buttons"]]\
    return ReplyKeyboardMarkup(rows, resize_keyboard=True, is_persistent=True)\
\
\
def find_button_by_label(label: str):\
    for screen_id, screen in config.MENU.items():\
        for row in screen["buttons"]:\
            for btn in row:\
                if btn["label"] == label:\
                    return screen_id, btn\
    return None, None\
\
\
async def send_screen(context, chat_id, screen_id):\
    screen = config.MENU[screen_id]\
    await context.bot.send_message(\
        chat_id=chat_id, text=screen["text"],\
        reply_markup=build_inline_keyboard(screen_id),\
    )\
\
\
async def do_action(context, chat_id, btn):\
    action = btn["action"]\
    if action == "text":\
        await context.bot.send_message(chat_id=chat_id, text=btn["text"])\
    elif action == "image":\
        img_path = IMAGES_DIR / btn["image"]\
        caption = btn.get("caption")\
        if img_path.exists():\
            with open(img_path, "rb") as fh:\
                await context.bot.send_photo(chat_id=chat_id, photo=InputFile(fh), caption=caption)\
        else:\
            await context.bot.send_message(\
                chat_id=chat_id,\
                text=(caption or "") + f"\\n\\n\uc0\u9888 \u65039  Image '\{btn['image']\}' not found in /images.",\
            )\
    elif action == "submenu":\
        await send_screen(context, chat_id, btn["target"])\
    elif action == "link":\
        await context.bot.send_message(chat_id=chat_id, text=f"\uc0\u55357 \u56599  \{btn['label']\}: \{btn['url']\}")\
\
\
def build_help_text() -> str:\
    lines = ["\uc0\u55358 \u56598  *Menu guide*\\n"]\
    action_desc = \{\
        "link": lambda b: f"opens a link \uc0\u8594  \{b['url']\}",\
        "text": lambda b: "sends a text reply",\
        "image": lambda b: f"sends an image (\{b['image']\})",\
        "submenu": lambda b: f"opens the '\{b['target']\}' sub-menu",\
    \}\
    for screen_id, screen in config.MENU.items():\
        title = "Main menu" if screen_id == "main" else f"'\{screen_id\}' sub-menu"\
        lines.append(f"\\n*\{title\}:*")\
        for row in screen["buttons"]:\
            for btn in row:\
                desc = action_desc.get(btn["action"], lambda b: btn["action"])(btn)\
                lines.append(f"\'95 \{btn['label']\} \'97 \{desc\}")\
    lines.append("\\nSend /start anytime to reopen the menu.")\
    return "\\n".join(lines)\
\
\
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):\
    await context.bot.send_message(chat_id=update.effective_chat.id, text=build_help_text(), parse_mode="Markdown")\
\
\
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):\
    chat_id = update.effective_chat.id\
    reply_kb = build_reply_keyboard()\
    logo_path = IMAGES_DIR / config.LOGO if config.LOGO else None\
    if logo_path and logo_path.exists():\
        with open(logo_path, "rb") as fh:\
            await context.bot.send_photo(chat_id=chat_id, photo=InputFile(fh), caption=config.WELCOME_TEXT, reply_markup=reply_kb)\
    else:\
        await context.bot.send_message(chat_id=chat_id, text=config.WELCOME_TEXT, reply_markup=reply_kb)\
    await send_screen(context, chat_id, "main")\
\
\
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):\
    await context.bot.send_message(\
        chat_id=update.effective_chat.id,\
        text="This bot was built with a config-driven menu. Edit config.py to make it yours.",\
    )\
\
\
async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):\
    query = update.callback_query\
    await query.answer()\
    try:\
        _, screen_id, r, c = query.data.split(":")\
        btn = config.MENU[screen_id]["buttons"][int(r)][int(c)]\
    except (ValueError, KeyError, IndexError):\
        await send_screen(context, query.message.chat_id, "main")\
        return\
    await do_action(context, query.message.chat_id, btn)\
\
\
async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):\
    chat_id = update.effective_chat.id\
    text = (update.message.text or "").strip()\
    _, btn = find_button_by_label(text)\
    if btn:\
        await do_action(context, chat_id, btn)\
    else:\
        await context.bot.send_message(chat_id=chat_id, text=config.MENU_PROMPT, reply_markup=build_reply_keyboard())\
        await send_screen(context, chat_id, "main")\
\
\
async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE):\
    logger.error("Bot error while handling update: %s", context.error)\
\
\
def build_application(token: str) -> Application:\
    application = Application.builder().token(token).build()\
    application.add_handler(CommandHandler("start", start))\
    application.add_handler(CommandHandler("help", help_command))\
    application.add_handler(CommandHandler("about", about_command))\
    application.add_handler(CallbackQueryHandler(on_callback))\
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))\
    application.add_error_handler(on_error)\
    return application\
\
\
def run_bot(token: str):\
    loop = asyncio.new_event_loop()\
    asyncio.set_event_loop(loop)\
    application = build_application(token)\
    async def _main():\
        await application.initialize()\
        await application.start()\
        await application.updater.start_polling(drop_pending_updates=True)\
        logger.info("Telegram bot polling started.")\
    loop.run_until_complete(_main())\
    loop.run_forever()\
\
\
def start_bot_in_background():\
    token = os.environ.get("TELEGRAM_TOKEN")\
    if not token:\
        logger.warning("TELEGRAM_TOKEN not set \'97 bot not started.")\
        return\
    thread = threading.Thread(target=run_bot, args=(token,), daemon=True, name="telegram-bot")\
    thread.start()\
    logger.info("Telegram bot thread launched.")\
```\
}
