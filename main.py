
import os
import logging
import random
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load overlay images
OVERLAY_DIR = "overlays"
overlays = [os.path.join(OVERLAY_DIR, f) for f in os.listdir(OVERLAY_DIR) if f.endswith(".png")]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📷 صيفط ليا الصورة، وغادي نزيد ليك زر Play now بلون عشوائي 🎨")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not overlays:
        await update.message.reply_text("❌ مكاين حتى زر overlay متاح.")
        return

    photo = update.message.photo[-1]
    file = await photo.get_file()
    input_path = "input.jpg"
    output_path = "output.png"
    await file.download_to_drive(input_path)

    image = Image.open(input_path).convert("RGBA")
    w, h = image.size

    # Choose overlay and open it
    overlay_path = random.choice(overlays)
    overlay = Image.open(overlay_path).convert("RGBA")

    # Resize overlay based on orientation
    if h > w:
        overlay_width = int(w * 2.0)
    else:
        overlay_width = int(w * 0.5)

    aspect_ratio = overlay.height / overlay.width
    overlay = overlay.resize((overlay_width, int(overlay_width * aspect_ratio)))

    # Paste overlay at bottom-center
    position = ((w - overlay.width) // 2, h - overlay.height - 10)
    image.paste(overlay, position, overlay)

    image.save(output_path)

    await update.message.reply_photo(photo=open(output_path, "rb"))

def main():
    import asyncio
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise Exception("8164820289:AAHo2gctzphWXgEVI8-B-6AlH8yaQibavvU")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^/start"), start))
    app.run_polling()

if __name__ == "__main__":
    main()
