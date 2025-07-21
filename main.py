
import random
import os
from pathlib import Path
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📷 صيفط ليا الصورة، وغادي نزيد ليك زر Play now بلون عشوائي 🎨")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📥 وصلك صورة")

    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive("input.jpg")

    background = Image.open("input.jpg").convert("RGBA")

    overlay_folder = Path("overlays")
    overlays = list(overlay_folder.glob("*.png"))
    if not overlays:
        await update.message.reply_text("🚫 ما كاين حتى زر فـ overlays/.")
        return

    selected_overlay = Image.open(random.choice(overlays)).convert("RGBA")

    # Detect image orientation
    is_portrait = background.height > background.width

    # Adjust overlay size dynamically
    if is_portrait:
        overlay_width = int(background.width * 0.5)
    else:
        overlay_width = int(background.width * 0.6)  # larger for landscape

    overlay_height = int(selected_overlay.height * overlay_width / selected_overlay.width)
    selected_overlay = selected_overlay.resize((overlay_width, overlay_height))

    x = (background.width - overlay_width) // 2
    y = background.height - overlay_height - 30

    background.paste(selected_overlay, (x, y), selected_overlay)
    background.save("output.png")

    print("📤 الرد بصورة جديدة")
    await update.message.reply_photo(photo=open("output.png", "rb"))

# Run bot
token = os.getenv("TELEGRAM_BOT_TOKEN") or "8164820289:AAHo2gctzphWXgEVI8-B-6AlH8yaQibavvU"
app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.run_polling()
