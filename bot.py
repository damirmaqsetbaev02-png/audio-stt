import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from faster_whisper import WhisperModel

BOT_TOKEN = os.getenv("7690392497:AAHhwdxfXlj22_sRlj8u0hpOXLL8Ahw3rOY")

# CPU uchun (Railway da GPU yo‘q)
model = WhisperModel(
    "maqsudxo1ja/uz-whisper-small-stt-v2",
    device="cpu",
    compute_type="int8"
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Assalomu alaykum!\n\n"
        "Menga ovozli xabar yuboring — matnga aylantiraman.\n"
        "Faqat o‘zbek tili."
    )

@dp.message(F.voice)
async def voice_handler(message: Message):
    status = await message.answer("Ovoz qayta ishlanmoqda...")

    try:
        file = await bot.get_file(message.voice.file_id)
        ogg_path = f"voice_{message.from_user.id}.ogg"
        await bot.download_file(file.file_path, ogg_path)

        segments, info = model.transcribe(
            ogg_path,
            language="uz",
            beam_size=5,
            vad_filter=True
        )

        text = "".join([s.text for s in segments]).strip()

        if text:
            await status.edit_text(f"**Natija:**\n\n{text}")
        else:
            await status.edit_text("Hech narsa tushunilmadi.")

        os.remove(ogg_path)

    except Exception as e:
        await status.edit_text(f"Xatolik: {str(e)}")

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
