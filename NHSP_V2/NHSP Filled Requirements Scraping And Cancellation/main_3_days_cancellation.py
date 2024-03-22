from selenium import webdriver
from selenium.webdriver.common.by import By

# for firefox browser
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

import pandas as pd

import time
import os
import shutil
import glob
from datetime import datetime, timedelta
import json
import sys
import traceback

from common_3_days_cancellation import Constants

import logging
logging.basicConfig(level=logging.INFO, 
                    filename=datetime.now().strftime(os.path.join(Constants.PROJECT_PATH + Constants.EXECUTION_LOGS_FOLDER, Constants.EXECUTION_LOGS_FILENAME)), 
                    filemode='w', format='%(asctime)s - [%(threadName)s] [%(levelname)s] - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

class NHSPPortalScraping():
    def scraping():
        try:
            start_time = time.time()
            logging.info(f'NHSP Portal Scraping Started')

            # for firefox browser
            options = FirefoxOptions()
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.dir", Constants.EXPORT_EXCEL_DOWNLOAD_PATH)
            options.add_argument('-headless')
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            # driver = webdriver.Firefox()

            # minimize the window size to view the requirements in the cards format
            window_size = driver.get_window_size()
            window_width = window_size['width'] - ((window_size['width']/100) * 20)
            window_height = window_size['height'] - ((window_size['height']/100) * 7)
            driver.set_window_size(window_width, window_height)
            
            driver.get(Constants.PORTAL_LINK)
            logging.info(f'login page opened')
            
            username = driver.find_element(By.ID, Constants.USERNAME_FIELD_ID)
            username.clear()
            username.send_keys(Constants.PORTAL_CREDENTIALS['username'])

            password = driver.find_element(By.ID, Constants.PASSWORD_FIElD_ID)
            password.clear()
            password.send_keys(Constants.PORTAL_CREDENTIALS['password'])

            login = driver.find_element(By.ID, Constants.LOGIN_BUTTON_ID)
            login.click()

            logging.info(f'clicked Login')
            time.sleep(30)
            
            # click on the next 3 days tab
            logging.info(f'checking for the navigation panel')
            navbar = driver.find_element(By.ID, Constants.NAVIGATION_PANEL_DIV_ID)
            logging.info(f'navigation panel found and checking for the next 3 days tab')
            next_3_days_tab = navbar.find_element(By.LINK_TEXT, Constants.NEXT_3_DAYS_TAB_NAME)
            next_3_days_tab.click()
            logging.info(f'clicked on the next 3 days tab')
            time.sleep(5)
            
            # open the filtering option
            logging.info(f'opening the filter option panel')
            filter_menu_element = driver.find_element(By.XPATH, Constants.FILTER_MENU_XPATH)
            filter_menu_element.click()
            time.sleep(5)

            # select the filtering option - status (all)
            logging.info(f'selecting the filtering option - status (all)')
            filter_status_all_option_element = driver.find_element(By.XPATH, Constants.FILTER_STATUS_ALL_OPTION_XPATH)
            filter_status_all_option_element.click()
            time.sleep(10)

            # select the filtering option - authorisation (all)
            logging.info(f'selecting the filtering option - authorisation (all)')
            filter_authorisation_all_option_element = driver.find_element(By.XPATH, Constants.FILTER_AUTHORISATION_ALL_OPTION_XPATH)
            filter_authorisation_all_option_element.click()
            time.sleep(10)

            # TAKE SCREENSHOT OF SELECTED FILTERING OPTIONS
            driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.PROJECT_PATH + Constants.EXECUTION_SCREENSHOTS_FOLDER, '3_days_01_filter_selections_%d_%m_%Y_%H_%M_%S.png')))

            # close the filtering option
            logging.info(f'closing the filter option panel')
            filter_menu_element = driver.find_element(By.XPATH, Constants.FILTER_MENU_XPATH)
            filter_menu_element.click()
            time.sleep(5)

            # get the list of .xlsx files from the download folder before exporting the excel
            logging.info(f'getting the list of .xlsx files from downloads before exporting excel')
            list_of_files_before_download = glob.glob(Constants.EXPORT_EXCEL_DOWNLOAD_PATH + '*.xlsx')

            # export the excel
            logging.info(f'clicking on the export option')
            export_element = driver.find_element(By.XPATH, Constants.EXPORT_BUTTON_XPATH)
            export_element.click()
            time.sleep(3)
            
            excel_element = driver.find_element(By.XPATH, Constants.EXPORT_EXCEL_OPTION_XPATH)
            excel_element.click()
            time.sleep(10)
            
            # get new exported file name and move it
            logging.info(f'getting the list of the .xlsx files list from the downloads after exporting the excel')
            list_of_files_after_download = glob.glob(Constants.EXPORT_EXCEL_DOWNLOAD_PATH + '*.xlsx')
            exported_excel_file = list(set(list_of_files_after_download).difference(list_of_files_before_download))
            
            logging.info(f'copying the exported excel file from downloads to exported_excel folder')
            if len(exported_excel_file) > 0:
                src_file = exported_excel_file[0]
                
                file_name = datetime.now().strftime(os.path.join(Constants.EXPORTED_EXCEL_FILENAME))
                moved_exported_file = os.path.join(Constants.PROJECT_PATH + Constants.EXPORTED_EXCELS_FOLDER, file_name)
                dst_file = moved_exported_file

                shutil.copy(src_file, dst_file)
            
            # open the exported excel file
            logging.info(f'opening the exported excel file in the pandas dataframe')
            exported_excel_df = pd.read_excel(exported_excel_file[0], sheet_name=Constants.REQIREMENTES_EXCEL_SHEET_NAME)
            
            filtered_df = exported_excel_df[:-2]
            # filtered_df = filtered_df[filtered_df[Constants.EXCEL_COLUMN_HEADERS_LIST[7]] != 'Unfilled']
            filtered_df = filtered_df[Constants.EXCEL_COLUMN_HEADERS_LIST]
            filtered_df = filtered_df.fillna('')
            df = pd.DataFrame(columns=Constants.EXCEL_COLUMN_HEADERS_LIST)
            logging.info(f'looping on the exported file dataframe')
            for index in range(len(filtered_df.index)):                
                # adding all required detailes from exported excel datframe to newly generated dataframe
                new_row = {}
                for column in Constants.EXCEL_COLUMN_HEADERS_LIST:
                    # new_row[column] = str(exported_excel_df.loc[index, column]).strip()
                    new_row[column] = str(filtered_df.loc[index, column]).strip()
                                           
                df = df.append(new_row, ignore_index=True)
                print('df= ',df)
            logging.info(f'creating the filled shift requirements excel files')
            file_name = datetime.now().strftime(os.path.join(Constants.SHIFT_REQUIREMENTS_EXCEL_FILENAME))
            filled_requirements_file = os.path.join(Constants.PROJECT_PATH + Constants.FILLED_REQUIREMENTS_EXCELS_FOLDER, file_name)
            # filtered_df.to_excel(filled_requirements_file, sheet_name=Constants.REQIREMENTES_EXCEL_SHEET_NAME, index=False)
            df.to_excel(filled_requirements_file, sheet_name=Constants.REQIREMENTES_EXCEL_SHEET_NAME, index=False)
 
            logging.info(f'adding record in the execution summary file')
            filled_requirements_summary_df = pd.read_excel(Constants.FILLED_SCRAPING_SUMMARY_FILE_NAME, sheet_name=Constants.SCRAPING_SUMMARY_EXCEL_SHEET_NAME)
            new_summary_row = {Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[0]: datetime.now().strftime('%d/%m/%Y'), 
                               Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[1]: datetime.now().strftime('%H:%M:%S'), 
                               Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[2]: file_name, 
                               Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]: 'no', 
                               Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[4]: ''
                               }
            filled_requirements_summary_df = filled_requirements_summary_df.append(new_summary_row, ignore_index=True)
            filled_requirements_summary_df.to_excel(Constants.FILLED_SCRAPING_SUMMARY_FILE_NAME, sheet_name=Constants.SCRAPING_SUMMARY_EXCEL_SHEET_NAME, index=False)

            # logout the portal
            logging.info(f'checking and clicking on the logout navigation menu panel')
            navigation_menu_dropdown_element = driver.find_element(By.ID, Constants.LOGOUT_NAVIGATION_DROPDOWN_MENU_ID)
            navigation_menu_dropdown_element.click()
            time.sleep(1)
            
            logging.info(f'clicking on the logout menu button')
            navigation_menu_element = driver.find_element(By.ID, Constants.LOGOUT_NAVIGATION_MENU_ID)
            logout_element = navigation_menu_element.find_element(By.LINK_TEXT, Constants.LOGOUT_OPTION_NAME)
            logout_element.click()
            time.sleep(5)
            
            logging.info(f'logout completed')

            driver.close()
            driver.quit()
            logging.info(f'closed the browser window')

            end_time = time.time()
            total_time = end_time - start_time
            logging.info(f'Time required for the execution is {total_time}')

            logging.info(f'NHSP Portal Scraping Completed')
        except Exception:
            # TAKE SCREENSHOT AFTER ERROR
            driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.PROJECT_PATH + Constants.EXECUTION_SCREENSHOTS_FOLDER, '3_days_after_error_occured_%d_%m_%Y_%H_%M_%S.png')))

            exception_type, exception_value, exception_traceback = sys.exc_info()
            traceback_string = traceback.format_exception(exception_type,
                            exception_value, exception_traceback)
            err_msg = json.dumps({
                "errorType": exception_type.__name__,
                "errorMessage": str(exception_value),
                "stackTrace": traceback_string
            })
            logging.error(f'Error Occured: {err_msg}')
        return

