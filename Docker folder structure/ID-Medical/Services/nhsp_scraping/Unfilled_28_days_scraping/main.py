import uvicorn
from fastapi import FastAPI
from typing import List
from datetime import datetime

import main_28_days_scraping
# import main_28_days
import asyncio
# import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
import time
from contextlib import asynccontextmanager
import logging
import traceback
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

from pytz import timezone

# scheduler = BackgroundScheduler()

# def scrape_website_28_days_unfilled():
    
#         print("start Scheduler of Scraping website for 28 days ...")
#         # Your scraping logic here
#         main_28_days_scraping.NHSPPortalScraping.scraping_requirements()
        
#         # time.sleep(120)             # Simulating a scraping task taking 7 minutes
#         print("Scraping complete for 28 days") 


# # scheduler.add_job(scrape_website_3_days_unfilled,'interval',minutes=4, id='job_1', next_run_time=datetime.now())
# scheduler.add_job(scrape_website_28_days_unfilled,'interval',hours=2, minutes=30, id='job_2', next_run_time=datetime.now())       
           

logger = logging.getLogger('main')

def setup_base_logger():
    logfile = "worker__main.log"
    logging.Formatter.converter = lambda *args: datetime.now(timezone('Asia/Kolkata')).timetuple()
    formatter = logging.Formatter(fmt='%(asctime)s - [%(threadName)s] [%(levelname)s] - %(message)s',
                                  datefmt='%d-%b-%y %H:%M:%S')
    file_handler = logging.FileHandler(logfile, mode='w')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.setLevel(logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        setup_base_logger()
        # logger.info(f'Started the main program')
        # logger.info(f'in startup event')
        # Start the scheduler
        scheduler.start()

        yield
        logger.info(f'in shutdown event')
        # Stop the scheduler
        scheduler.shutdown()

    except KeyboardInterrupt:
        # Forceful shutdown on KeyboardInterrupt
        scheduler.shutdown(wait=False)     
        
app = FastAPI(lifespan=lifespan)
         
# Create an instance of the BackgroundScheduler
scheduler = BackgroundScheduler()


@scheduler.scheduled_job(trigger=IntervalTrigger(minutes=15), id='scraping_28_days')
def task_28_days_scraping():
    scheduler.remove_job('scraping_28_days')
    # logger.info(f'Scrapping task started at: {datetime.now()}')
    
    main_28_days_scraping.NHSPPortalScraping()
    main_28_days_scraping.NHSPPortalScraping.scraping_requirements()
    # main_28_days.NHSPPortalScraping()
    # main_28_days.NHSPPortalScraping.scraping_requirements()
                     
    # NHSPPortalScraping.scraping()
    # logger.info(f'Scrapping task ended at: {datetime.now()}')
    scheduler.add_job(task_28_days_scraping, trigger=IntervalTrigger(minutes=15), id='scraping_28_days')
 
# @scheduler.scheduled_job(trigger=CronTrigger(hour=11, minute=18), id='delete_files')
@scheduler.scheduled_job(trigger='cron', day_of_week='thu', hour=12, minute=45, id='delete_files')
def task_delete_files():
    scheduler.remove_job('delete_files')
    logger.info(f'Delete files task started at: {datetime.now()}')
    print('inside delete job')
    
    main_28_days_scraping.ArchiveFiles.delete_files_based_on_date()
    # main_28_days.ArchiveFiles.delete_files_based_on_date()
    logger.info(f'Delete files task ended at: {datetime.now()}')
    
    scheduler.add_job(task_delete_files, trigger=CronTrigger(hour=11, minute=18), id='delete_files')
    
     
    
if __name__ == "__main__":
    # uvicorn.run("main:app", host='0.0.0.0', port=9000)
    uvicorn.run(app, host='0.0.0.0', port=8002)
    
   
    

"""

# @app.on_event('startup')
# def start_3_days_unfilled_scraping_scheduler():
#     try:
#         # job=scheduler.add_job(scrape_website,'cron',day_of_week='mon-fri', hour=10, minute=9,id='my_job_id')
#         job=scheduler.add_job(scrape_website_3_days_unfilled,'interval',minutes=4, next_run_time=datetime.now())
#         scheduler.start()

#         # while True: 
#         #     print("inside while...")
#         #     time.sleep(120) 
            
#     except KeyboardInterrupt:
#         # Forceful shutdown on KeyboardInterrupt
#         print("Forceful shutdown...")
#         scheduler.shutdown(wait=False)     
        
        
# @app.on_event('startup') 
# def start_28_days_unfilled_scraping_scheduler():
#     try:
#         # job=scheduler.add_job(scrape_website,'cron',day_of_week='mon-fri', hour=10, minute=9,id='my_job_id')
#         job=scheduler2.add_job(scrape_website_28_days_unfilled,'interval',hours=2, minutes=30, next_run_time=datetime.now())
#         scheduler2.start()

#         # while True: 
#         #     print("inside while...")
#         #     time.sleep(120) 
            
#     except KeyboardInterrupt:
#         # Forceful shutdown on KeyboardInterrupt
#         print("Forceful shutdown...")
#         scheduler2.shutdown(wait=False)     
        
        
        
# @app.on_event('shutdown')
# def stop_scheduler():
#     print("Scraping 1 STOPED...")
#     # Shut down the scheduler gracefully on application shutdown
#     scheduler.shutdown()    
#     scheduler2.shutdown()  
#     print("Scraping 2 STOPED...") 

"""