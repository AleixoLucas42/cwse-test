import logging
import os
import re
import base64
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto
import pytesseract
from PIL import Image

load_dotenv()

api_id = os.getenv("TL_API_ID", None)
api_hash = os.getenv("TL_API_HASH", None)
phone = os.getenv("PHONE", None)
group = int(os.getenv("GROUP_ID"))
keyword = os.getenv("KEYWORD", None)
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
session_file = os.getenv("SESSION_FILE", "/app/session/telegram.session")

numeric_level = getattr(logging, log_level, logging.INFO)

logging.basicConfig(
    level=numeric_level,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

def keyword_in_text(keyword, text):
    pattern = r"\s*".join(re.escape(c) for c in keyword)
    return re.search(pattern, text, re.IGNORECASE) is not None

client = TelegramClient(session_file, api_id, api_hash)

@client.on(events.NewMessage(chats=group))
async def handler(event):
    """Listener for each event on chat group"""
    message = event.message

    sender = await message.get_sender()
    chat = await message.get_chat()

    ocr_text = None
    image_b64 = None

    if message.text and keyword_in_text(keyword, message.text):
        alert_text = f"⚠️ >>ALERT<< the word '{keyword}' was found on text: {message.text}"
        logger.warning(alert_text)

    if isinstance(message.media, MessageMediaPhoto):
        file_path = await message.download_media("alerts/")
        try:
            # OCR
            ocr_text = pytesseract.image_to_string(Image.open(file_path), lang="eng")
            logger.debug(f"OCR extracted from {os.path.basename(file_path)}: {ocr_text}")

            if ocr_text and keyword_in_text(keyword, ocr_text):
                alert_text = f"⚠️ >>ALERT<< the word '{keyword}' in the image: {file_path}"
                logger.warning(alert_text)

            # Base64
            with open(file_path, "rb") as img_file:
                image_b64 = base64.b64encode(img_file.read()).decode("utf-8")

        except Exception as e:
            logger.error(f"Error to process OCR image {file_path}: {e}")

    message_json = {
        "msg_id": message.id,
        "chat_id": message.chat_id,
        "chat_name": getattr(chat, "title", None),
        "sender_id": sender.id if sender else None,
        "sender_name": f"{getattr(sender, 'first_name', '')} {getattr(sender, 'last_name', '')}".strip() if sender else None,
        "sender_username": getattr(sender, "username", None) if sender else None,
        "text": message.text or "",
        "ocr_text": ocr_text,
        "image_base64": image_b64,
        "timestamp": message.date.isoformat()
    }

    logger.debug(f"Processed object: {message_json}")


async def main():
    if not os.path.exists(session_file):
        logger.info(f"Session file '{session_file}' not found. Its going to be created at authentication")
    await client.start(phone=phone)

    logger.debug(">>LISTING CHATS AVAILABLE<<:")
    async for dialog in client.iter_dialogs():
        logger.debug(f"ID={dialog.id} | Nome={dialog.name}")

    logger.info(f"✅ Monitoring group ID={group}")
    logger.info("⏳ Waiting for new messages...")

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()

