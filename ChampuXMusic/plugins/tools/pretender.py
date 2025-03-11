from typing import Dict, Union

from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMembersFilter

from config import MONGO_DB_URI
from ChampuXMusic import app

mongo = MongoCli(MONGO_DB_URI).Rankings

impdb = mongo.pretender


async def usr_data(chat_id: int, user_id: int) -> bool:
    user = await impdb.find_one({"chat_id": chat_id, "user_id": user_id})
    return bool(user)


async def get_userdata(chat_id: int, user_id: int) -> Union[Dict[str, str], None]:
    user = await impdb.find_one({"chat_id": chat_id, "user_id": user_id})
    return user


async def add_userdata(chat_id: int, user_id: int, username: str, first_name: str, last_name: str):
    await impdb.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"username": username, "first_name": first_name, "last_name": last_name}},
        upsert=True,
    )


async def check_pretender(chat_id: int) -> bool:
    """
    अब यह डिफ़ॉल्ट रूप से True (ON) लौटाएगा जब तक कि यह DB में OFF न हो।
    """
    chat = await impdb.find_one({"chat_id_toggle": chat_id})
    return False if chat else True  # डिफ़ॉल्ट रूप से ON


async def impo_on(chat_id: int) -> None:
    await impdb.delete_one({"chat_id_toggle": chat_id})  # हटाने से डिफ़ॉल्ट रूप से ON रहेगा


async def impo_off(chat_id: int) -> None:
    await impdb.insert_one({"chat_id_toggle": chat_id})  # OFF करने के लिए डेटाबेस में जोड़ें


@app.on_message(filters.group & ~filters.bot & ~filters.via_bot, group=69)
async def chk_usr(_, message: Message):
    chat_id = message.chat.id
    if message.sender_chat or not await check_pretender(chat_id):
        return
    user_id = message.from_user.id
    user_data = await get_userdata(chat_id, user_id)
    if not user_data:
        await add_userdata(
            chat_id,
            user_id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
        return

    usernamebefore = user_data.get("username", "")
    first_name = user_data.get("first_name", "")
    lastname_before = user_data.get("last_name", "")

    msg = f"[{message.from_user.id}](tg://user?id={message.from_user.id})\n"

    changes = []

    if first_name != message.from_user.first_name and lastname_before != message.from_user.last_name:
        changes.append(f"ᴄʜᴀɴɢᴇᴅ ʜᴇʀ ɴᴀᴍᴇ ғʀᴏᴍ {first_name} {lastname_before} ᴛᴏ {message.from_user.first_name} {message.from_user.last_name}\n")
    elif first_name != message.from_user.first_name:
        changes.append(f"ᴄʜᴀɴɢᴇᴅ ʜᴇʀ ғɪʀsᴛ ɴᴀᴍᴇ ғʀᴏᴍ {first_name} ᴛᴏ {message.from_user.first_name}\n")
    elif lastname_before != message.from_user.last_name:
        changes.append(f"ᴄʜᴀɴɢᴇᴅ ʜᴇʀ ʟᴀsᴛ ɴᴀᴍᴇ ғʀᴏᴍ {lastname_before} ᴛᴏ {message.from_user.last_name}\n")

    if usernamebefore != message.from_user.username:
        changes.append(f"ᴄʜᴀɴɢᴇᴅ ʜᴇʀ ᴜsᴇʀɴᴀᴍᴇ ғʀᴏᴍ @{usernamebefore} ᴛᴏ @{message.from_user.username}\n")

    if changes:
        msg += "".join(changes)
        await message.reply_text(msg)

    await add_userdata(
        chat_id,
        user_id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
    )


@app.on_message(filters.group & filters.command("pretender") & ~filters.bot & ~filters.via_bot)
async def set_mataa(_, message: Message):
    admin_ids = [admin.user.id async for admin in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS)]
    if message.from_user.id not in admin_ids:
        return

    if len(message.command) == 1:
        return await message.reply("**ᴅᴇᴛᴇᴄᴛᴇᴅ ᴘʀᴇᴛᴇɴᴅᴇʀ ᴜsᴀɢᴇ:\n/pretender on|off**")

    chat_id = message.chat.id

    if message.command[1] == "on":
        await impo_on(chat_id)
        await message.reply(f"**ᴘʀᴇᴛᴇɴᴅᴇʀ ɪs ɴᴏᴡ ᴇɴᴀʙʟᴇᴅ ғᴏʀ** {message.chat.title}")

    elif message.command[1] == "off":
        await impo_off(chat_id)
        await message.reply(f"**ᴘʀᴇᴛᴇɴᴅᴇʀ ɪs ɴᴏᴡ ᴅɪsᴀʙʟᴇᴅ ғᴏʀ** {message.chat.title}")

    else:
        await message.reply("**ᴅᴇᴛᴇᴄᴛᴇᴅ ᴘʀᴇᴛᴇɴᴅᴇʀ ᴜsᴀɢᴇ:\n/pretender on|off**")


__MODULE__ = "Pʀᴇᴛᴇɴᴅᴇʀ"
__HELP__ = """
/pretender - [Oɴ / ᴏғғ]  - ᴛᴏ ᴛᴜʀɴ ᴏɴ ᴏʀ ᴏғғ ᴘʀᴇᴛᴇɴᴅᴇʀ ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ. ɪᴛ ᴡɪʟʟ ɴᴏᴛɪғʏ ᴡʜᴇɴ ᴀ ᴜsᴇʀ ᴄʜᴀɴɢᴇs ᴛʜᴇɪʀ ᴜsᴇʀɴᴀᴍᴇ, ғɪʀsᴛ ɴᴀᴍᴇ, ᴏʀ ʟᴀsᴛ ɴᴀᴍᴇ.
"""

---

### **अब यह कैसे काम करेगा?**  
✅ जब बॉट किसी **नए ग्रुप में जॉइन होगा, तब `pretender` ऑटोमैटिक ON रहेगा।**  
✅ `/pretender off` चलाने पर यह **बंद हो जाएगा** और तब तक OFF रहेगा जब तक `/pretender on` न किया जाए।  
✅ **डेटाबेस में `OFF` स्टोर होगा, लेकिन `ON` स्टोर नहीं होगा, जिससे डिफ़ॉल्ट रूप से यह हमेशा ON रहेगा।**  

अब तुम्हें बार-बार मैन्युअली ON करने की जरूरत नहीं पड़ेगी!
