import time
import schedule
from datetime import datetime
from jobs_scraper import setup_job_vault, hunt_for_jobs, save_to_vault


def autonomous_mission():
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"\n[SYSTEM CLOCK: {current_time}] Waking up ghost browser...")


def autonomous_mission():
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"\n[SYSTEM CLOCK: {current_time}] Waking up ghost browser...")
    live_data = hunt_for_jobs()
    save_to_vault(live_data)
    print(
        f"[SYSTEM CLOCK: {datetime.now().strftime('%H:%M:%S')}] Mission complete. Returning to sleep mode.\n"
    )


def engage_autopilot():
    print("Initiating Autopilot Sequence...")
    setup_job_vault()
    schedule.every(10).seconds.do(autonomous_mission)  # schedule.every().day.at("08:00")

    print("Autopilot engaged. Waiting for the first scheduled run...")
    print("Press Ctrl+C on your keyboard to kill the engine.\n")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    engage_autopilot()
