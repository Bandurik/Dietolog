import schedule
import time
from telegram import Bot
from database import session, User, update_current_week, update_last_menu_sent
from config import TELEGRAM_TOKEN
from menu import MenuLoaderNewStructure
import datetime

bot = Bot(token=TELEGRAM_TOKEN)
menu_loader_new_structure = MenuLoaderNewStructure()
menu_loader_daily = MenuLoaderDaily('C:/Mytradingapp/menu_new_structure.xlsx')
stop_scheduler_flag = False

def send_reminder(chat_id, message):
    bot.send_message(chat_id=chat_id, text=message)

def send_daily_menu():
    users = session.query(User).filter_by(subscribed=True).all()
    for user in users:
        if user.subscription_end and user.subscription_end > datetime.datetime.now():
            current_day = f'День {datetime.datetime.now().day}'
            menu_for_day = menu_loader_daily.get_menu_for_day(current_day)
            message = f"Ваше меню на сегодня:\n\n"
            for meal, description in menu_for_day.items():
                message += f"{meal}: {description}\n"
            bot.send_message(chat_id=user.chat_id, text=message)

def send_weekly_menu():
    users = session.query(User).filter_by(subscribed=True).all()
    for user in users:
        if user.subscription_end and user.subscription_end > datetime.datetime.now():
            current_week = user.current_week or 1
            menu_for_week = menu_loader_new_structure.get_menu_for_week(f'Неделя {current_week}')
            message = f"Ваше меню на неделю {current_week}:\n\n"
            for day, menu in menu_for_week.items():
                message += f"{day}:\n"
                for meal, description in menu.items():
                    message += f"{meal}: {description}\n"
                message += "\n"
            bot.send_message(chat_id=user.chat_id, text=message)
            update_current_week(user.chat_id, current_week + 1)
            update_last_menu_sent(user.chat_id, datetime.datetime.now())

def send_reminders_for_schedule(schedule_time, message):
    users = session.query(User).filter(User.eating_schedule.like(f'%Пробуждение в {schedule_time}%')).filter_by(subscribed=True).all()
    for user in users:
        send_reminder(user.chat_id, message)

def start_scheduler():
    global stop_scheduler_flag

    # Напоминания для пользователей с пробуждением в 5-00
    schedule.every().day.at("06:30").do(send_reminders_for_schedule, "5-00", "Не забудьте выпить воды!")
    schedule.every().day.at("06:40").do(send_reminders_for_schedule, "5-00", "Не забудьте покушать Завтрак!")
    schedule.every().day.at("09:30").do(send_reminders_for_schedule, "5-00", "Не забудьте выпить воды!")
    schedule.every().day.at("09:40").do(send_reminders_for_schedule, "5-00", "Не забудьте покушать Обед!")
    schedule.every().day.at("12:30").do(send_reminders_for_schedule, "5-00", "Не забудьте выпить воды!")
    schedule.every().day.at("12:40").do(send_reminders_for_schedule, "5-00", "Не забудьте покушать Перекус!")
    schedule.every().day.at("15:30").do(send_reminders_for_schedule, "5-00", "Не забудьте выпить воды!")
    schedule.every().day.at("15:40").do(send_reminders_for_schedule, "5-00", "Не забудьте покушать Ужин!")

    # Напоминания для пользователей с пробуждением в 7-00
    schedule.every().day.at("08:30").do(send_reminders_for_schedule, "7-00", "Не забудьте выпить воды!")
    schedule.every().day.at("08:40").do(send_reminders_for_schedule, "7-00", "Не забудьте покушать Завтрак!")
    schedule.every().day.at("11:30").do(send_reminders_for_schedule, "7-00", "Не забудьте выпить воды!")
    schedule.every().day.at("11:40").do(send_reminders_for_schedule, "7-00", "Не забудьте покушать Обед!")
    schedule.every().day.at("14:30").do(send_reminders_for_schedule, "7-00", "Не забудьте выпить воды!")
    schedule.every().day.at("14:40").do(send_reminders_for_schedule, "7-00", "Не забудьте покушать Перекус!")
    schedule.every().day.at("17:30").do(send_reminders_for_schedule, "7-00", "Не забудьте выпить воды!")
    schedule.every().day.at("17:40").do(send_reminders_for_schedule, "7-00", "Не забудьте покушать Ужин!")

    # Напоминания для пользователей с пробуждением в 9-00
    schedule.every().day.at("09:30").do(send_reminders_for_schedule, "9-00", "Не забудьте выпить воды!")
    schedule.every().day.at("09:40").do(send_reminders_for_schedule, "9-00", "Не забудьте покушать Завтрак!")
    schedule.every().day.at("12:30").do(send_reminders_for_schedule, "9-00", "Не забудьте выпить воды!")
    schedule.every().day.at("12:40").do(send_reminders_for_schedule, "9-00", "Не забудьте покушать Обед!")
    schedule.every().day.at("15:30").do(send_reminders_for_schedule, "9-00", "Не забудьте выпить воды!")
    schedule.every().day.at("15:40").do(send_reminders_for_schedule, "9-00", "Не забудьте покушать Перекус!")
    schedule.every().day.at("18:30").do(send_reminders_for_schedule, "9-00", "Не забудьте выпить воды!")
    schedule.every().day.at("18:40").do(send_reminders_for_schedule, "9-00", "Не забудьте покушать Ужин!")

    schedule.every().day.at("07:00").do(send_daily_menu)
    schedule.every().sunday.at("18:00").do(send_weekly_menu)
    
    while not stop_scheduler_flag:
        schedule.run_pending()
        time.sleep(1)

def stop_scheduler():
    global stop_scheduler_flag
    stop_scheduler_flag = True

if __name__ == "__main__":
    start_scheduler()
