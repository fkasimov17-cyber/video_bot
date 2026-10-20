"""
PromptCraft AI Bot — @PromptCraft_AI_bot
World-Class AI Video Prompt Engineer Telegram Bot
"""

import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from prompt_engine import enhance_prompt

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── /start ──────────────────────────────────────────────────────────────────

WELCOME_TEXT = (
    "👋 *Salom! Men PromptCraft AI botman.*\n\n"
    "🎬 Men sizning oddiy g'oyangizni *professional, kinematografik AI video promptiga* aylantirib beraman.\n\n"
    "📝 *Foydalanish:*\n"
    "Shunchaki o'zbek yoki ingliz tilida g'oyangizni yozing.\n\n"
    "Masalan:\n"
    "`Tog'larda ot minayotgan qiz`\n"
    "`A futuristic city at night with flying cars`\n\n"
    "⚡ /help — barcha buyruqlar\n"
    "🌟 /example — namuna promptlar"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("📖 Help", callback_data="help"),
            InlineKeyboardButton("🌟 Examples", callback_data="examples"),
        ],
        [InlineKeyboardButton("🎬 Generate Prompt Now", callback_data="generate")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        WELCOME_TEXT, parse_mode="Markdown", reply_markup=reply_markup
    )


# ── /help ───────────────────────────────────────────────────────────────────

HELP_TEXT = (
    "🛠 *Buyruqlar ro'yxati:*\n\n"
    "/start — Botni boshlash\n"
    "/help — Yordam\n"
    "/example — Namuna promptlar\n"
    "/about — Bot haqida\n\n"
    "💡 *Qanday ishlaydi?*\n"
    "1️⃣ G'oyangizni yozing (har qanday tilda)\n"
    "2️⃣ Bot uni *kinematografik video promptga* aylantiradi\n"
    "3️⃣ Natijani nusxa olib AI generatorga joylashtiring\n\n"
    "🎯 *Qo'llab-quvvatlanadigan AI generatorlar:*\n"
    "• Runway Gen-3 Alpha\n"
    "• OpenAI Sora\n"
    "• Kling AI\n"
    "• Luma Dream Machine\n"
    "• Pika Labs\n"
    "• MidJourney Video"
)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_TEXT, parse_mode="Markdown")


# ── /example ────────────────────────────────────────────────────────────────

EXAMPLES = [
    (
        "🌄 Tog' manzarasi",
        "A lone wolf standing on a snow-capped mountain peak at golden hour, "
        "wide-angle drone shot slowly ascending, volumetric god rays piercing through "
        "low clouds, shot on Arri Alexa Mini 35mm, cinematic color grade, 24fps.",
    ),
    (
        "🌆 Kiberp​ank shahar",
        "A female hacker in a neon-lit cyberpunk alley, rain-soaked reflections "
        "on cobblestones, slow-motion close-up dolly push-in on her glowing eyes, "
        "Blade Runner 2049 aesthetic, deep blue and magenta palette, f/1.4 bokeh, 48fps.",
    ),
    (
        "🚀 Kosmik sahna",
        "A lone astronaut floating weightlessly inside a derelict space station, "
        "Earth visible through a cracked porthole, handheld POV camera drifting slowly, "
        "harsh side lighting from solar rays, Interstellar film grain, 24fps IMAX look.",
    ),
]

EXAMPLE_TEXT = "🌟 *Namuna promptlar:*\n\n" + "\n\n".join(
    f"*{title}*\n`{prompt}`" for title, prompt in EXAMPLES
)


async def example_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(EXAMPLE_TEXT, parse_mode="Markdown")


# ── /about ──────────────────────────────────────────────────────────────────

ABOUT_TEXT = (
    "🤖 *PromptCraft AI Bot*\n\n"
    "Versiya: 1.0.0\n"
    "Kanal: @PromptCraft\\_AI\\_bot\n\n"
    "Bu bot oddiy g'oyalarni professional kinematografik "
    "AI video promptlariga aylantiradi. "
    "Sora, Runway, Kling, Luma va boshqa zamonaviy "
    "AI video generatorlari uchun optimallashtirilgan.\n\n"
    "🛠 Yaratuvchi: PromptCraft Team"
)


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(ABOUT_TEXT, parse_mode="Markdown")


# ── Callback buttons ─────────────────────────────────────────────────────────

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "help":
        await query.message.reply_text(HELP_TEXT, parse_mode="Markdown")
    elif query.data == "examples":
        await query.message.reply_text(EXAMPLE_TEXT, parse_mode="Markdown")
    elif query.data == "generate":
        await query.message.reply_text(
            "✍️ Endi g'oyangizni yozing — men uni professional video promptga "
            "aylantirib beraman!",
            parse_mode="Markdown",
        )


# ── Message handler ──────────────────────────────────────────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text.strip()
    user_name = update.effective_user.first_name or "foydalanuvchi"

    # Typing indicator
    await update.message.chat.send_action("typing")

    logger.info("User [%s]: %s", update.effective_user.id, user_text[:80])

    try:
        result = enhance_prompt(user_text)
    except Exception as exc:
        logger.error("Prompt engine error: %s", exc)
        await update.message.reply_text(
            "⚠️ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.",
            parse_mode="Markdown",
        )
        return

    response = (
        f"🎬 *Enhanced Video Prompt (Copy-Paste Ready):*\n"
        f"`{result['prompt']}`\n\n"
        f"📊 *Prompt Breakdown:*\n"
        f"• *Subject & Motion:* {result['subject']}\n"
        f"• *Cinematography & Camera:* {result['camera']}\n"
        f"• *Lighting & Style:* {result['lighting']}\n\n"
        f"💡 *Recommended AI Generator:* {result['generator']}\n"
        f"⚙️ *Aspect Ratio / FPS:* {result['specs']}"
    )

    keyboard = [
        [
            InlineKeyboardButton("🔄 Qayta yaratish", callback_data=f"regen:{user_text[:50]}"),
            InlineKeyboardButton("🌟 Yangi g'oya", callback_data="generate"),
        ]
    ]
    await update.message.reply_text(
        response,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ── Error handler ────────────────────────────────────────────────────────────

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling update:", exc_info=context.error)


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable is not set. Check your .env file.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("example", example_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    logger.info("🚀 PromptCraft AI Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
