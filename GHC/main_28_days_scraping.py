from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, InvalidSessionIdException

# for firefox browser
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

import time
from common_28_days_scraping import Constants
from datetime import datetime, timedelta
import pandas as pd
import logging
from pytz import timezone
import os
import json
import sys
import traceback
import shutil
import glob

# global logger variable
logger = None
file_handler = ''

def configure_logger(name, logfile):
    global logger, file_handler
    logger = logging.getLogger(name)
    logging.Formatter.converter = lambda *args: datetime.now(timezone('Asia/Kolkata')).timetuple()
    formatter = logging.Formatter(fmt='%(asctime)s - [%(threadName)s] [%(levelname)s] - %(message)s',
                                  datefmt='%d-%b-%y %H:%M:%S')
    file_handler = logging.FileHandler(logfile, mode='w')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

def remove_file_handler_logger():
    logger.removeHandler(file_handler)
    
# #logging formatter to change log time according to timezone
# logging.Formatter.converter = lambda *args: datetime.now(timezone('Asia/Kolkata')).timetuple()
# logging.basicConfig(level=logging.INFO, 
#             filename=datetime.now(timezone('Asia/Kolkata')).strftime(os.path.join(Constants.EXECUTION_LOGS_FOLDER, Constants.EXECUTION_LOGS_FILENAME)), 
#             filemode='w', format='%(asctime)s - [%(threadName)s] [%(levelname)s] - %(message)s',
#             datefmt='%d-%b-%y %H:%M:%S')
 
# logging.Formatter.converter = lambda *args: datetime.now().timetuple()
# logging.basicConfig(level=logging.INFO, 
#             filename=datetime.now().strftime(os.path.join(Constants.EXECUTION_LOGS_FOLDER, Constants.EXECUTION_LOGS_FILENAME)), 
#             filemode='w', format='%(asctime)s - [%(threadName)s] [%(levelname)s] - %(message)s',
#             datefmt='%d-%b-%y %H:%M:%S')

