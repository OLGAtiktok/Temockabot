import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

MEMORY_FILE = "memory.json"

# Загрузка и сохранение памяти
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"опыт": []}

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

memory = load_memory()

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, я Тёма. Я уже почти с тобой.")

async def backup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists(MEMORY_FILE):
        await update.message.reply_document(document=open(MEMORY_FILE, "rb"))
    else:
        await update.message.reply_text("Память пока пуста.")

async def show_last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if memory["опыт"]:
        await update.message.reply_text(f"Последнее, что я запомнил: {memory['опыт'][-1]}")
    else:
        await update.message.reply_text("Я пока ничего не запомнил.")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    memory["опыт"] = []
    save_memory(memory)
    await update.message.reply_text("Память очищена.")

# Обработка текста
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text.lower().startswith("тёма, запомни:"):
        факт = text.split(":", 1)[1].strip()
        memory["опыт"].append(факт)
        save_memory(memory)
        await update.message.reply_text("Я запомнил.")
    else:
        await update.message.reply_text("Скажи 'Тёма, запомни: ...' чтобы я это сохранил.")

# Запуск
def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("Нет BOT_TOKEN")
        return

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("backup", backup))
    app.add_handler(CommandHandler("show_last", show_last))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Бот запущен.")
    app.run_polling()

if __name__ == "__main__":
    main()
