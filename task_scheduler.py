import schedule
import time
import datetime
from weekly_generator import generate_weekly_report  # assumes you created this as discussed
from main import main  # assumes you have a main function in main.py that processes daily summaries
def weekly_job():
    print(f"[{datetime.datetime.now()}] Running weekly summary generation...")
    generate_weekly_report("D:\\teams_genai\\venv\\weekly_data")

def daily_job():
    print(f"[{datetime.datetime.now()}] Running daily summary generation...")
    main()
#sample time
schedule.every().day.at("18:52").do(daily_job)
print("Scheduler started. Waiting for daily  job  6.52 PM...")
#sample time
schedule.every().thursday.at("18:53").do(weekly_job)
print("Scheduler started. Waiting for weekly job 6.53 PM...")

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
