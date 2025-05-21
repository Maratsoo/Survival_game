from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

facts = [
    "🎯 Bazuku var atrast tikai izpētes laikā. Iespēja: 5% / You can find a bazooka only during exploration. Chance: 5%",
    "🔋 Atpūšoties, tu atgūsti +2 enerģiju. Maksimums — 10 / Resting restores +2 energy. Max — 10",
    "💧 Lietus laikā tu saņem +2 ūdeni / During rain, you get +2 water",
    "🦁 Lauva var dot apģērbu ar 30% iespēju / A lion can give you clothes with a 30% chance",
    "🎒 Tev ir maksimums 2 darbības dienā / You can perform a maximum of 2 actions per day",
    "🏕️ Teltis pasargā no lauvas uzbrukuma / A tent protects you from lion attacks",
    "🎁 Priekšmetus var atrast izpētes laikā ar 20% iespēju / Items can be found during exploration with a 20% chance",
    "🧪 Zāles ārstē slimības un brūces, bet pazūd pēc lietošanas / Medicine heals diseases and wounds but disappears after use",
    "🎉 Ja izdzīvosi 30 dienas — tu uzvari! / Survive 30 days — and you win!"
]


TOKEN = "7044564312:AAGaVGsjzIq926dE0fhE1nea5s5sGZHvT98"

# Игроки
players = {}

# Предметы
item_names = ["Apģērbs", "Bints", "Telts", "Zāles", "Bazuka"]

# Начальное состояние игрока
def create_player():
    return {
        "день": 1,
        "вода": 5,
        "еда": 5,
        "энергия": 5,
        "жизнь": 10,
        "действия": 0,
        "предметы": [],
        "болен": False,
        "рана": False,
        "базука": False
    }

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    players[update.effective_user.id] = create_player()
    msg = (
        "🌲 Sveicināts meža izdzīvošanas spēlē!\n"
        "🌲 Welcome to the forest survival game!\n\n"
        "🗓 Tu esi 1. dienā / You are on day 1.\n"
        "🎯 Tavs mērķis ir izdzīvot 30 dienas! / Survive 30 days.\n\n"
        "📋 Komandas / Commands:\n"
        "/status - Parādīt statusu / Show status\n"
        "/rest - Atpūsties / Rest\n"
        "/hunt - Medīt / Hunt\n"
        "/explore - Izpētīt / Explore\n"
        f"/heal - ārstēt / Heal\n"
        "/endday - Beigt dienu / End the day\n"
        "/nextday - Nākamā diena / Go to next day"
    )
    await update.message.reply_text(msg)

# status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = players.get(update.effective_user.id)
    if not user:
        await update.message.reply_text("Sāc ar /start!")
        return

    msg = (
        f"🗓 Dienas: {user['день']}\n"
        f"💧 Ūdens: {user['вода']}\n"
        f"🍖 Ēdiens: {user['еда']}\n"
        f"⚡ Enerģija: {user['энергия']}\n"
        f"❤️ Dzīvība: {user['жизнь']}\n"
        f"🎒 Priekšmeti: {', '.join(user['предметы']) if user['предметы'] else 'Nav'}\n"
        f"📌 Darbības šodien: {user['действия']} / 2\n\n"
        f"📋 Komandas / Commands:\n"
        f"/status - Parādīt statusu / Show status\n"
        f"/rest - Atpūsties / Rest\n"
        f"/hunt - Medīt / Hunt\n"
        f"/explore - Izpētīt / Explore\n"
        f"/heal - ārstēt / Heal\n"
        f"/endday - Beigt dienu / End the day\n"
        f"/nextday - Nākamā diena / Go to next day"
    )
    await update.message.reply_text(msg)

# Действия
async def rest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await do_action(update, "rest")

async def hunt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await do_action(update, "hunt")

async def explore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await do_action(update, "explore")

async def heal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await do_action(update, "heal")