class GHCPortalScraping():
    def __init__(self):
        self.name = "worker__3_days_scraping"
        self.log_file = datetime.now(timezone('Asia/Kolkata')).strftime(os.path.join(Constants.EXECUTION_LOGS_FOLDER, Constants.EXECUTION_LOGS_FILENAME))
        configure_logger(self.name, self.log_file)
    
    def unfilled_req_scraping():
        try:
            start_time = time.time()
            logger.info(f'GHC portal scraping started.')
            
            options = FirefoxOptions()
            
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.dir", Constants.EXPORT_REQUIREMENT_EXCEL_DOWNLOAD_PATH)
            options.set_preference("browser.download.manager.showWhenStarting", False)
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
            options.add_argument('-headless')
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            # driver = webdriver.Firefox()
                  
            # list_of_files_before_download = glob.glob(Constants.EXPORT_REQUIREMENT_EXCEL_DOWNLOAD_PATH + '*.xls')
            # print('before download = ',len(list_of_files_before_download)) 
                                     
            driver.get(Constants.PORTAL_LINK)
            time.sleep(2)
            logger.info(f'Login page opened.')
            
            username = driver.find_element(By.ID, Constants.USERNAME_ELEMENT_ID)
            username.clear()
            username.send_keys(Constants.PORTAL_CREDENTIALS['username'])
            time.sleep(2)
            
            password = driver.find_element(By.ID, Constants.PASSWORD_ELEMENT_ID)
            password.clear()
            password.send_keys(Constants.PORTAL_CREDENTIALS['password'])
            time.sleep(2)
            
            login_btn = driver.find_element(By.ID, Constants.LOGIN_BUTTON_ELEMENT_ID)
            login_btn.click()
            time.sleep(5)
            logger.info(f'Login button clicked.')
            
            click_select_filter = driver.find_element(By.ID, Constants.FILTER_FIELD_ELEMENT_ID)
            click_select_filter.click()
            time.sleep(2)
            logger.info(f'Clicked on filter settings.')
            
            select_next_28_days = driver.find_element(By.ID, Constants.NEXT_28_DAYS_OPTION_ELEMENT_ID)
            select_next_28_days.send_keys('Next 28 Days')
            time.sleep(3)
            logger.info(f'Selected "Next 28 Days" period option.')
            
            submit_filter = driver.find_element(By.ID, Constants.SUBMIT_FILTER_BUTTON_ID)
            submit_filter.click()
            time.sleep(10)
            logger.info(f'Filter submitted.')
            
            list_of_unfilled_req_files_before_download = glob.glob(Constants.EXPORT_REQUIREMENT_EXCEL_DOWNLOAD_PATH + '*.xls')
            
            # wait until requirements get loaded
            try:
                WebDriverWait(driver, 15).until(EC.invisibility_of_element_located((By.XPATH, Constants.DATA_LOADER_XPATH)))
            except:
                logger.info(f'timeout error occured, waiting for somemore time')
                WebDriverWait(driver, 15).until(EC.invisibility_of_element_located((By.XPATH, Constants.DATA_LOADER_XPATH)))

             # TAKE SCREENSHOT AFTER ERROR
            driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_unfilled_records_%d_%m_%Y_%H_%M_%S.png'))) 
            time.sleep(2)
           
            export_excel_option = driver.find_element(By.ID, Constants.EXPORT_EXCEL_ELEMENT_ID)
            export_excel_option.click()
            time.sleep(15)
            logger.info(f'Excel downloaded successfully.')
            
            # wait until requirements get loaded
            try:
                WebDriverWait(driver, 15).until(EC.invisibility_of_element_located((By.XPATH, Constants.DATA_LOADER_XPATH)))
            except:
                logger.info(f'timeout error occured, waiting for somemore time')
                WebDriverWait(driver, 15).until(EC.invisibility_of_element_located((By.XPATH, Constants.DATA_LOADER_XPATH)))

            list_of_unfilled_req_files_after_download = glob.glob(Constants.EXPORT_REQUIREMENT_EXCEL_DOWNLOAD_PATH + '*.xls')
            unfilled_req_excel_file = list(set(list_of_unfilled_req_files_after_download).difference(list_of_unfilled_req_files_before_download))
            
            if len(unfilled_req_excel_file)>0:
                
                logger.info(f'Unfilled Requirements excel available.')
                unfilled_req_file = unfilled_req_excel_file[0]
                unfilled_req_file_df = pd.read_excel(unfilled_req_file, dtype='object')
                unfilled_req_file_df['Date'] = pd.to_datetime(unfilled_req_file_df['Date']) # convert the column to a datetime object
                unfilled_req_file_df['Date'] = unfilled_req_file_df['Date'].dt.strftime('%d-%b-%Y') # format the object
                # src_file_df['Start'] = pd.to_datetime(src_file_df['Start'], format='%H:%M:%S').dt.strftime('%H:%M') # convert the column to a datetime object
                # src_file_df['End'] = pd.to_datetime(src_file_df['End'], format='%H:%M:%S').dt.strftime('%H:%M')# format the object
            
                file_name = datetime.now().strftime(os.path.join(Constants.EXPORTED_REQUIREMENT_EXCEL_FILENAME))
                unfilled_requirement_file = os.path.join( Constants.REQUIREMENT_EXCEL_FOLDER, file_name)      #for docker
                unfilled_req_file_df.to_excel(unfilled_requirement_file, index=False, engine='openpyxl' )   #, dtype={'Request Id': 'str'}) #, engine='openpyxl')
                
                logger.info(f'Downloaded file moved to unfilled requirements folder.')
                logger.info(f'Unfilled requirements stored in file: {file_name}')
                
            else:
                logger.info(f'No requirements file available.')
                
            time.sleep(2)
            
            ### Scraping Filled Bookings ###
        
            # list_of_filled_req_files_before_download = list_of_files_after_download
            # print('filled req before download = ',len(list_of_filled_req_files_before_download)) 
            
            click_filled_booking = driver.find_element(By.XPATH, Constants.FILLED_BOOKING_OPTION_XPATH)
            click_filled_booking.click()
            time.sleep(3)
            logger.info('Filled Bookings tab clicked.')
            
            click_select_filter = driver.find_element(By.ID, Constants.FILTER_FIELD_ELEMENT_ID)
            click_select_filter.click()
            time.sleep(3)
            logger.info(f'Clicked on filter settings.')
            
            select_next_28_days = driver.find_element(By.ID, Constants.NEXT_28_DAYS_OPTION_ELEMENT_ID)
            select_next_28_days.send_keys('Next 28 Days')
            time.sleep(3)
            logger.info(f'Selected "Next 28 Days" period option.')
            
            submit_filter = driver.find_element(By.ID, Constants.SUBMIT_FILTER_BUTTON_ID)
            submit_filter.click()
            time.sleep(10)
            logger.info(f'Filter submitted.')

            list_of_filled_req_files_before_download = list_of_unfilled_req_files_after_download
            # wait until requirements get loaded
            try:
                WebDriverWait(driver, 15).until(EC.invisibility_of_element_located((By.XPATH, Constants.DATA_LOADER_XPATH)))
            except:
                logger.info(f'timeout error occured, waiting for somemore time')
                WebDriverWait(driver, 15).until(EC.invisibility_of_element_located((By.XPATH, Constants.DATA_LOADER_XPATH)))

            # TAKE SCREENSHOT AFTER ERROR
            driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_filled_records_%d_%m_%Y_%H_%M_%S.png'))) 
            time.sleep(2)
            
            export_excel_option = driver.find_element(By.ID, Constants.EXPORT_EXCEL_ELEMENT_ID)
            export_excel_option.click()
            time.sleep(15)
            logger.info(f'Filled Bookings Excel downloaded successfully.')
            
            # wait until requirements get loaded
            try:
                WebDriverWait(driver, 15).until(EC.invisibility_of_element_located((By.XPATH, Constants.DATA_LOADER_XPATH)))
            except:
                logger.info(f'timeout error occured, waiting for somemore time')
                WebDriverWait(driver, 15).until(EC.invisibility_of_element_located((By.XPATH, Constants.DATA_LOADER_XPATH)))

            list_of_filled_req_files_after_download = glob.glob(Constants.EXPORT_REQUIREMENT_EXCEL_DOWNLOAD_PATH + '*.xls')
            filled_req_exported_excel_file = list(set(list_of_filled_req_files_after_download).difference(list_of_filled_req_files_before_download))
            
            if len(filled_req_exported_excel_file) > 0:
                logger.info(f'Filled Requirements excel available.')
                
                exported_filled_req_file = filled_req_exported_excel_file[0]
                filled_req_file_df = pd.read_excel(exported_filled_req_file, dtype='object')
                filled_req_file_df['Date'] = pd.to_datetime(filled_req_file_df['Date']) # convert the column to a datetime object
                filled_req_file_df['Date'] = filled_req_file_df['Date'].dt.strftime('%d-%b-%Y') # format the object
                # filled_req_file_df['Start'] = pd.to_datetime(filled_req_file_df['Start'], format='%H:%M:%S').dt.strftime('%H:%M') # convert the column to a datetime object
                # filled_req_file_df['End'] = pd.to_datetime(filled_req_file_df['End'], format='%H:%M:%S').dt.strftime('%H:%M')# format the object
                
                filled_req_file_name = datetime.now().strftime(os.path.join(Constants.EXPORTED_FILLED_EXCEL_FILENAME))
                filled_req_file = os.path.join( Constants.EXPORT_FILLED_REQUIREMENT_EXCEL_DOWNLOAD_PATH, filled_req_file_name)   
                filled_req_file_df.to_excel(filled_req_file, index=False)  #, engine='openpyxl')
                logger.info(f'Downloaded file moved to filled requirements folder.')
                logger.info(f'Filled requirements stored in file: {filled_req_file_name}')
                
            else:
                logger.info(f'No requirements file available.')

            time.sleep(2)
            click_logout = driver.find_element(By.XPATH, Constants.LOGOUT_BUTTON_XPATH)
            time.sleep(3)
            click_logout.click()
            time.sleep(5)
            
            driver.close()
            driver.quit()
            
            logger.info(f'Logged out successfully.')
            logger.info('GHC portal scraping completed.')
            remove_file_handler_logger()
            
         
        except Exception:
            try:
                # TAKE SCREENSHOT AFTER ERROR
                driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_after_error_occured_%d_%m_%Y_%H_%M_%S.png'))) 

                driver.close()
                driver.quit()
            except:
                logger.info(f'Inside exception of capturing error screenshot, drive not initialised.')
                
            end_time = time.time()
            total_time = end_time - start_time
            logger.info(f'Time required for the execution is {total_time}')

            exception_type, exception_value, exception_traceback = sys.exc_info()
            traceback_string = traceback.format_exception(exception_type,
                            exception_value, exception_traceback)
            err_msg = json.dumps({
                "errorType": exception_type.__name__,
                "errorMessage": str(exception_value),
                "stackTrace": traceback_string
            })
            logger.error(f'Error Occured: {err_msg}') 
            remove_file_handler_logger()
        
        # finally:
        #     driver.close()
        #     driver.quit()
        #     remove_file_handler_logger()
             
             
