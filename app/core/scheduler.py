# Scheduler placeholder
import schedule, time, threading


def start_scheduler(job_func):
    schedule.every().day.at("09:00").do(job_func)

    def loop():
        while True:
            schedule.run_pending()
            time.sleep(60)

    threading.Thread(target=loop, daemon=True).start()
