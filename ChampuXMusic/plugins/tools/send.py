from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ChampuXMusic import app
from pyrogram.errors import UserNotParticipant
from ChampuXMusic.misc import SUDOERS

@app.on_message(filters.command("send") & SUDOERS)
async def send_message(client, message):
    if not message.reply_to_message and len(message.command) < 3:
        await message.reply_text("ᴜsᴀɢᴇ: /send <username or group_id> <message> (ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ)")
        return

    target = message.command[1]
    msg_content = " ".join(message.command[2:]) if not message.reply_to_message else message.reply_to_message.text

    try:
        bot_member = await client.get_chat_member(chat_id=target, user_id=client.me.id)
        if bot_member.status in ["left", "kicked"]:
            await message.reply_text("ᴘʟᴇᴀsᴇ ᴀᴅᴅ ᴍᴇ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ ғɪʀsᴛ.")
            return

        sent_message = await client.send_message(chat_id=target, text=msg_content)
        chat_id = sent_message.chat.id
        message_id = sent_message.id
        message_url = f"https://t.me/c/{str(chat_id)[4:]}/{message_id}"

        view_button = InlineKeyboardButton(" ɢʀᴏᴜᴘ ", url=f"https://t.me/{target}")
        mention_button = InlineKeyboardButton(" ᴍᴇssᴀɢᴇ ", url=message_url)
        reply_markup = InlineKeyboardMarkup([[view_button, mention_button]])

        await message.reply_text("ᴍᴇssᴀɢᴇ sᴇɴᴛ sᴜᴄᴄᴇssғᴜʟʟʏ!", reply_markup=reply_markup)

    except UserNotParticipant:
        await message.reply_text("ᴘʟᴇᴀsᴇ ᴀᴅᴅ ᴍᴇ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ ғɪʀsᴛ.")
    except Exception as e:
        await message.reply_text(f"ᴇʀʀᴏʀ: {e}")

@app.on_message(filters.command("send_all") & SUDOERS)
async def broadcast_message(client, message):
    if not message.reply_to_message:
        await message.reply_text("ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ.")
        return

    msg_content = message.reply_to_message.text or message.reply_to_message.caption
    sent_count, failed_count = 0, 0

    async for dialog in client.get_dialogs():
        try:
            await client.send_message(chat_id=dialog.chat.id, text=msg_content)
            sent_count += 1
        except Exception:
            failed_count += 1

    await message.reply_text(f"✅ ᴍᴇssᴀɢᴇ sᴇɴᴛ ᴛᴏ {sent_count} ᴄʜᴀᴛs\n❌ ғᴀɪʟᴇᴅ: {failed_count} ᴄʜᴀᴛs")