class ArchiveFiles():
    def __init__(self):

        self.name = "worker__delete_files"
        self.log_file = datetime.now(timezone('Asia/Kolkata')).strftime(os.path.join(Constants.EXECUTION_LOGS_FOLDER, Constants.EXECUTION_LOGS_FILENAME))
        configure_logger(self.name, self.log_file)
        
    def delete_files_based_on_date():
        ### modify paths, store in list        
        ######modify file list
        for directory in Constants.DELETE_FILES_DIRECTORY_LIST:
            threshold_date = datetime.now() - timedelta(days=Constants.DAYS_THRESHOLD) #on local
            threshold_date1 = datetime.now(timezone('Asia/Kolkata')) - timedelta(days=Constants.DAYS_THRESHOLD)  #on dockerr
            print('directory= ',directory, threshold_date, threshold_date1)
            # logger.info(f'#'*50,'Delete files execution started')
            # logger.info(f'Delete files job executed.')
            # logger.info(f'directory= ',directory, threshold_date)
            # logger.info(f'#'*50,'Delete files execution finished')
            
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
                print('creation_time= ',creation_time, ' threshold_date= ',threshold_date)
                print('file_path= ',file_path)
                # logger.info('creation_time= ',{creation_time}, ' threshold_date= ',{threshold_date})
                # logger.info(f'file_path= ,{file_path}')
                if creation_time < threshold_date:
                    try:
                        os.unlink(file_path)
                        # logger.info(f'Deleted file {file_path}')
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")
                        # logger.error(f'error while deleting file {file_path}: {e}')
             
            

             
# if __name__ == '__main__':
#     GHCPortalScraping.unfilled_req_scraping()         
            
"""          
except TimeoutException:
            # driver.close()
            # driver.quit()
            
            print("Timeout.")
            exception_type, exception_value, exception_traceback = sys.exc_info()
            traceback_string = traceback.format_exception(exception_type,
                            exception_value, exception_traceback)
            err_msg = json.dumps({
                "errorType": exception_type.__name__,
                "errorMessage": str(exception_value),
                "stackTrace": traceback_string
            })
            logger.error(f'Error Occured: {err_msg}') 
            remove_file_handler_logger()
            
        except InvalidSessionIdException:
            driver.close()
            driver.quit()
            
            print("WebDriver session does not exist or is not active. Retrying...")
            exception_type, exception_value, exception_traceback = sys.exc_info()
            traceback_string = traceback.format_exception(exception_type,
                            exception_value, exception_traceback)
            err_msg = json.dumps({
                "errorType": exception_type.__name__,
                "errorMessage": str(exception_value),
                "stackTrace": traceback_string
            })
            logger.error(f'Error Occured: {err_msg}') 
            remove_file_handler_logger()
            
"""