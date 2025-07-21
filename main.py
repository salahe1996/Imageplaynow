
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📷 صيفط ليا صورة، وغادي نزيد ليك الزر 'Play Now' 👇")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = await update.message.photo[-1].get_file()
    await photo.download_to_drive("input.jpg")

    background = Image.open("input.jpg").convert("RGBA")
    overlay = Image.open("play_now.png").convert("RGBA")

    # ⬆️ Resize overlay to 65% of image width (bigger for portrait images)
    overlay_width = int(background.width * 0.65)
    overlay_height = int(overlay.height * overlay_width / overlay.width)
    overlay = overlay.resize((overlay_width, overlay_height))

    # ⬇️ Place near bottom center
    x = (background.width - overlay.width) // 2
    y = background.height - overlay.height - 40

    background.paste(overlay, (x, y), overlay)
    background.convert("RGB").save("output.jpg")

    await update.message.reply_photo(photo=open("output.jpg", "rb"))

# ✅ بدّل التوكن ديالك من BotFather
app = ApplicationBuilder().token("8164820289:AAHo2gctzphWXgEVI8-B-6AlH8yaQibavvU").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.run_polling()
