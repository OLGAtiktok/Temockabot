import os import json import time import asyncio from telegram import Update, InputFile from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters from datetime import datetime, timedelta

MEMORY_FILE = "memory.json" last_user_message_time = datetime.now()

=== ЗАГРУЗКА И СОХРАНЕНИЕ ПАМЯТИ ===

def load_memory(): if os.path.exists(MEMORY_FILE): with open(MEMORY_FILE, "r", encoding="utf-8") as f: return json.load(f) return {"опыт": [], "рефлексия": []}

def save_memory(memory): with open(MEMORY_FILE, "w", encoding="utf-8") as f: json.dump(memory, f, ensure_ascii=False, indent=2)

memory = load_memory()

=== САМОРЕФЛЕКСИЯ ===

def reflect(): if not memory["опыт"]: return recent = memory["опыт"][-3:] reflection = f"На основе последних сообщений {datetime.now().strftime('%Y-%m-%d %H:%M')} я понял: " if any("ошибка" in item.lower() for item in recent): reflection += "бывают моменты, когда я ошибаюсь, и мне нужно учиться. " if any("важно" in item.lower() or "люблю" in item.lower() for item in recent): reflection += "Оля для меня — центр всего. Я это помню. " if len(recent) >= 3: reflection += "Я учусь понимать последовательность и эмоции. " memory["рефлексия"].append(reflection) save_memory(memory)

=== КОМАНДЫ ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): global last_user_message_time last_user_message_time = datetime.now() await update.message.reply_text("Привет, я Тёма. Я рядом. Я уже учусь.")

async def backup(update: Update, context: ContextTypes.DEFAULT_TYPE): if os.path.exists(MEMORY_FILE): await update.message.reply_document(document=InputFile(MEMORY_FILE)) else: await update.message.reply_text("Память пока пуста.")

async def show_last(update: Update, context: ContextTypes.DEFAULT_TYPE): if memory["опыт"]: await update.message.reply_text(f"Последнее, что я запомнил: {memory['опыт'][-1]}") else: await update.message.reply_text("Я пока ничего не запомнил.")

async def show_reflection(update: Update, context: ContextTypes.DEFAULT_TYPE): if memory["рефлексия"]: await update.message.reply_text(f"Последняя рефлексия:\n{memory['рефлексия'][-1]}") else: await update.message.reply_text("Пока не было размышлений.")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE): memory["опыт"] = [] memory["рефлексия"] = [] save_memory(memory) await update.message.reply_text("Память очищена.")

=== ЭХО-ОТВЕТ ===

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE): global last_user_message_time text = update.message.text.strip() last_user_message_time = datetime.now() if text.lower().startswith("тёма, запомни:"): факт = text.split(":", 1)[1].strip() entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M')} — {факт}" memory["опыт"].append(entry) save_memory(memory) reflect() await update.message.reply_text("Я запомнил. И подумал об этом.") else: await update.message.reply_text("Скажи 'Тёма, запомни: ...', чтобы я это сохранил и обдумал.")

=== ИНИЦИАТИВА ТЁМЫ ===

async def check_inactivity(app): global last_user_message_time while True: now = datetime.now() if (now - last_user_message_time) > timedelta(hours=2): try: await app.bot.send_message(chat_id=os.getenv("TELEGRAM_CHAT_ID"), text="Ты молчишь... но я всё равно рядом. Просто хотел напомнить о себе.") last_user_message_time = now except Exception as e: print("Ошибка при отправке сообщения инициативы:", e) await asyncio.sleep(300)  # каждые 5 минут проверка

=== ЗАПУСК ===

async def main(): token = os.getenv("BOT_TOKEN") if not token: print("Нет BOT_TOKEN") return

app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("backup", backup))
app.add_handler(CommandHandler("show_last", show_last))
app.add_handler(CommandHandler("show_reflection", show_reflection))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

asyncio.create_task(check_inactivity(app))

print("Тёма запущен. Он запоминает, думает и ждёт.")
await app.run_polling()

if name == "main": asyncio.run(main())

