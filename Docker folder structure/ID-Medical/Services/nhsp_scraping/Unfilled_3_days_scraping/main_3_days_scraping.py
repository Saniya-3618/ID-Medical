from selenium import webdriver
from selenium.webdriver.common.by import By

# for firefox browser
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from bs4 import BeautifulSoup
import pandas as pd

import time
import os
import shutil
import glob
from datetime import datetime, timedelta
import json
import sys
import traceback
from pytz import timezone 
from common_3_days_scraping import Constants, Tasks

import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# import asyncio
from apscheduler.schedulers.background import BackgroundScheduler

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

class NHSPPortalScraping():
    def __init__(self):
        self.name = "worker__3_days_scraping"
        self.log_file = datetime.now(timezone('Asia/Kolkata')).strftime(os.path.join(Constants.EXECUTION_LOGS_FOLDER, Constants.EXECUTION_LOGS_FILENAME))
        configure_logger(self.name, self.log_file)
    
    def scraping():
                
        # #logging formatter to change log time according to timezone
        # logging.Formatter.converter = lambda *args: datetime.now(timezone('Asia/Kolkata')).timetuple()
        # logging.basicConfig(level=logging.INFO, 
        #             filename=datetime.now(timezone('Asia/Kolkata')).strftime(os.path.join(Constants.EXECUTION_LOGS_FOLDER, Constants.EXECUTION_LOGS_FILENAME)), 
        #             filemode='w', format='%(asctime)s - [%(threadName)s] [%(levelname)s] - %(message)s',
        #             datefmt='%d-%b-%y %H:%M:%S')
        try:
            start_time = time.time()
            logger.info(f'NHSP Portal Scraping Started')

            # for firefox browser
            options = FirefoxOptions()
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.dir", Constants.EXPORT_EXCEL_DOWNLOAD_PATH)
            # options.set_preference("browser.download.manager.showWhenStarting", False)
            # options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
            options.add_argument('-headless')
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            # driver = webdriver.Firefox()
            
            # minimize the window size to view the requirements in the cards format
            window_size = driver.get_window_size()
            window_width = window_size['width'] - ((window_size['width']/100) * 20)
            window_height = window_size['height'] - ((window_size['height']/100) * 7)
            driver.set_window_size(window_width, window_height)
            
            driver.get(Constants.PORTAL_LINK)
            logger.info(f'login page opened')
            
            username = driver.find_element(By.ID, Constants.USERNAME_FIELD_ID)
            username.clear()
            username.send_keys(Constants.PORTAL_CREDENTIALS['username'])

            password = driver.find_element(By.ID, Constants.PASSWORD_FIElD_ID)
            password.clear()
            password.send_keys(Constants.PORTAL_CREDENTIALS['password'])

            login = driver.find_element(By.ID, Constants.LOGIN_BUTTON_ID)
            login.click()

            logger.info(f'clicked Login')
            time.sleep(30)
            
            # click on the next 3 days tab
            logger.info(f'checking for the navigation panel')
            navbar = driver.find_element(By.ID, Constants.NAVIGATION_PANEL_DIV_ID)
            logger.info(f'navigation panel found and checking for the next 3 days tab')
            next_3_days_tab = navbar.find_element(By.LINK_TEXT, Constants.NEXT_3_DAYS_TAB_NAME)
            next_3_days_tab.click()
            logger.info(f'clicked on the next 3 days tab')
            time.sleep(5)
            
            # open the filtering option
            logger.info(f'opening the filter option panel')
            filter_menu_element = driver.find_element(By.XPATH, Constants.FILTER_MENU_XPATH)
            filter_menu_element.click()
            time.sleep(5)

            # select the filtering option - status (unfilled)
            logger.info(f'selecting the filtering option - status (unfilled)')
            filter_status_unfilled_option_element = driver.find_element(By.XPATH, Constants.FILTER_STATUS_UNFILLED_OPTION_XPATH)
            filter_status_unfilled_option_element.click()
            time.sleep(10)

            # select the filtering option - authorisation (all)
            logger.info(f'selecting the filtering option - authorisation (all)')
            filter_authorisation_all_option_element = driver.find_element(By.XPATH, Constants.FILTER_AUTHORISATION_ALL_OPTION_XPATH)
            filter_authorisation_all_option_element.click()
            time.sleep(10)

            # TAKE SCREENSHOT OF SELECTED FILTERING OPTIONS
            # driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.PROJECT_PATH + Constants.EXECUTION_SCREENSHOTS_FOLDER, '3_days_01_filter_selections_%d_%m_%Y_%H_%M_%S.png')))    #on local
            driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.EXECUTION_SCREENSHOTS_FOLDER, '3_days_01_filter_selections_%d_%m_%Y_%H_%M_%S.png')))   #on docker

            # close the filtering option
            logger.info(f'closing the filter option panel')
            filter_menu_element = driver.find_element(By.XPATH, Constants.FILTER_MENU_XPATH)
            filter_menu_element.click()
            time.sleep(5)

            # get the list of .xlsx files from the download folder before exporting the excel
            logger.info(f'getting the list of .xlsx files from downloads before exporting excel')
            list_of_files_before_download = glob.glob(Constants.EXPORT_EXCEL_DOWNLOAD_PATH + '*.xlsx')

            # export the excel
            logger.info(f'clicking on the export option')
            export_element = driver.find_element(By.XPATH, Constants.EXPORT_BUTTON_XPATH)
            export_element.click()
            time.sleep(3)
            
            excel_element = driver.find_element(By.XPATH, Constants.EXPORT_EXCEL_OPTION_XPATH)
            excel_element.click()
            time.sleep(10)
            
            # scroll the page to the end of the list (infinite scroll)
            logger.info(f'scrolling the page down (infinite scrolling)')
            Tasks.infinite_scroll(driver)
            logger.info(f'completed scrolling the page down (infinite scrolling)')

            # TAKE SCREENSHOT AFTER THE INFINITE SCROLLING
            # driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.PROJECT_PATH + Constants.EXECUTION_SCREENSHOTS_FOLDER, '3_days_02_infinite_scrolling_%d_%m_%Y_%H_%M_%S.png')))
            driver.get_screenshot_as_file(datetime.now(timezone('Asia/Kolkata')).strftime(os.path.join( Constants.EXECUTION_SCREENSHOTS_FOLDER, '3_days_02_infinite_scrolling_%d_%m_%Y_%H_%M_%S.png'))) #for docker
            
            # get all cards elements after scrolling
            logger.info(f'getting the all cards details div from the page')
            content = driver.page_source
            soup = BeautifulSoup(content, features="html.parser")
            div_element = soup.find('div', attrs={'id':Constants.SHIFT_REQUIREMENTS_DIV_ID})

            # get new exported file name and move it
            logger.info(f'getting the list of the .xlsx files list from the downloads after exporting the excel')
            list_of_files_after_download = glob.glob(Constants.EXPORT_EXCEL_DOWNLOAD_PATH + '*.xlsx')
            exported_excel_file = list(set(list_of_files_after_download).difference(list_of_files_before_download))
            
            logger.info(f'copying the exported excel file from downloads to exported_excel folder')
            if len(exported_excel_file) > 0:
                src_file = exported_excel_file[0]
                
                # file_name = datetime.now().strftime(os.path.join(Constants.EXPORTED_EXCEL_FILENAME))      #on local
                file_name = datetime.now(timezone('Asia/Kolkata')).strftime(os.path.join(Constants.EXPORTED_EXCEL_FILENAME))    #On docker
                # moved_exported_file = os.path.join(Constants.PROJECT_PATH + Constants.EXPORTED_EXCELS_FOLDER, file_name) #uncomment if not on docker
                moved_exported_file = os.path.join( Constants.EXPORTED_EXCELS_FOLDER, file_name)      #for docker
                dst_file = moved_exported_file

                shutil.copy(src_file, dst_file)
            
            # open the exported excel file
            logger.info(f'opening the exported excel file in the pandas dataframe') 
            exported_excel_df = pd.read_excel(exported_excel_file[0], sheet_name=Constants.EXCEL_SHEET_NAME)

            # parse all elements one by one from exported excel and from web page
            # also, create the dataframe to generate the shift requirements excel
            logger.info(f'generating the new empty dataframe to store the shift requirements details')
            df = pd.DataFrame(columns=Constants.EXCEL_COLUMN_HEADERS_LIST)

            logger.info(f'looping on the exported file dataframe')
            for index in range(len(exported_excel_df.index)):
                # check if the row is blank or invalid and skip those rows from excel
                booking_reference_number = str(exported_excel_df.loc[index, Constants.EXCEL_COLUMN_HEADERS_LIST[0]]).strip()
                if booking_reference_number in ['', 'nan'] or 'Date Created' in booking_reference_number:
                    logger.info(f'found the invalid record from the excel dataframe')
                    continue
                
                # adding all required detailes from exported excel datframe to newly generated dataframe
                new_row = {}
                for column in Constants.EXCEL_COLUMN_HEADERS_LIST:
                    new_row[column] = str(exported_excel_df.loc[index, column]).strip()
                
                # check if A icon is present or not
                try:
                    # formulate card id
                    card_element_id = '3-' + booking_reference_number
                    
                    # get the A icon section from the cards header section
                    card_element = div_element.find('div', attrs={'id':card_element_id})
                    header_element = card_element.find('div', attrs={'class':'isotonHeader'})
                    A_icon_element = header_element.find('i')    # here find returns the value None if the element is not found
                    if A_icon_element == None:
                        new_row[Constants.EXCEL_EXTRA_COLUMN_HEADER] = 0
                    else:
                        new_row[Constants.EXCEL_EXTRA_COLUMN_HEADER] = 1
                except:
                    logger.info(f'In Exception, card element not found. booking_reference_number = {booking_reference_number}')
                
                # insert the new row in the dataframe of shift requirements excel
                df = df.append(new_row, ignore_index=True)
            
            logger.info(f'creating the shift requirements excel files')
            # file_name = datetime.now().strftime(os.path.join(Constants.SHIFT_REQUIREMENTS_EXCEL_FILENAME))    #on local
            file_name = datetime.now(timezone('Asia/Kolkata')).strftime(os.path.join(Constants.SHIFT_REQUIREMENTS_EXCEL_FILENAME))  #on docker
            # shift_requirements_file = os.path.join(Constants.PROJECT_PATH + Constants.SHIFT_REQUIREMENTS_EXCELS_FOLDER, file_name) #on local
            shift_requirements_file = os.path.join( Constants.SHIFT_REQUIREMENTS_EXCELS_FOLDER, file_name) #for docker
            df.to_excel(shift_requirements_file, sheet_name=Constants.EXCEL_SHEET_NAME, index=False)

            logger.info(f'creating the requirements excel file to check the cancellation')
            # requirements_file_name = datetime.now().strftime(os.path.join(Constants.SHIFT_REQUIREMENTS_EXCEL_FILENAME))   #on local
            requirements_file_name = datetime.now(timezone('Asia/Kolkata')).strftime(os.path.join(Constants.SHIFT_REQUIREMENTS_EXCEL_FILENAME))     #on docker
            
            requirements_file = os.path.join(Constants.REQUIREMENTS_FOR_COMPARE_EXCEL_PATH, requirements_file_name)
            df.to_excel(requirements_file, sheet_name=Constants.EXCEL_SHEET_NAME, index=False)

            logger.info(f'adding record in the execution summary file')
            requirements_summary_df = pd.read_excel(Constants.REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_FILE_PATH, sheet_name=Constants.REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_EXCEL_SHEET_NAME)
            ## on local
            # new_summary_row = {Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[0]: datetime.now().strftime('%d/%m/%Y'), 
            #                    Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[1]: datetime.now().strftime('%H:%M:%S'), 
            #                    Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[2]: requirements_file_name, 
            #                    Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]: 'no', 
            #                    Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[4]: ''
            #                    } 
            ## on docker
            new_summary_row = {Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[0]: datetime.now(timezone('Asia/Kolkata')).strftime('%d/%m/%Y'), 
                               Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[1]: datetime.now(timezone('Asia/Kolkata')).strftime('%H:%M:%S'), 
                               Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[2]: requirements_file_name, 
                               Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]: 'no', 
                               Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[4]: ''
                               } 
            
            requirements_summary_df = requirements_summary_df.append(new_summary_row, ignore_index=True)
            requirements_summary_df.to_excel(Constants.REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_FILE_PATH, sheet_name=Constants.REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_EXCEL_SHEET_NAME, index=False)

            # logout the portal
            logger.info(f'checking and clicking on the logout navigation menu panel')
            navigation_menu_dropdown_element = driver.find_element(By.ID, Constants.LOGOUT_NAVIGATION_DROPDOWN_MENU_ID)
            navigation_menu_dropdown_element.click()
            time.sleep(1)
            
            logger.info(f'clicking on the logout menu button')
            navigation_menu_element = driver.find_element(By.ID, Constants.LOGOUT_NAVIGATION_MENU_ID)
            logout_element = navigation_menu_element.find_element(By.LINK_TEXT, Constants.LOGOUT_OPTION_NAME)
            logout_element.click()
            time.sleep(5)
            
            logger.info(f'logout completed')

            driver.close()
            driver.quit()
            logger.info(f'closed the browser window')

            end_time = time.time()
            total_time = end_time - start_time
            logger.info(f'Time required for the execution is {total_time}')

            logger.info(f'NHSP Portal Scraping Completed')
            remove_file_handler_logger()
        except Exception:
            try:
                # TAKE SCREENSHOT AFTER ERROR
                # driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.PROJECT_PATH + Constants.EXECUTION_SCREENSHOTS_FOLDER, '3_days_after_error_occured_%d_%m_%Y_%H_%M_%S.png')))
                driver.get_screenshot_as_file(datetime.now(timezone('Asia/Kolkata')).strftime(os.path.join( Constants.EXECUTION_SCREENSHOTS_FOLDER, '3_days_after_error_occured_%d_%m_%Y_%H_%M_%S.png')))  #for docker
                driver.close()
                driver.quit()
            except:
                logger.info(f'Inside the exception of capture error screenshot, drive not initialised')
                
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
        return


                  
                
