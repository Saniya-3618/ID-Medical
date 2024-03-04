from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
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

# global logger variable
logger = None
file_handler = ''

def configure_logger(name, logfile):
    print("in scraping logger config")
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
    

# logging.Formatter.converter = lambda *args: datetime.now(timezone('Asia/Kolkata')).timetuple()
# logging.basicConfig(level=logging.INFO, 
#         filename=datetime.now(timezone('Asia/Kolkata')).strftime(os.path.join( Constants.EXECUTION_LOGS_FOLDER, Constants.EXECUTION_LOGS_FILENAME)), 
#         filemode='w', format='%(asctime)s - [%(threadName)s] [%(levelname)s] - %(message)s',
#         datefmt='%d-%b-%y %H:%M:%S')
            

class RequirementScraping():
    def __init__(self):
        print("in scraping init")
        self.name = "worker__28_days_scraping"
        self.log_file = datetime.now(timezone('Asia/Kolkata')).strftime(os.path.join( Constants.EXECUTION_LOGS_FOLDER, Constants.EXECUTION_LOGS_FILENAME))
        configure_logger(self.name, self.log_file)
        
    def scraping_requirements():
        start_time = time.time() 
        try:
            
            logger.info(f'East Kent Hospital Requirements Scraping Started.')
            logger.info(f'Excecution start time: {start_time}')
            options = FirefoxOptions()
            
            # options.set_preference("browser.download.folderList", 2)
            # options.set_preference("browser.download.dir", Constants.EXPORT_EXCEL_DOWNLOAD_PATH)
            options.set_preference("browser.download.manager.showWhenStarting", False)
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
            # options.add_argument('-headless')
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            # driver = webdriver.Firefox()
                                                
            driver.get(Constants.PORTAL_LINK)
            
            logger.info(f'login page opened.')
            time.sleep(5)
            
            ## TO CHECK FRAME NAME
            driver.page_source
            ## SWITCH TO FRAME
            driver.switch_to.frame('body')
            time.sleep(5)
                
            username = driver.find_element(By.NAME, Constants.USERNAME_FIELD_ELEMENT_NAME)
            username.clear()
            username.send_keys(Constants.PORTAL_CREDENTIALS['username'])
            time.sleep(2)
            
            password = driver.find_element(By.NAME, Constants.PASSWORD_FIELD_ELEMENT_NAME)
            password.clear()
            password.send_keys(Constants.PORTAL_CREDENTIALS['password'])
            time.sleep(2)
            
            login_btn = driver.find_element(By.NAME, Constants.LOGIN_BUTTON_ELEMENT_NAME)
            login_btn.click()
            time.sleep(10)
            
            driver.switch_to.default_content()
            driver.switch_to.frame('toc')
            time.sleep(2)
                
            view_request=driver.find_element(By.ID, Constants.VIEW_REQUEST_OPTION_ELEMENT_ID)
            view_request.click()
            time.sleep(5)
            logger.info(f'View requests option clicked.')
            
            driver.switch_to.default_content()
            driver.switch_to.frame('content')
            driver.switch_to.frame('MenuDetailsWindow')
            time.sleep(5)
            
            # empty dataframe to store data of all tables
            combined_data = pd.DataFrame() 
            interval_start_date = datetime.now()# + timedelta(days=8)
            name_found = False    
            # Generate time intervals for the next 28 days, every 7 days    
            for index in range(Constants.INTERVAL_ITERATION_RANGE):

                # select_name = driver.find_element(By.NAME, Constants.SELECT_TRUST_NAME_ELEMENT_NAME)
                select_name = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, Constants.SELECT_TRUST_NAME_ELEMENT_NAME)) )
                names = select_name.find_elements(By.TAG_NAME, 'option')
                
                for name in names:
                    # print('select_name=',name.text)
                    agency_name = name.text
                    if str(agency_name) == Constants.TRUST_NAME:
                        # print('name found')
                        # break
                        name_found = True
                        select_name.send_keys(Constants.TRUST_NAME)
                        time.sleep(5)
                        logger.info(f'Trust name "East Kent Hospital" selected from dropdown.')
                                
                        interval_start = (interval_start_date + timedelta(days=index * 7)).strftime('%d/%m/%Y')
                        interval_end = (datetime.strptime(interval_start, '%d/%m/%Y') + timedelta(days=6)).strftime('%d/%m/%Y')
                        logger.info(f'Interval Start: {interval_start}, Interval End: {interval_end}')
                
                        try:
                            # start_date = driver.find_element(By.NAME, Constants.START_DATE_ELEMENT_NAME)
                            start_date = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, Constants.START_DATE_ELEMENT_NAME)))
                            start_date.clear()
                            start_date.send_keys(str(interval_start))
                            time.sleep(2)
                            
                            # end_date = driver.find_element(By.NAME, Constants.END_DATE_ELEMENT_NAME)
                            end_date = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, Constants.END_DATE_ELEMENT_NAME)))
                            end_date.clear()
                            end_date.send_keys(str(interval_end))
                            time.sleep(2)
                            
                        except:
                            # TAKE SCREENSHOT AFTER ERROR
                            driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.PROJECT_PATH + Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_after_error_occured_%d_%m_%Y_%H_%M_%S.png')))#on local
                            
                            logger.info(f'Exception occured due to start and end date field not found.')
                            
                            # back_to_filter_selection = driver.find_element(By.ID, Constants.BACK_BUTTON_ELEMENT_ID)
                            back_to_filter_selection = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, Constants.BACK_BUTTON_ELEMENT_ID)))
                            time.sleep(5)
                            back_to_filter_selection.click()
                            time.sleep(5)
                            logger.info(f'Back button clicked inside exception block.')
                            
                            # select_name = driver.find_element(By.NAME, Constants.SELECT_TRUST_NAME_ELEMENT_NAME)
                            select_name = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, Constants.SELECT_TRUST_NAME_ELEMENT_NAME)))
                            select_name.send_keys(Constants.TRUST_NAME)
                            # select_name.click()
                            time.sleep(3)
                            
                            # start_date = driver.find_element(By.NAME, Constants.START_DATE_ELEMENT_NAME)
                            start_date = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, Constants.START_DATE_ELEMENT_NAME)))
                            start_date.clear()
                            start_date.send_keys(str(interval_start))
                            time.sleep(2)
                            
                            # end_date = driver.find_element(By.NAME, Constants.END_DATE_ELEMENT_NAME)
                            end_date = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, Constants.END_DATE_ELEMENT_NAME)))
                            end_date.clear()
                            end_date.send_keys(str(interval_end))
                            time.sleep(2)
                
                            logger.info(f'Start and end date found.')
                            logger.info(f'Exiting exception block; defined excecution is successfull.')
                        
                        # # TAKE SCREENSHOT AFTER FILTER SELECTION
                        # driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.PROJECT_PATH + Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_filter_selection_%d_%m_%Y_%H_%M_%S.png')))#on local
                        time.sleep(2)
                        
                        # #submit after filter selection
                        submit_filters_btn = driver.find_element(By.NAME, Constants.SUBMIT_BUTTON_ELEMENT_NAME)
                        submit_filters_btn.click()
                        time.sleep(10)
                        
                        logger.info(f'Filter selected and submitted for time interavl: {interval_start}, {interval_end}')
                        time.sleep(5)
                    
                        try:
                            no_record_msg = driver.find_element(By.ID, Constants.RECORD_NOT_FOUND_MSG_ELEMENT_ID) 
                            record_not_found = True
                            logger.info(f'Record not found for selected filter.')
                            time.sleep(5)
                            # TAKE SCREENSHOT AFTER RECORND NOT FOUND
                            driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.PROJECT_PATH + Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_record_not_found_%d_%m_%Y_%H_%M_%S.png')))#on local
                            
                        except:
                            record_not_found = False
                            time.sleep(30)
                        
                        if not record_not_found:  
                            # wait until requirements get loaded
                            try:
                                table_element = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, Constants.TABLE_ELEMENT_ID)))
                            except:
                                logger.info(f'timeout error occured, waiting for somemore time')
                                table_element = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, Constants.TABLE_ELEMENT_ID)))
                            
                            # table_element = driver.find_element(By.ID, Constants.TABLE_ELEMENT_ID)
                            table_html = table_element.get_attribute("outerHTML")
                            table_data = pd.read_html(table_html)[0]
                            time.sleep(2)
                            logger.info(f'Table data scraped.')
                            
                            if combined_data.empty:
                                combined_data = table_data
                                logger.info(f'Table data appended to combined empty dataframe')
                            else:
                                # Append data to the combined DataFrame without repeating column names
                                combined_data = combined_data.append(table_data, ignore_index=True)
                                logger.info(f'Table data appended to combined dataframe.')
                            
                            time.sleep(2)   
                            
                            #back button click
                            back_to_filter_selection = driver.find_element(By.ID, Constants.BACK_BUTTON_ELEMENT_ID)
                            time.sleep(5)
                            # # TAKE SCREENSHOT 
                            # driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.PROJECT_PATH + Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_table_%d_%m_%Y_%H_%M_%S.png')))#on local
                        
                            back_to_filter_selection.click()
                            time.sleep(5)
                            
                            logger.info(f'Back button clicked.')

                        break
                    
                    else:
                        continue
             
             
            if name_found:
                logger.info(f'Records of 28 days scraped successfully.')              
                excel_filename = datetime.now().strftime(os.path.join(Constants.FILE_NAME_OF_SCRAPED_DATA))
                unfilled_requirements_file = os.path.join(Constants.PROJECT_PATH + Constants.REQUIREMENT_EXCEL_FOLDER, excel_filename)
                all_unfilled_requirements_file = os.path.join(Constants.PROJECT_PATH + Constants.UNFILLED_REQUIREMENT_EXCEL_FOLDER, excel_filename)    #on local
                
                filtered_df = combined_data
                filtered_df = filtered_df[Constants.EXCEL_COLUMN_HEADERS_LIST]
                filtered_df = filtered_df.fillna('')
                
                # filtered_df.to_excel(unfilled_requirements_file, index=False)
                filtered_df.to_excel(all_unfilled_requirements_file, index=False) #read by java side
                logger.info(f'Table data stored in excel: {excel_filename}')
            
                # logging.info(f'Adding record in the execution summary file')
                # unilled_requirements_summary_df = pd.read_excel(Constants.UNFILLED_SCRAPING_SUMMARY_FILE_NAME, sheet_name=Constants.SCRAPING_SUMMARY_EXCEL_SHEET_NAME)
                # new_summary_row = {Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[0]: datetime.now().strftime('%d/%m/%Y'), 
                #                     Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[1]: datetime.now().strftime('%H:%M:%S'), 
                #                     Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[2]: excel_filename, 
                #                     Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]: 'no', 
                #                     Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[4]: ''
                #                     }
                # unilled_requirements_summary_df = unilled_requirements_summary_df.append(new_summary_row, ignore_index=True)
                # unilled_requirements_summary_df.to_excel(Constants.UNFILLED_SCRAPING_SUMMARY_FILE_NAME, sheet_name=Constants.SCRAPING_SUMMARY_EXCEL_SHEET_NAME, index=False)
            else:
                logger.info(f'Agency name not found.')
                
                
            driver.switch_to.default_content()
            driver.switch_to.frame('content')
            driver.switch_to.frame('MainMenuWindow')
            
            logout = driver.find_element(By.ID, Constants.LOGOUT_BUTTON_ELEMENT_ID)
            time.sleep(3)
            logout.click()
            time.sleep(2)
            
            logger.info(f'Loged out successfuly.')
            
            driver.close()
            logger.info(f'Driver closed.')
            logger.info(f'Scraping completed successfully.')
              
            end_time = time.time()
            total_time = end_time - start_time
            logger.info(f'Time required for the scraping is: {total_time}')    
            remove_file_handler_logger()
        except Exception:
            try:
                # TAKE SCREENSHOT AFTER ERROR
                # driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.PROJECT_PATH + Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_after_error_occured_%d_%m_%Y_%H_%M_%S.png')))#on local
                driver.get_screenshot_as_file(datetime.now().strftime(os.path.join( Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_after_error_occured_%d_%m_%Y_%H_%M_%S.png')))  #on docker
                
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
            logger.error(f'Error Occured while scraping: {err_msg}')
            
            end_time = time.time()
            total_time = end_time - start_time
            logger.info(f'Time required for the scraping is: {total_time}')    
            remove_file_handler_logger()
        return 
    
  
class RequirementCancellation():

    def cancelled_requirements():
        start_time = time.time()
        try:
            
            # current_date = datetime.now()
            # current_date_str = current_date.strftime('%d/%m/%Y')
            # previous_date = datetime.now() - timedelta(days = 1)
            # previous_date_str = previous_date.strftime('%d/%m/%Y')
            
            # filter the not compared records from the summary dataframe
            unfilled_scraping_summary_excel_df = pd.read_excel(Constants.UNFILLED_SCRAPING_SUMMARY_FILE_NAME, sheet_name=Constants.SCRAPING_SUMMARY_EXCEL_SHEET_NAME)
            filtered_unfilled_scraping_summary_excel_df = unfilled_scraping_summary_excel_df[unfilled_scraping_summary_excel_df[Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]] == 'no']
            # filtered_unfilled_scraping_summary_today_excel_df = filtered_unfilled_scraping_summary_excel_df[filtered_unfilled_scraping_summary_excel_df[Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[0]] == current_date_str]
            # filtered_unfilled_scraping_summary_previous_excel_df = filtered_unfilled_scraping_summary_excel_df[filtered_unfilled_scraping_summary_excel_df[Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[0]] == previous_date_str]
            
            # check if the records for comparision are more than 0   
            # if len(filtered_unfilled_scraping_summary_excel_df.index) > 1:
            if len(filtered_unfilled_scraping_summary_excel_df.index) > 1:
                 
                logger.info(f'summary records available for the comparision')
                # get the row index values        
                unfilled_row_index_prev_file = filtered_unfilled_scraping_summary_excel_df.index[0]
                unfilled_row_index_curr_file = filtered_unfilled_scraping_summary_excel_df.index[1]
                # unfilled_row_index0 = filtered_unfilled_scraping_summary_today_excel_df.index[0]
                # unfilled_row_index1 = filtered_unfilled_scraping_summary_today_excel_df.index[1]
            
                # unfilled_requirements_prev_file = os.path.join(Constants.PROJECT_PATH + Constants.REQUIREMENT_EXCEL_FOLDER + '\\' + filtered_unfilled_scraping_summary_excel_df.loc[unfilled_row_index_prev_file, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[2]])     #on local
                # unfilled_requirements_curr_file = os.path.join(Constants.PROJECT_PATH + Constants.REQUIREMENT_EXCEL_FOLDER + '\\' + filtered_unfilled_scraping_summary_excel_df.loc[unfilled_row_index_curr_file, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[2]])     #on local
                unfilled_requirements_prev_file = Constants.REQUIREMENT_EXCEL_FOLDER + '/' + filtered_unfilled_scraping_summary_excel_df.loc[unfilled_row_index_prev_file, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[2]]          #on docker
                unfilled_requirements_curr_file = Constants.REQUIREMENT_EXCEL_FOLDER + '/' + filtered_unfilled_scraping_summary_excel_df.loc[unfilled_row_index_curr_file, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[2]]         #on docker
                logger.info(f'Unfilled requirements files for comparios: - {filtered_unfilled_scraping_summary_excel_df.loc[unfilled_row_index_prev_file, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[2]]}, {filtered_unfilled_scraping_summary_excel_df.loc[unfilled_row_index_curr_file, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[2]]}')
        
                unfilled_requirements_prev_file_df = pd.read_excel(unfilled_requirements_prev_file, sheet_name=Constants.REQIREMENTES_EXCEL_SHEET_NAME)
                unfilled_requirements_curr_file_df = pd.read_excel(unfilled_requirements_curr_file, sheet_name=Constants.REQIREMENTES_EXCEL_SHEET_NAME)
                unfilled_requirements_curr_file_bank_req_id_list = unfilled_requirements_curr_file_df['Bank Req Num'].tolist()
                
                # # find the difference and get the closed/filled requirements
                closed_requirements_df = unfilled_requirements_prev_file_df[~unfilled_requirements_prev_file_df['Bank Req Num'].isin(unfilled_requirements_curr_file_bank_req_id_list)]
                
                previous_date = datetime.now() - timedelta(days = 1)
                previous_date_str = previous_date.strftime('%d-%b-%Y')
                current_date = datetime.now()
                current_date_str = current_date.strftime('%d-%b-%Y')
                
                logger.info(f'removing the previous and current date requirements from the cancelled requirements')
                completely_missing_requirements_df = closed_requirements_df[~closed_requirements_df['Date'].isin([previous_date_str, current_date_str])]
                
                # # check if the dataframe has rows greater than 0 then generate the cancellation excel
                # # else check the next comparision and update the summary dataframe with appropriate values
                if len(completely_missing_requirements_df.index) > 0:
                
                    cancellation_df = completely_missing_requirements_df
                    
                    logger.info(f'creating the requirements cancellation excel file')
                    
                    file_name = datetime.now().strftime(os.path.join(Constants.REQUIREMENTS_CANCELLATION_EXCEL_FILENAME))
                    # requirements_cancellation_28_days_file = os.path.join(Constants.PROJECT_PATH + Constants.REQUIREMENTS_CANCELLATION_EXCELS_FOLDER, file_name) #on local
                    requirements_cancellation_28_days_file = os.path.join(Constants.REQUIREMENTS_CANCELLATION_EXCELS_FOLDER, file_name)         #on docker
                    cancellation_df.to_excel(requirements_cancellation_28_days_file, sheet_name=Constants.CANCELLATION_EXCEL_SHEET_NAME, index=False)
                    logger.info(f'Requirement cancellation file name is: {file_name}')
                    unfilled_scraping_summary_excel_df.loc[unfilled_row_index_prev_file, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]] = 'yes'
                    unfilled_scraping_summary_excel_df.loc[unfilled_row_index_prev_file, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[4]] = file_name
                    unfilled_scraping_summary_excel_df.to_excel(Constants.UNFILLED_SCRAPING_SUMMARY_FILE_NAME, sheet_name=Constants.SCRAPING_SUMMARY_EXCEL_SHEET_NAME, index=False)
                    
                    time.sleep(1)
                else:
                    logger.info(f'No difference between the two consecutive scraped requirements.')
                    unfilled_scraping_summary_excel_df.loc[unfilled_row_index_prev_file, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]] = 'yes'
                    unfilled_scraping_summary_excel_df.loc[unfilled_row_index_prev_file, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[4]] = 'No Difference'
                    unfilled_scraping_summary_excel_df.to_excel(Constants.UNFILLED_SCRAPING_SUMMARY_FILE_NAME, sheet_name=Constants.SCRAPING_SUMMARY_EXCEL_SHEET_NAME, index=False)
                  
            else:
                logger.info(f'Summary records are not available for the comparision.')
                # print('summary records are not available for the comparision')
            
            ## If excecution date is previous date then skip file for comparion
            # if len(filtered_unfilled_scraping_summary_previous_excel_df.index) > 0:
            #     for i in range(len(filtered_unfilled_scraping_summary_previous_excel_df.index)):
            #         files_not_for_comparison = filtered_unfilled_scraping_summary_previous_excel_df.index[i]
            #         print('files_not_for_comparison= ',files_not_for_comparison,filtered_unfilled_scraping_summary_previous_excel_df.loc[files_not_for_comparison, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[2]])
            #         unfilled_scraping_summary_excel_df.loc[files_not_for_comparison, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]] = 'yes'
            #         unfilled_scraping_summary_excel_df.loc[files_not_for_comparison, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[4]] = 'Compared'
            #         unfilled_scraping_summary_excel_df.to_excel(Constants.UNFILLED_SCRAPING_SUMMARY_FILE_NAME, sheet_name=Constants.SCRAPING_SUMMARY_EXCEL_SHEET_NAME, index=False)
            
            end_time = time.time()
            total_time = end_time - start_time
      
            logger.info(f'Time required for the cancelled requirement comparison is: {total_time}')    
            logger.info(f'East Kent Hospital Requirements Comparison Completed.')
            remove_file_handler_logger()
            
        except Exception:
            
            exception_type, exception_value, exception_traceback = sys.exc_info()
            traceback_string = traceback.format_exception(exception_type,
                            exception_value, exception_traceback)
            err_msg = json.dumps({
                "errorType": exception_type.__name__,
                "errorMessage": str(exception_value),
                "stackTrace": traceback_string
            })
            logger.error(f'Error Occured While Comparing 28 Days Requirements: {err_msg}')
            
            end_time = time.time()
            total_time = end_time - start_time
            logger.info(f'Time required for the cancelled requirement comparison is: {total_time}')    
            remove_file_handler_logger()

        return
        
              
# if __name__ == '__main__':
#     start_time = time.time()
    
#     RequirementScraping.scraping_requirements()  
##     RequirementCancellation.cancelled_requirements()
    
#     end_time = time.time()
#     total_time = end_time - start_time
#     logging.info(f'Total time required for the execution is {total_time}')
            
            