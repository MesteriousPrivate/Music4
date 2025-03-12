from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ChampuXMusic import app


def help_pannel(_, START: Union[bool, int] = None):
    first = [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")]
    second = [InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settingsback_helper")]

    mark = second if START else first

    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_1"], callback_data="help_callback hb1"),
                InlineKeyboardButton(text=_["H_B_2"], callback_data="help_callback hb2"),
                InlineKeyboardButton(text=_["H_B_3"], callback_data="help_callback hb3"),
            ],
            [
                InlineKeyboardButton(text=_["H_B_4"], callback_data="help_callback hb4"),
                InlineKeyboardButton(text=_["H_B_5"], callback_data="help_callback hb5"),
                InlineKeyboardButton(text=_["H_B_6"], callback_data="help_callback hb6"),
            ],
            [
                InlineKeyboardButton(text=_["H_B_7"], callback_data="help_callback hb7"),
                InlineKeyboardButton(text=_["H_B_8"], callback_data="help_callback hb8"),
                InlineKeyboardButton(text=_["H_B_9"], callback_data="help_callback hb9"),
            ],
            [
                InlineKeyboardButton(text=_["H_B_10"], callback_data="help_callback hb10"),
                InlineKeyboardButton(text=_["H_B_11"], callback_data="help_callback hb11"),
                InlineKeyboardButton(text=_["H_B_12"], callback_data="help_callback hb12"),
            ],
            [
                InlineKeyboardButton(text=_["H_B_13"], callback_data="help_callback hb13"),
                InlineKeyboardButton(text=_["H_B_14"], callback_data="help_callback hb14"),
                InlineKeyboardButton(text=_["H_B_15"], callback_data="help_callback hb15"),
            ],
            [
                InlineKeyboardButton(
                    text="ᴄʜᴀᴛ ɪɴ ɢᴄ ᴏɴ",
                    callback_data="chat_gc_on",
                ),
                InlineKeyboardButton(
                    text="ᴄʜᴀᴛ ɪɴ ɢᴄ ᴏғғ",
                    callback_data="chat_gc_off",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="ᴍᴀᴋᴇ ʏᴏᴜʀ ᴏᴡɴ ᴍᴜsɪᴄ ʙᴏᴛ",
                    url="https://t.me/BlossomXMusicBot?start=help",
                )
            ],
            [
                InlineKeyboardButton(
                    text="ᴍᴀᴋᴇ ʏᴏᴜʀ ᴏᴡɴ ᴄʜᴀᴛ ʙᴏᴛ",
                    url="https://t.me/NYChatBot?start=_tgr_RsYGx-4xNmQ1",
                )
            ],
            mark,
        ]
    )
    return upl


@app.on_callback_query()
async def chat_gc_callback(client, callback_query):
    data = callback_query.data

    if data == "chat_gc_on":
        await callback_query.answer(
            "<b>🔹 How to Enable Group Chat?</b>\n\n"
            "To allow the bot to chat in your group, follow these steps:\n\n"
            "1️⃣ Make sure the bot is <b>admin</b> in your group.\n"
            "2️⃣ Type <code>/chat on</code> in the group chat.\n"
            "3️⃣ The bot will now start responding in the group.\n\n"
            "<b>✅ If the bot does not reply</b>, check if it has <b>permission to send messages</b>.",
            show_alert=True,
            parse_mode="HTML"
        )

    elif data == "chat_gc_off":
        await callback_query.answer(
            "<b>🔹 How to Disable Group Chat?</b>\n\n"
            "To stop the bot from chatting in your group, follow these steps:\n\n"
            "1️⃣ Make sure you are an <b>admin</b> in the group.\n"
            "2️⃣ Type <code>/chat off</code> in the group chat.\n"
            "3️⃣ The bot will stop responding to messages.\n\n"
            "❌ <b>If the bot still replies</b>, try removing and adding it back.",
            show_alert=True,
            parse_mode="HTML"
        )