async def do_action(update, action):
    user = players.get(update.effective_user.id)
    if not user or user["действия"] >= 2:
        await update.message.reply_text("❌ Tu nevari darīt vairāk šodien. / No more actions today.")
        return

    user["действия"] += 1

    if action == "rest":
        user["энергия"] = min(user["энергия"] + 5, 10)
        await update.message.reply_text("😴 Tu atpūties / You rested.")
    elif action == "hunt":
        food = random.randint(1, 3)
        water = random.randint(0, 1)
        user["еда"] += food
        user["вода"] += water
        user["энергия"] -= 2
        user["жизнь"] -= 2
        await update.message.reply_text(f"🏹 Tu medīji un dabūji {food} ēdienu un {water} ūdeni!")
    elif action == "explore":
        found = random.choices(["еда", "вода", "предмет", "nekas"], weights=[30, 20, 30, 20])[0]
        if found == "еда":
            user["еда"] += 1
            user["энергия"] -= 2
            await update.message.reply_text("🔎 Tu atradi ēdienu!")
        elif found == "вода":
            user["вода"] += 1
            user["энергия"] -= 2
            await update.message.reply_text("🔎 Tu atradi ūdeni!")
        elif found == "предмет":
            item = random.choice(item_names)
            if item not in user["предметы"]:
                user["предметы"].append(item)
                if item == "Bazuка":
                    user["Bazuka"] = True
                await update.message.reply_text(f"🎁 Tu atradi priekšmetu: {item}!")
            else:
                await update.message.reply_text("🎁 Tu atradi priekšmetu, bet tev tas jau ir.")
        else:
            user["энергия"] -= 2
            await update.message.reply_text("🔎 Tu neko neatradi.")
    elif action == "heal":
            healed = 0
            if "Bints" in user["предметы"]:
                user["предметы"].remove("Bints")
                healed = 4
            elif "Zāles" in user["предметы"]:
                user["предметы"].remove("Zāles")
                healed = 4
            else:
                healed = 1

            user["жизнь"] = min(100, user["жизнь"] + healed)
            await update.message.reply_text(f"🩹 Tu esi dziedināts par {healed} dzīvības punktiem!")

# Завершение дня
async def endday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = players.get(update.effective_user.id)
    if not user:
        return
    if user["действия"] == 0:
        await update.message.reply_text("🚫 Tu neko nedarīji! / You did nothing today.")
    user["еда"] -= 2
    user["вода"] -= 1
    user["энергия"] = min(user["энергия"] + 1, 10)
    user["жизнь"] = min(user["жизнь"] + 1, 10)
    user["действия"] = 0
    fact = random.choice(facts)
    await update.message.reply_text(f"📘 Fakts par spēli / Game fact:\n{fact}")
    await update.message.reply_text("🌙 Dienas beigas / Day ended. Izmanto /nextday lai turpinātu.")

# Переход ко следующему дню и ивенты
async def nextday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = players.get(update.effective_user.id)
    if not user:
        return
    user["день"] += 1

    # Проверка на смерть
    if user["вода"] <= 0 or user["еда"] <= -3:
        await update.message.reply_text("💀 Tu nomiri no bada vai slāpēm. / You died of hunger or thirst.")
        players.pop(update.effective_user.id)
        return
    if user["еда"] <= 0 or user["еда"] <= -3:
        await update.message.reply_text("💀 Tu nomiri no bada vai slāpēm. / You died of hunger or thirst.")
        players.pop(update.effective_user.id)
        return
    if user["жизнь"] <= 0:
        await update.message.reply_text("💀 Tu nomiri. / You died.")
        players.pop(update.effective_user.id)
        return
    if user["день"] > 30:
        await update.message.reply_text("🎉 Tu izdzīvoji 30 dienas! / You survived 30 days!")
        players.pop(update.effective_user.id)
        return
    if user["энергия"] <= 0:
        await update.message.reply_text("💀 Tu nomiri. / You died.")
        players.pop(update.effective_user.id)
        return
    "энергия"
    # Ивенты
    event = random.choices(["дождь", "лев", "оползень", "ничего",], weights=[40, 20, 3, 37])[0]
    msg = f"🗓 Dienas {user['день']} sākums\n"

    if event == "дождь":
        user["вода"] += 2
        msg += "🌧 Līst lietus — tu ieguvi +2 ūdeni!"
    elif event == "лев":
        if "Telts" in user["предметы"]:
            msg += "🦁 Lauva uzbruka, bet tava teltī tevi pasargāja. Tu ieguvi ēdienu un iespējams apģērbu!"
            user["еда"] += 2
            user["предметы"].remove("Telts")
            if random.random() < 0.5:
                user["предметы"].append("lauvas āda")
        else:
            msg += "🦁 Lauva uzbruka! Tu cieti un ieguvi kaut ko...\n"
            user["жизнь"] -= 4
            user["еда"] += 1
            if random.random() < 0.3:
                user["предметы"].append("lauvas āda")
    elif event == "оползень":
        user["жизнь"] -= 5
        user["вода"] -= 2
        user["еда"] -= 2
        user["предметы"] = []
        msg += "🏔 Notika noslīdējums! Tu pazaudēji gandrīz visu!"
    else:
        msg += "☀️ Nekas nenotika šodien."

    await update.message.reply_text(msg)

# Запуск
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("rest", rest))
    app.add_handler(CommandHandler("hunt", hunt))
    app.add_handler(CommandHandler("explore", explore))
    app.add_handler(CommandHandler("endday", endday))
    app.add_handler(CommandHandler("nextday", nextday))
    app.add_handler(CommandHandler("heal", heal))

    app.run_polling()

if __name__ == "__main__":
    main()
