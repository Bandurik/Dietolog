import schedule
import time
from telegram import Bot
from database import session, User, update_current_week, update_last_menu_sent
from config import TELEGRAM_TOKEN
from menu import MenuLoaderNewStructure  # Импортируем новый загрузчик меню
import datetime

bot = Bot(token=TELEGRAM_TOKEN)
menu_loader = MenuLoaderNewStructure()
stop_scheduler_flag = False

def send_reminder():
    users = session.query(User).filter_by(subscribed=True).all()
    for user in users:
        bot.send_message(chat_id=user.chat_id, text="Напоминание о приёме пищи!")

def send_daily_menu():
    users = session.query(User).filter_by(subscribed=True).all()
    for user in users:
        if user.subscription_end and user.subscription_end > datetime.datetime.now():
            current_week = user.current_week or 1
            current_day = (datetime.datetime.now().weekday() + 1)
            menu_for_day = menu_loader.get_menu_for_day(f'Неделя {current_week}', f'День {current_day}')
            message = f"Ваше меню на сегодня:\n\n"
            for meal, description in menu_for_day.items():
                message += f"{meal}: {description}\n"
            bot.send_message(chat_id=user.chat_id, text=message)

def send_weekly_menu():
    users = session.query(User).filter_by(subscribed=True).all()
    for user in users:
        if user.subscription_end and user.subscription_end > datetime.datetime.now():
            current_week = user.current_week or 1
            menu_for_week = menu_loader.get_menu_for_week(f'Неделя {current_week}')
            message = f"Ваше меню на неделю {current_week}:\n\n"
            for day, menu in menu_for_week.items():
                message += f"{day}:\n"
                for meal, description in menu.items():
                    message += f"{meal}: {description}\n"
                message += "\n"
            bot.send_message(chat_id=user.chat_id, text=message)
            update_current_week(user.chat_id, current_week + 1)
            update_last_menu_sent(user.chat_id, datetime.datetime.now())

def start_scheduler():
    global stop_scheduler_flag
    schedule.every().day.at("08:00").do(send_reminder)
    schedule.every().day.at("12:00").do(send_reminder)
    schedule.every().day.at("18:00").do(send_reminder)
    schedule.every().day.at("07:00").do(send_daily_menu)
    schedule.every().sunday.at("18:00").do(send_weekly_menu)
    
    while not stop_scheduler_flag:
        schedule.run_pending()
        time.sleep(1)

def stop_scheduler():
    global stop_scheduler_flag
    stop_scheduler_flag = True
