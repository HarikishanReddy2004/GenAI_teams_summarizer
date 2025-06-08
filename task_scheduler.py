import schedule
import time
import datetime
from weekly_generator import generate_weekly_report  # assumes you created this as discussed

def job():
    print(f"[{datetime.datetime.now()}] Running weekly summary generation...")
    generate_weekly_report()

# Schedule the job every Friday at 5:00 PM
schedule.every().friday.at("17:00").do(job)

print("Scheduler started. Waiting for Friday 5 PM...")

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