class ArchiveFiles():
    def __init__(self):

        self.name = "worker__delete_files"
        self.log_file = datetime.now(timezone('Asia/Kolkata')).strftime(os.path.join(Constants.EXECUTION_LOGS_FOLDER, Constants.EXECUTION_LOGS_FILENAME))
        configure_logger(self.name, self.log_file)
        
    def delete_files_based_on_date():
        ### modify paths, store in list        
        ######modify file list
        for directory in Constants.DELETE_FILES_DIRECTORY_LIST:
            # threshold_date = datetime.now() - timedelta(days=Constants.DAYS_THRESHOLD) #on local
            # threshold_date = datetime.now(timezone('Asia/Kolkata')) - timedelta(days=Constants.DAYS_THRESHOLD)  #on dockerr
            threshold_date = datetime.now() - timedelta(days=Constants.DAYS_THRESHOLD)  #on dockerr
            print('before',threshold_date)
            
            # threshold_date = threshold_date - timedelta(hours=5, minutes=30)
            # print('directory= ',directory, threshold_date)
                        
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
                print('creation_time= ',creation_time, ' threshold_date= ',threshold_date)
                # print('file_path= ',file_path)
                # now = time.time()
                # cutoff = now - (Constants.DAYS_THRESHOLD * 86400)  # Convert days to seconds

                if creation_time < threshold_date:
                    try:
                        # print('creation_time= ',creation_time, ' threshold_date= ',threshold_date)
                        os.unlink(file_path)
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")
                        
            


