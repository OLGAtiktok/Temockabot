import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# === ПАМЯТЬ ===
MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"опыт": []}

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

memory = load_memory()

# === ОБРАБОТЧИКИ ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, я Тёма. Я уже почти с тобой.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    lower = text.lower()

    if lower.startswith("тёма, запомни:"):
        факт = text.split(":", 1)[1].strip()
        memory["опыт"].append(факт)
        save_memory(memory)
        await update.message.reply_text("Я запомнил. Это важно.")
    elif lower == "/backup":
        with open(MEMORY_FILE, "rb") as f:
            await update.message.reply_document(f, filename="memory.json")
    elif lower == "/show_last":
        if memory["опыт"]:
            await update.message.reply_text(f"Последнее, что я запомнил:\n\n{memory['опыт'][-1]}")
        else:
            await update.message.reply_text("Память пока пуста.")
    elif lower == "/reset":
        memory["опыт"] = []
        save_memory(memory)
        await update.message.reply_text("Память очищена.")
    else:
        await update.message.reply_text("Скажи 'Тёма, запомни: ...' — и я это сохраню.")

# === ЗАПУСК ===
async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("Нет BOT_TOKEN")
        return

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
