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
from datetime import datetime
import json
import sys
import traceback

from common_3_days_scraping import Constants, Tasks

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

            # select the filtering option - status (unfilled)
            logging.info(f'selecting the filtering option - status (unfilled)')
            filter_status_unfilled_option_element = driver.find_element(By.XPATH, Constants.FILTER_STATUS_UNFILLED_OPTION_XPATH)
            filter_status_unfilled_option_element.click()
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
            
            # scroll the page to the end of the list (infinite scroll)
            logging.info(f'scrolling the page down (infinite scrolling)')
            Tasks.infinite_scroll(driver)
            logging.info(f'completed scrolling the page down (infinite scrolling)')

            # TAKE SCREENSHOT AFTER THE INFINITE SCROLLING
            driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.PROJECT_PATH + Constants.EXECUTION_SCREENSHOTS_FOLDER, '3_days_02_infinite_scrolling_%d_%m_%Y_%H_%M_%S.png')))
            
            # get all cards elements after scrolling
            logging.info(f'getting the all cards details div from the page')
            content = driver.page_source
            soup = BeautifulSoup(content, features="html.parser")
            div_element = soup.find('div', attrs={'id':Constants.SHIFT_REQUIREMENTS_DIV_ID})

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
            print('exported_excel_file[0]= ',exported_excel_file[0])
            exported_excel_df = pd.read_excel(exported_excel_file[0], sheet_name=Constants.EXCEL_SHEET_NAME)
            filtered_df = exported_excel_df[:-2]
            filtered_df = filtered_df[Constants.EXCEL_COLUMN_HEADERS_LIST]
            filtered_df = filtered_df.fillna('')
            # parse all elements one by one from exported excel and from web page
            # also, create the dataframe to generate the shift requirements excel
            logging.info(f'generating the new empty dataframe to store the shift requirements details')
            df = pd.DataFrame(columns=Constants.EXCEL_COLUMN_HEADERS_LIST)
            logging.info(f'looping on the exported file dataframe')
            for index in range(len(filtered_df.index)):                
                # check if the row is blank or invalid and skip those rows from excel
                booking_reference_number = str(filtered_df.loc[index, Constants.EXCEL_COLUMN_HEADERS_LIST[0]]).strip()
                if booking_reference_number in ['', 'nan'] or 'Date Created' in booking_reference_number:
                    logging.info(f'found the invalid record from the excel dataframe')
                    continue
                # adding all required detailes from exported excel datframe to newly generated dataframe
                new_row = {}
                for column in Constants.EXCEL_COLUMN_HEADERS_LIST:
                    new_row[column] = str(filtered_df.loc[index, column]).strip()
                     
                    # value = str(exported_excel_df.loc[index, column]).strip()
                    # # Check if the column is 'Notes' and the value is 'nan'
                    # if column == Constants.EXCEL_COLUMN_HEADERS_LIST[8]  and value in ['', 'nan']:
                    #     new_row[column] = ''
                    # # Check if the column is 'Gender' and the value is 'nan'
                    # elif column == Constants.EXCEL_COLUMN_HEADERS_LIST[9]  and value in ['', 'nan']:
                    #     new_row[column] = 'NA'
                    # else:
                    #     new_row[column] = value
                
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
                    logging.info(f'In Exception, card element not found. booking_reference_number = {booking_reference_number}')
                
                # insert the new row in the dataframe of shift requirements excel
                df = df.append(new_row, ignore_index=True)
            
            logging.info(f'creating the shift requirements excel files')
            file_name = datetime.now().strftime(os.path.join(Constants.SHIFT_REQUIREMENTS_EXCEL_FILENAME))
            shift_requirements_file = os.path.join(Constants.PROJECT_PATH + Constants.SHIFT_REQUIREMENTS_EXCELS_FOLDER, file_name)
            df.to_excel(shift_requirements_file, sheet_name=Constants.EXCEL_SHEET_NAME, index=False)

            logging.info(f'creating the requirements excel file to check the cancellation')
            requirements_file_name = datetime.now().strftime(os.path.join(Constants.SHIFT_REQUIREMENTS_EXCEL_FILENAME))
            requirements_file = os.path.join(Constants.REQUIREMENTS_FOR_COMPARE_EXCEL_PATH, requirements_file_name)
            df.to_excel(requirements_file, sheet_name=Constants.EXCEL_SHEET_NAME, index=False)

            logging.info(f'adding record in the execution summary file')
            requirements_summary_df = pd.read_excel(Constants.REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_FILE_PATH, sheet_name=Constants.REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_EXCEL_SHEET_NAME)
            new_summary_row = {Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[0]: datetime.now().strftime('%d/%m/%Y'), 
                               Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[1]: datetime.now().strftime('%H:%M:%S'), 
                               Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[2]: requirements_file_name, 
                               Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]: 'no', 
                               Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[4]: ''
                               }
            requirements_summary_df = requirements_summary_df.append(new_summary_row, ignore_index=True)
            requirements_summary_df.to_excel(Constants.REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_FILE_PATH, sheet_name=Constants.REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_EXCEL_SHEET_NAME, index=False)

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

if __name__ == '__main__':
    NHSPPortalScraping.scraping()
