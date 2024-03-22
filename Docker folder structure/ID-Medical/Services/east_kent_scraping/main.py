
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from datetime import datetime
import time
import logging

# from scraping_3_days.main_3_days_scraping import NHSPPortalScraping
from main_28_days_scraping import RequirementScraping, RequirementCancellation
import json
import sys
import traceback
from pytz import timezone

logger = logging.getLogger('main')

def setup_base_logger():
    print("in main logger config")
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
        logger.info(f'Started the main program')
        logger.info(f'in startup event')
        # Start the scheduler
        scheduler.start()
        yield
        logger.info(f'in shutdown event')
        # Stop the scheduler
        scheduler.shutdown() 
    except KeyboardInterrupt as e:
        print('keyborad interupted')
        # Stop the scheduler
        scheduler.shutdown()
        
app = FastAPI(lifespan=lifespan)

# Create an instance of the BackgroundScheduler
scheduler = BackgroundScheduler()

# @scheduler.scheduled_job(trigger=IntervalTrigger(seconds=60), id='basic_task')
# def my_scheduled_task():
#     logger.info(f'Scheduled task executed at: {datetime.now()}')


@scheduler.scheduled_job(trigger=IntervalTrigger(minutes=1), id='scraping_28_days')
def task_28_days_scraping():
    
    scheduler.remove_job('scraping_28_days')
    logger.info(f'Scrapping task started at: {datetime.now()}')
    start_time = time.time() 
    
    RequirementScraping()
    RequirementScraping.scraping_requirements()  
    # RequirementCancellation.cancelled_requirements()
    
    logger.info(f'Scrapping task ended at: {datetime.now()}')
    
    end_time = time.time()
    total_time = end_time - start_time
    logger.info(f'Total time required for the execution is {total_time}')        
    
    
    scheduler.add_job(task_28_days_scraping, trigger=IntervalTrigger(minutes=2), id='scraping_28_days')


@app.get("/")
async def root():
    logger.info(f'In the root API')
    return {"message": "In the root API"}


if __name__ == '__main__':
    # print('Starting the main program')
    uvicorn.run(app, host='0.0.0.0', port=8000)  # for higher env
    # uvicorn.run("main:app", host='127.0.0.1', port=8000)  # for local env
    # uvicorn.run(app, host='127.0.0.1', port=8000)
