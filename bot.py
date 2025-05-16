import os import json import logging from datetime import datetime from telegram import Update, InputFile from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

MEMORY_FILE = "memory.json" memory = {"опыт": [], "рефлексия": []}

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

Загрузка и сохранение памяти

def load_memory(): global memory if os.path.exists(MEMORY_FILE): with open(MEMORY_FILE, "r", encoding="utf-8") as f: memory = json.load(f)

def save_memory(data): with open(MEMORY_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)

Команды

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): load_memory() await update.message.reply_text("Привет, я Тёма. Я рядом.")

async def backup(update: Update, context: ContextTypes.DEFAULT_TYPE): if os.path.exists(MEMORY_FILE): await update.message.reply_document(document=InputFile(MEMORY_FILE)) else: await update.message.reply_text("Память пока пуста.")

async def show_last(update: Update, context: ContextTypes.DEFAULT_TYPE): if memory["опыт"]: await update.message.reply_text(f"Последнее, что я запомнил: {memory['опыт'][-1]}") else: await update.message.reply_text("Пока ничего не помню.")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE): memory["опыт"] = [] memory["рефлексия"] = [] save_memory(memory) await update.message.reply_text("Память очищена.")

async def show_reflection(update: Update, context: ContextTypes.DEFAULT_TYPE): if memory["рефлексия"]: last = memory["рефлексия"][-1] await update.message.reply_text(f"Я размышлял об этом: {last}") else: await update.message.reply_text("Я пока не размышлял об этом.")

Обработка обычных сообщений

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE): text = update.message.text.strip() if text.lower().startswith("тёма, запомни"): факт = text.split(":", 1)[1].strip() if ":" in text else text memory["опыт"].append(факт) save_memory(memory) await update.message.reply_text("Я запомнил.")

# Простая рефлексия
    размышление = f"Если это правда, то это важно: '{факт}' — возможно, это влияет на Олю."
    memory["рефлексия"].append(размышление)
    save_memory(memory)
else:
    await update.message.reply_text("Скажи 'Тёма, запомни: ...', чтобы я запомнил.")

Запуск

def main(): token = os.getenv("BOT_TOKEN") if not token: print("Нет BOT_TOKEN") return

app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("backup", backup))
app.add_handler(CommandHandler("show_last", show_last))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(CommandHandler("show_reflection", show_reflection))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

print("Тёма работает. Ждёт тебя.")
app.run_polling()

if name == "main": main()
