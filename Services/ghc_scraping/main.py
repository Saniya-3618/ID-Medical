import uvicorn
from fastapi import FastAPI
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta

import main_28_days_scraping

from apscheduler.schedulers.background import BackgroundScheduler
import time
from contextlib import asynccontextmanager
import json
import logging
import traceback
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

import sys
from pytz import timezone

   
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
        # logger.info(f'in shutdown event')
        # Stop the scheduler
        scheduler.shutdown()

    except KeyboardInterrupt:
        # Forceful shutdown on KeyboardInterrupt
        scheduler.shutdown(wait=False)     
        
app = FastAPI(lifespan=lifespan)

# Create an instance of the BackgroundScheduler
scheduler = BackgroundScheduler()


@scheduler.scheduled_job(trigger=IntervalTrigger(seconds=30), id='scraping_28_days')
def task_28_days_scraping():
    scheduler.remove_job('scraping_28_days')
    # logger.info(f'Scrapping task started at: {datetime.now()}')
    
    main_28_days_scraping.GHCPortalScraping()
    main_28_days_scraping.GHCPortalScraping.unfilled_req_scraping()
    
    # main_28_days_scraping.NHSPPortalScraping.scraping()
    
    scheduler.add_job(task_28_days_scraping, trigger=IntervalTrigger(seconds=40), id='scraping_28_days')

# @scheduler.scheduled_job(trigger=CronTrigger(hour=18, minute=42), id='delete_files')
# def task_delete_files():
#     scheduler.remove_job('delete_files')
#     logger.info(f'Delete files task started at: {datetime.now()}')
#     print('inside delete job')
    
#     main_28_days_scraping.ArchiveFiles.delete_files_based_on_date()

#     logger.info(f'Delete files task ended at: {datetime.now()}')
    
#     # scheduler.add_job(task_delete_files, trigger=CronTrigger(hour=11, minute=18), id='delete_files')
  
            
if __name__ == "__main__":
    # uvicorn.run("main:app", host='0.0.0.0', port=9000)
    uvicorn.run(app, host='0.0.0.0', port=8000)