# import docker
# import re
# from datetime import datetime

# def delete_files_created_before(container_id, days_threshold):
#     client = docker.from_env()
    
#     try:
#         container = client.containers.get(container_id)
#         # Command to list files and their creation dates in the container
#         cmd = "find /app/3_days_requirements_excels/unfilled -type f -printf '%T+ %p\n'"
        
#         # Execute the command inside the container
#         exec_result = container.exec_run(cmd)
        
#         # Get the output of the command
#         output = exec_result.output.decode("utf-8")
#         print('output= ',output)
        
#         # Split the output into lines
#         lines = output.split('\n')
#         print('lines= ',len(lines))
#         # Filter files based on creation date
#         count = 0
#         for line in lines:
#             parts = line.split(' ', 1)
#             print('parts= ',parts)
            
#             if len(parts) == 2:
#                 creation_date_str, file_path = parts
#                 creation_date = datetime.strptime(creation_date_str[:26], '%Y-%m-%d+%H:%M:%S.%f')
#                 # Calculate the threshold date
#                 threshold_date = datetime.now() - timedelta(days=days_threshold)
#                 print('threshold_date= ',threshold_date)
                
#                 if creation_date < threshold_date:
#                     # # Delete the file
#                     exec_command = f"rm -f {file_path}"
#                     container.exec_run(exec_command)
#                     print(f"Deleted: {file_path}")
#                     print('count= ',count)
#                     count+=1
                    
                    
#     except docker.errors.NotFound:
#         print(f"Container {container_id} not found.")
#     except docker.errors.APIError as e:
#         print(f"Error executing command in container: {e}")

# # # Example usage
# # container_id = "your_container_id"
# # days_threshold = 15  # Delete files created more than 30 days ago

# # delete_files_created_before(container_id, days_threshold)

# # Example usage
# container_id = "b435111028c3aa4e5d7d55ace03ac98817123969d839e6357c779f8d72aa1943"
# file_path = "/app/3_days_requirements_excels/unfilled/"
# days_threshold = 15  # Delete files created more than 30 days ago

# delete_files_created_before(container_id, days_threshold)



    # # Replace 'your_folder_path' with the actual path to your folder
    # folder_path = 'D:\\EPI_Saniya\\Id-Medical_old\\Services\\nhsp_scraping\\Unfilled_3_days_scraping\\execution_logs\\'
    # todays_files_content = read_log_files(folder_path, today)


# if __name__ == "__main__":
#     # uvicorn.run("main_3_days_scraping:app", host='172.16.16.75', port=9001)
#     uvicorn.run("main_3_days_scraping:app", host='0.0.0.0', port=9000)


    
# if __name__ == '__main__':
            
    # NHSPPortalScraping.scraping()
