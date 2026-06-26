from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from config import TOKEN, ADMIN_ID
from database import init_db, create_user, get_user
from generator import generate


init_db()


def is_admin(user_id):
    return user_id == ADMIN_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    create_user(user.id, user.username)

    keyboard = [
        [InlineKeyboardButton("🎲 Générer IBAN", callback_data="gen")],
        [InlineKeyboardButton("👤 Profil", callback_data="sub")]
    ]

    await update.message.reply_text(
        "🚀 Bot IBAN prêt",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    user_id = q.from_user.id

    if q.data == "gen":
        iban, error = generate(user_id)

        if error:
            await q.edit_message_text(f"⏳ Cooldown actif\n\nTemps restant: {error}")
            return

        await q.edit_message_text(f"✅ IBAN:\n\n`{iban}`")

    if q.data == "sub":
        user = get_user(user_id)

        await q.edit_message_text(
            f"""👤 Profil

Plan: {user[2]}
Dernière génération: {user[3]}
Total: {user[4]}
"""
        )


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("No access")
        return

    await update.message.reply_text("🔐 Admin OK")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()