class NHSPRequirementsCompare():
    def comparing():
        try:
            start_time = time.time()
            logging.info(f'NHSP Requirements Compare Started')

            # get the unfilled requirements scraping summary excel and
            # filter the not compared records from the summary dataframe
            unfilled_scraping_summary_excel_df = pd.read_excel(Constants.UNFILLED_SCRAPING_SUMMARY_FILE_NAME, sheet_name=Constants.SCRAPING_SUMMARY_EXCEL_SHEET_NAME)
            filtered_unfilled_scraping_summary_excel_df = unfilled_scraping_summary_excel_df[unfilled_scraping_summary_excel_df[Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]] == 'no']
            
            # check if the records for comparision are more than 0
            if len(filtered_unfilled_scraping_summary_excel_df.index) > 0:
                logging.info(f'summary records available for the comparision')

                # scrape the current filled/unfilled/all requirements from the portal
                # and retry once if any exception occurres in the scraping
                try:
                    NHSPPortalScraping.scraping()
                except Exception:
                    exception_type, exception_value, exception_traceback = sys.exc_info()
                    traceback_string = traceback.format_exception(exception_type,
                                    exception_value, exception_traceback)
                    err_msg = json.dumps({
                        "errorType": exception_type.__name__,
                        "errorMessage": str(exception_value),
                        "stackTrace": traceback_string
                    })
                    logging.error(f'Error Occured While Comparing 3 Days Requirements: {err_msg}')
                    logging.info(f'Retrying with the scraping the all requirements from portal')
                    NHSPPortalScraping.scraping()
                
                unfilled_scraping_summary_excel_df = pd.read_excel(Constants.UNFILLED_SCRAPING_SUMMARY_FILE_NAME, sheet_name=Constants.SCRAPING_SUMMARY_EXCEL_SHEET_NAME)
                filtered_unfilled_scraping_summary_excel_df = unfilled_scraping_summary_excel_df[unfilled_scraping_summary_excel_df[Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]] == 'no']

                filled_scraping_summary_excel_df = pd.read_excel(Constants.FILLED_SCRAPING_SUMMARY_FILE_NAME, sheet_name=Constants.SCRAPING_SUMMARY_EXCEL_SHEET_NAME)
                filtered_filled_scraping_summary_excel_df = filled_scraping_summary_excel_df[filled_scraping_summary_excel_df[Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]] == 'no']
                if len(filtered_filled_scraping_summary_excel_df.index) == 1:
                    filled_excel_row_index = filtered_filled_scraping_summary_excel_df.index[0]
                    filled_requirements_file_path = Constants.FILLED_REQUIREMENTS_EXCELS_FOLDER + '\\' + filtered_filled_scraping_summary_excel_df.loc[filled_excel_row_index, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[2]]
                    logging.info(f'filled_requirements_file_path - {filled_requirements_file_path}')
                    # filled_execution_date = filtered_filled_scraping_summary_excel_df.loc[filled_excel_row_index, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[0]]
                    # logging.info(f'filled_execution_date - {filled_execution_date}')
                    
                    filled_requirements_excel_df = pd.read_excel(filled_requirements_file_path, sheet_name=Constants.REQIREMENTES_EXCEL_SHEET_NAME)
                    all_requirements_booking_reference_number_list = filled_requirements_excel_df['Booking Reference Number'].tolist()
                    filled_by_bank_requirements_excel_df = filled_requirements_excel_df[filled_requirements_excel_df[Constants.EXCEL_COLUMN_HEADERS_LIST[7]] == 'Filled by Bank']
                    filled_by_bank_requirements_booking_reference_number_list = filled_by_bank_requirements_excel_df['Booking Reference Number'].tolist()
                    
                    # iterate the loop untill all comparision completed
                    for count in range (len(filtered_unfilled_scraping_summary_excel_df.index)):
                        # get the row index values
                        unfilled_row_index = filtered_unfilled_scraping_summary_excel_df.index[count]

                        # # # get the execution dates for previous and current executions and check if both are same
                        # unfilled_execution_date = filtered_unfilled_scraping_summary_excel_df.loc[unfilled_row_index, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[0]]
                        # if unfilled_execution_date == filled_execution_date:
                        #     # compare the scraped requirements only if the execution date is same
                        
                        unfilled_requirements_file_path = Constants.UNFILLED_REQUIREMENTS_EXCELS_FOLDER + '\\' + filtered_unfilled_scraping_summary_excel_df.loc[unfilled_row_index, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[2]]
                        logging.info(f'unfilled_requirements_file_path - {unfilled_requirements_file_path}')
                        unfilled_requirements_excel_df = pd.read_excel(unfilled_requirements_file_path, sheet_name=Constants.REQIREMENTES_EXCEL_SHEET_NAME)
                        
                        # # find the difference and get the requirements which are now filled by bank
                        requirements_filled_by_bank_df = unfilled_requirements_excel_df[unfilled_requirements_excel_df['Booking Reference Number'].isin(filled_by_bank_requirements_booking_reference_number_list)]
                        requirements_filled_by_bank_df.loc[:, 'Status'] = 'Filled by Bank'

                        # current_date = datetime.now()
                        # current_date_str = current_date.strftime('%d/%m/%Y')
                        # logging.info(f'removing the current date requirements from the cancelled requirements')
                        # requirements_filled_by_bank_df = requirements_filled_by_bank_df[~requirements_filled_by_bank_df['Shift Date'].isin([current_date_str])]
                        # requirements_filled_by_bank_df.loc[:, 'Status'] = 'Filled by Bank'
                        
                        # # find the difference and get the requirements which are completely missing
                        completely_missing_requirements_df = unfilled_requirements_excel_df[~unfilled_requirements_excel_df['Booking Reference Number'].isin(all_requirements_booking_reference_number_list)]

                        previous_date = datetime.now() - timedelta(days = 1)
                        previous_date_str = previous_date.strftime('%d/%m/%Y')
                        current_date = datetime.now()
                        current_date_str = current_date.strftime('%d/%m/%Y')
                        logging.info(f'removing the previous and current date requirements from the cancelled requirements')
                        completely_missing_requirements_df = completely_missing_requirements_df[~completely_missing_requirements_df['Shift Date'].isin([previous_date_str, current_date_str])]
                        
                        # check if the dataframe has rows greater than 0 then generate the cancellation excel
                        # else check the next comparision and update the summary dataframe with appropriate values
                        if len(requirements_filled_by_bank_df.index) > 0 or len(completely_missing_requirements_df.index) > 0:
                            dfs = [requirements_filled_by_bank_df, completely_missing_requirements_df]
                            cancellation_df = pd.concat(dfs, ignore_index=True)
                            # cancellation_df = requirements_filled_by_bank_df
                            
                            logging.info(f'creating the requirements cancellation excel file')
                            file_name = datetime.now().strftime(os.path.join(Constants.REQUIREMENTS_CANCELLATION_EXCEL_FILENAME))
                            requirements_cancellation_3_days_file = os.path.join(Constants.PROJECT_PATH + Constants.REQUIREMENTS_CANCELLATION_EXCELS_FOLDER, file_name)
                            cancellation_df.to_excel(requirements_cancellation_3_days_file, sheet_name=Constants.CANCELLATION_EXCEL_SHEET_NAME, index=False)
                            
                            unfilled_scraping_summary_excel_df.loc[unfilled_row_index, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]] = 'yes'
                            unfilled_scraping_summary_excel_df.loc[unfilled_row_index, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[4]] = file_name
                            time.sleep(1)
                        else:
                            logging.info(f'no difference between the unfilled and filled scraped requirements')
                            unfilled_scraping_summary_excel_df.loc[unfilled_row_index, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]] = 'yes'
                            unfilled_scraping_summary_excel_df.loc[unfilled_row_index, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[4]] = 'No Difference'
                        # else:
                        #     # do not compare the scraped requirements if the execution date is changed
                        #     logging.info(f'execution dates are not same for the unfilled and filled scraping')
                        #     unfilled_scraping_summary_excel_df.loc[unfilled_row_index, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]] = 'yes'
                        #     unfilled_scraping_summary_excel_df.loc[unfilled_row_index, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[4]] = 'Execution Date Changed'

                    # update the excel file using the updated dataframe
                    unfilled_scraping_summary_excel_df.to_excel(Constants.UNFILLED_SCRAPING_SUMMARY_FILE_NAME, sheet_name=Constants.SCRAPING_SUMMARY_EXCEL_SHEET_NAME, index=False)

                    # update the filled excel file using the updated dataframe
                    filled_scraping_summary_excel_df.loc[filled_excel_row_index, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]] = 'yes'
                    filled_scraping_summary_excel_df.loc[filled_excel_row_index, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[4]] = 'Compared'
                    filled_scraping_summary_excel_df.to_excel(Constants.FILLED_SCRAPING_SUMMARY_FILE_NAME, sheet_name=Constants.SCRAPING_SUMMARY_EXCEL_SHEET_NAME, index=False)

                else:
                    logging.info(f'filled/all requirements scraping is not completed / failed')
                    logging.info(f'breaking the comparison execution and cancellation functionality')
            else:
                logging.info(f'summary records are not available for the comparision')
            
            end_time = time.time()
            total_time = end_time - start_time
            logging.info(f'Total time required for the entire execution is {total_time}')

            logging.info(f'NHSP Requirements Compare Completed')
        except Exception:
            end_time = time.time()
            total_time = end_time - start_time
            logging.info(f'Time required for the execution is {total_time}')

            exception_type, exception_value, exception_traceback = sys.exc_info()
            traceback_string = traceback.format_exception(exception_type,
                            exception_value, exception_traceback)
            err_msg = json.dumps({
                "errorType": exception_type.__name__,
                "errorMessage": str(exception_value),
                "stackTrace": traceback_string
            })
            logging.error(f'Error Occured While Comparing 3 Days Requirements: {err_msg}')
        return

if __name__ == '__main__':
    NHSPRequirementsCompare.comparing()
