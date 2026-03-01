import os
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ===== DEMO TOP3 =====
def generate_top3():
    return [
        ("Inter vs Genoa", "Over 1.5", 0.72, 1.55),
        ("PSG vs Le Havre", "Under 3.5", 0.75, 1.40),
        ("Atletico vs Oviedo", "1X", 0.70, 1.50),
    ]

# ===== HANDLERS =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bankroll AI Bot aktív!\n\n"
        "/today - Mai top 3\n"
        "/ping - Teszt"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot működik ✅")

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    results = generate_top3()

    msg = "🔥 Mai TOP 3 Tipp:\n\n"
    for match, label, p, o in results:
        msg += f"{match}\n→ {label}\nOdds: {o}\np: {p:.2f}\n\n"

    await update.message.reply_text(msg)

# ===== AUTOMATIKUS 10:00 =====
async def auto_send(context: ContextTypes.DEFAULT_TYPE):
    results = generate_top3()

    msg = "🔥 AUTOMATIKUS 10:00 TOP 3\n\n"
    for match, label, p, o in results:
        msg += f"{match}\n→ {label}\nOdds: {o}\np: {p:.2f}\n\n"

    await context.bot.send_message(chat_id=context.job.chat_id, text=msg)

# ===== APP =====
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("today", today))
app.add_handler(CommandHandler("ping", ping))

scheduler = AsyncIOScheduler(timezone=pytz.timezone("Europe/Budapest"))
scheduler.start()

app.run_polling()
