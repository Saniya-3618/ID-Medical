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
import math
import urllib
import requests, zipfile
from io import BytesIO

from common_28_days_scraping import Constants, Tasks

import logging
from pytz import timezone


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
        self.name = "worker__28_days_scraping"
        self.log_file = datetime.now(timezone('Asia/Kolkata')).strftime(os.path.join(Constants.EXECUTION_LOGS_FOLDER, Constants.EXECUTION_LOGS_FILENAME))
        configure_logger(self.name, self.log_file)
        
    def scraping_requirements():
        try:
            # logging.Formatter.converter = lambda *args: datetime.now(timezone('Asia/Kolkata')).timetuple()
            # logging.basicConfig(level=logging.INFO, 
            #         filename=datetime.now(timezone('Asia/Kolkata')).strftime(os.path.join( Constants.EXECUTION_LOGS_FOLDER, Constants.EXECUTION_LOGS_FILENAME)), 
            #         filemode='w', format='%(asctime)s - [%(threadName)s] [%(levelname)s] - %(message)s',
            #         datefmt='%d-%b-%y %H:%M:%S') #for docker
            
            start_time = time.time()
            logger.info(f'NHSP Portal Scraping Started')
            
            is_parsing_completed = False
            location_index = 0

            # create a blank file to save the collective requirements to compare for the cancellations
            blank_df = pd.DataFrame(columns=Constants.EXCEL_COLUMN_HEADERS_LIST + [Constants.EXCEL_EXTRA_COLUMN_HEADER])
            blank_file_name = datetime.now().strftime(os.path.join(Constants.SHIFT_REQUIREMENTS_EXCEL_FILENAME))
            collective_shift_requirements_file = os.path.join(Constants.REQUIREMENTS_FOR_COMPARE_EXCEL_PATH, blank_file_name)
            blank_df.to_excel(collective_shift_requirements_file, sheet_name=Constants.EXCEL_SHEET_NAME, index=False)

            driver_path = NHSPPortalScraping.download_chrome_driver()
            
            # iterate the loop until the parsing and scraping get completed
            while not is_parsing_completed:
                # get the parsing status and the next location index for the parsing, and update the loop variables
                is_all_locations_parsed, next_location_index = NHSPPortalScraping.scraping_requirements_for_location(location_index, collective_shift_requirements_file, driver_path)     #on local
                # is_all_locations_parsed, next_location_index = NHSPPortalScraping.scraping_requirements_for_location(location_index, collective_shift_requirements_file)  #on docker 
                
                if not is_all_locations_parsed:
                    is_parsing_completed = False
                    location_index = next_location_index
                else:
                    is_parsing_completed = True
            
            # add record in the execution summary file
            requirements_summary_df = pd.read_excel(Constants.REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_FILE_PATH, sheet_name=Constants.REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_EXCEL_SHEET_NAME)
            new_summary_row = {Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[0]: datetime.now().strftime('%d/%m/%Y'), 
                               Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[1]: datetime.now().strftime('%H:%M:%S'), 
                               Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[2]: blank_file_name, 
                               Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]: 'no', 
                               Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[4]: ''}
            requirements_summary_df = requirements_summary_df.append(new_summary_row, ignore_index=True)
            requirements_summary_df.to_excel(Constants.REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_FILE_PATH, sheet_name=Constants.REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_EXCEL_SHEET_NAME, index=False)

            end_time = time.time()
            total_time = end_time - start_time
            logger.info(f'Total time required for the execution is {total_time}')

            logger.info(f'NHSP Portal Scraping Completed')
            remove_file_handler_logger()
        except Exception:
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
        return

    def scraping_requirements_for_location(location_index, collective_shift_requirements_file, driver_path): #on local
    # def scraping_requirements_for_location(location_index, collective_shift_requirements_file): #on docker
    
        try:
            location_scraping_start_time = time.time()

            # initiate the loop variables
            is_wards_parsing_limit_reached = False
            is_all_locations_parsed = False
            total_parsed_wards = 0
            total_parsed_locations = 0
            location_name_list = []
            break_flag = False
            
            logger.info(f'Scraping requirements for the location index - {location_index}')
            # print('before driver')
            # options = ChromeOptions()
            # prefs = {'download.default_directory': Constants.EXPORT_EXCEL_DOWNLOAD_PATH}
            # options.add_experimental_option('prefs', prefs)
            # options.add_argument('--no-sandbox')
            # options.add_argument('--disable-dev-shm-usage')
            # options.add_argument('--disable-gpu')
            # options.add_argument('--headless=new')
            # driver = webdriver.Chrome(service=ChromeService(executable_path=driver_path), options=options)
            # # driver = webdriver.Chrome(options=options)
            # # driver = webdriver.Remote('http://127.0.0.1:4441/wd/hub' , options=options) 
            # # driver = webdriver.Chrome(service=ChromeService(executable_path='/usr/local/bin/chromedriver'), options=options)
            # # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            # print('after driver')
            
            options = FirefoxOptions()
            
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.dir", Constants.EXPORT_EXCEL_DOWNLOAD_PATH)
            options.set_preference("browser.download.manager.showWhenStarting", False)
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
            options.add_argument('-headless')
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            
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
            time.sleep(20)
            
            # click on the 28 days tab
            logger.info(f'checking for the navigation panel')
            navbar = driver.find_element(By.ID, Constants.NAVIGATION_PANEL_DIV_ID)
            logger.info(f'navigation panel found and checking for the 28 days tab')
            next_28_days_tab = navbar.find_element(By.LINK_TEXT, Constants.NEXT_28_DAYS_TAB_NAME)
            next_28_days_tab.click()
            logger.info(f'clicked on the 28 days tab')
            time.sleep(10)
            
            # open the filtering option
            logger.info(f'opening the filter option panel')
            filter_menu_element = driver.find_element(By.XPATH, Constants.FILTER_MENU_XPATH)
            filter_menu_element.click()
            time.sleep(5)

            # select the filtering option - status (unfilled)
            logger.info(f'selecting the filtering option - status (unfilled)')
            filter_status_unfilled_option_element = driver.find_element(By.XPATH, Constants.FILTER_STATUS_UNFILLED_OPTION_XPATH)
            filter_status_unfilled_option_element.click()
            time.sleep(5)
            
            # select the filtering option - authorisation (all)
            logger.info(f'selecting the filtering option - authorisation (all)')
            filter_authorisation_all_option_element = driver.find_element(By.XPATH, Constants.FILTER_AUTHORISATION_ALL_OPTION_XPATH)
            filter_authorisation_all_option_element.click()
            time.sleep(5)
            
            # TAKE SCREENSHOT OF SELECTED FILTERING OPTIONS
            # driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.PROJECT_PATH + Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_01_filter_selctions_%d_%m_%Y_%H_%M_%S.png')))
            driver.get_screenshot_as_file(datetime.now().strftime(os.path.join( Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_01_filter_selctions_%d_%m_%Y_%H_%M_%S.png')))

            # close the filtering option
            logger.info(f'closing the filter option panel')
            filter_menu_element = driver.find_element(By.XPATH, Constants.FILTER_MENU_XPATH)
            filter_menu_element.click()
            time.sleep(3)
            
            # get the location options data
            location_menu_element = driver.find_element(By.XPATH, Constants.LOCATION_DROPDOWN_XPATH)
            location_menu_options_elements = location_menu_element.find_elements(By.TAG_NAME, 'option')
            location_menu_options_elements = location_menu_options_elements[1:]
            logger.info(f'location_menu_options_elements - {len(location_menu_options_elements)}')

            # iterate the loop until either wards parsing limit exceeds or all locations are parsed
            while not (is_wards_parsing_limit_reached or is_all_locations_parsed):
                # get location element from list and click it
                location = location_menu_options_elements[location_index]
                location_name = location.text
                logger.info(f'location - {location_name}')
                location.click()
                time.sleep(1)

                # uncheck all wards selection
                ward_menu_option_element = driver.find_element(By.XPATH, Constants.WARD_DROPDOWN_XPATH)
                ward_menu_option_ul_element = ward_menu_option_element.find_element(By.TAG_NAME, 'ul')
                ward_menu_option_a_element = ward_menu_option_ul_element.find_elements(By.TAG_NAME, 'a')
                
                uncheck_all_wards_element = ward_menu_option_a_element[1]
                
                ward_menu_option_a_element = ward_menu_option_a_element[:-1]
                ward_menu_option_a_element = ward_menu_option_a_element[2:]
                total_wards = len(ward_menu_option_a_element)

                logger.info(f'total parsed locations - {total_parsed_locations}')
                logger.info(f'total parsed wards - {total_parsed_wards}')
                logger.info(f'total next wards for parsing - {total_wards}')
                
                # check if the wards limit exceeded or not
                if total_parsed_locations == 0:
                    # logging.info(f'continue the scraping process even if total wards greater than the wards limit')
                    pass
                else:
                    # logging.info(f'scraping is already started for this login')
                    if total_parsed_wards >= Constants.TOTAL_WARDS_FOR_SCRAPING_IN_ONE_LOGIN:
                        # logging.info(f'break scraping and return and start with new login')
                        is_wards_parsing_limit_reached = True
                        continue # or break
                    elif total_parsed_wards < Constants.TOTAL_WARDS_FOR_SCRAPING_IN_ONE_LOGIN:
                        if total_parsed_wards + total_wards <= Constants.TOTAL_WARDS_FOR_SCRAPING_IN_ONE_LOGIN:
                            # logging.info(f'wards limit not exceeded, continue the scraping process')
                            pass
                        else:
                            # logging.info(f'wards limit exceeded, return and start with new login')
                            is_wards_parsing_limit_reached = True
                            continue # or break
                
                ward_menu_option_element.click()
                time.sleep(1)
                uncheck_all_wards_element.click()
                ward_menu_option_element.click()
                
                # select the date range option
                date_range_menu_element = driver.find_element(By.XPATH, Constants.DATE_RANGE_DROPDOWN_XPATH)
                date_range_menu_element.click()
                date_filter_options_element = driver.find_element(By.CLASS_NAME, Constants.DATE_RANGE_DROPDOWN_OPTIONS_CLASS_NAME)
                date_range_options_ul_element = date_filter_options_element.find_element(By.TAG_NAME, 'ul')
                for date_range_option in Constants.DATE_RANGE_OPTIONS:
                    try:
                        date_range_option_element = date_range_options_ul_element.find_element(By.XPATH, f'//*[text() = "{date_range_option}"]')
                        logger.info(f'Selected the date range option is - {date_range_option_element.text}')
                        date_range_option_element.click()
                        break
                    except:
                        pass
                
                total_iterations_for_parsing = math.ceil(total_wards/Constants.TOTAL_WARDS_FOR_PARSING)
                logger.info(f'Total iterations require for the parsing are - {total_iterations_for_parsing}')

                # iterate on the wards options and scrape the requirements
                # for iteration_count in range(total_iterations_for_parsing):
                is_all_wards_parsed = False
                iteration_count = 0
                while not is_all_wards_parsed:
                    try:
                        # open the ward dropdown
                        ward_menu_option_element = driver.find_element(By.XPATH, Constants.WARD_DROPDOWN_XPATH)
                        ward_menu_option_element.click()
                        time.sleep(1)
                        
                        ward_options_ul_element = ward_menu_option_element.find_element(By.TAG_NAME, 'ul')
                        ward_options_li_elements = ward_options_ul_element.find_elements(By.CLASS_NAME, Constants.WARD_DROPDOWN_OPTIONS_CLASS_NAME)
                        
                        # uncheck the selected wards
                        uncheck_all_wards_element.click()
                        time.sleep(1)

                        # calculate the start and end index for the wards parsing
                        start_ward_index = iteration_count * Constants.TOTAL_WARDS_FOR_PARSING
                        end_ward_index = (iteration_count * Constants.TOTAL_WARDS_FOR_PARSING) + Constants.TOTAL_WARDS_FOR_PARSING
                        wards_group_for_parsing = ward_options_li_elements[start_ward_index:end_ward_index]
                        
                        # select the wards
                        wards_name_list = []
                        for ward in wards_group_for_parsing:
                            ward_text = ward.get_attribute('textContent')
                            ward_text = ward_text.strip()
                            wards_name_list.append(ward_text)
                            logger.info(f'{iteration_count} - {ward_text}')
                            ward.click()

                        # close the wards dropdown
                        ward_menu_option_element.click()
                        time.sleep(1)

                        # click on the search button
                        search_element = driver.find_element(By.XPATH, Constants.SEARCH_BUTTON_XPATH)
                        search_element.click()

                        # wait until requirements get loaded
                        try:
                            WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, Constants.DATA_LOADER_XPATH)))
                        except:
                            logger.info(f'timeout error occured, waiting for somemore time')
                            WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, Constants.DATA_LOADER_XPATH)))

                        # check if requirements are available or not
                        requirements_available = False
                        try:
                            requirements_table_element = driver.find_element(By.ID, Constants.SHIFT_REQUIREMENTS_DIV_ID)
                            #search_notice_element = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div[4]/div/div/div/div[2]/div/div[2]/table/tbody/tr/td/span')
                            # requirements_table_element = driver.find_element(By.ID, Constants.SHIFT_REQUIREMENTS_DIV_ID)
                            # time.sleep(5)
                            search_notice_element = requirements_table_element.find_element(By.CLASS_NAME, Constants.RECORDS_NOT_FOUND_TABLE_CLASS_NAME)
                            # time.sleep(10)
                            requirements_available = False
                            # time.sleep(60)
                            print('requirements_available = False')
                        
                        except:
                            requirements_available = True
                            print('requirements_available = True')

                        if requirements_available:
                            logger.info(f'requirements are available')
                            
                            # get the list of .xlsx files from the download folder before exporting the excel
                            logger.info(f'getting the list of .xlsx files from downloads before exporting excel')
                            list_of_files_before_download = glob.glob(Constants.EXPORT_EXCEL_DOWNLOAD_PATH + '*.xlsx')

                            # export the excel
                            logger.info(f'clicking on the export excel option')
                            export_element = driver.find_element(By.XPATH, Constants.EXPORT_BUTTON_XPATH)
                            export_element.click()
                            time.sleep(2)
                            
                            excel_element = driver.find_element(By.XPATH, Constants.EXPORT_EXCEL_OPTION_XPATH)
                            excel_element.click()
                            time.sleep(10)
                            
                            # scroll the page to the end of the list (infinite scroll)
                            logger.info(f'scrolling the page down (infinite scrolling)')
                            Tasks.infinite_scroll_down(driver)
                            logger.info(f'completed scrolling the page down (infinite scrolling)')

                            # TAKE SCREENSHOT AFTER THE INFINITE SCROLLING
                            # driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.PROJECT_PATH + Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_02_infinite_scrolling_%d_%m_%Y_%H_%M_%S.png')))  #on local
                            driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_02_infinite_scrolling_%d_%m_%Y_%H_%M_%S.png'))) #on docker
                            
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
                                
                                file_name = datetime.now().strftime(os.path.join(Constants.EXPORTED_EXCEL_FILENAME))
                                #moved_exported_file = os.path.join(Constants.PROJECT_PATH + Constants.EXPORTED_EXCELS_FOLDER, file_name)  #on local
                                moved_exported_file = os.path.join(Constants.EXPORTED_EXCELS_FOLDER, file_name)    #on docker
                                dst_file = moved_exported_file

                                shutil.copy(src_file, dst_file)
                            
                            # open the exported excel file
                            logger.info(f'opening the exported excel file in the pandas dataframe')
                            exported_excel_df = pd.read_excel(exported_excel_file[0], sheet_name=Constants.EXCEL_SHEET_NAME)
                            #print('exported_excel_df= ',exported_excel_df.index, len(exported_excel_df.index))
                            if len(exported_excel_df.index) <= 2:
                                logger.info(f'something went wrong, raising the exception to retry the ward selction')
                                raise Exception
                            else:
                                # check the contains of the exported requirements file, verify the
                                # loaction and the ward from the first record from excel with the
                                # loaction and the wards for which scraping is performed
                                location_from_excel = str(exported_excel_df.loc[0, Constants.EXCEL_COLUMN_HEADERS_LIST[1]]).strip()
                                ward_from_excel = str(exported_excel_df.loc[0, Constants.EXCEL_COLUMN_HEADERS_LIST[2]]).strip()
                                if ward_from_excel not in wards_name_list and location_from_excel != location_name:
                                    logger.info(f'Exported excel data is not correct, retry the ward selction')
                                    # scroll the page up to the top of the list
                                    logger.info(f'scrolling the page up to top')
                                    Tasks.scroll_up(driver)
                                    continue
                                else:
                                    pass
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
                                # try:
                                # formulate card id
                                card_element_id = 'b1d9c768-cdd2-44d6-8172-9754ea39a9e7-' + booking_reference_number
                                
                                # # get the A icon section from the cards header section
                                card_element = div_element.find('div', attrs={'id':card_element_id})
                                #header_element = card_element.find('div', attrs={'class':Constants.CARD_HEADER_CLASS_NAME})    #on chrome
                                header_element = card_element.find('td', attrs={'class':Constants.CARD_HEADER_CLASS_NAME})  #on firefox
                                A_icon_element = header_element.find('i')    # here find returns the value None if the element is not found
                                # A_icon_element = driver.find_element(By.XPATH, Constants.CARD_ICOX_XPATH) #'/html/body/div[2]/div/div[2]/div/div[5]/div/div/div[4]/div/div/div/div[2]/div/div[2]/div/div/table/tbody/tr/td[5]/div/i'
                                A_icon_element = card_element.find('i')    # here find returns the value None if the element is not found
                                if A_icon_element == None:
                                    #print('in if of A')
                                    new_row[Constants.EXCEL_EXTRA_COLUMN_HEADER] = 0
                                else:
                                    #print('in else of A')
                                    new_row[Constants.EXCEL_EXTRA_COLUMN_HEADER] = 1
                                # except:
                                #     logging.info(f'In Exception, card element not found. booking_reference_number = {booking_reference_number}')
                                
                                # insert the new row in the dataframe of shift requirements excel
                                df = df.append(new_row, ignore_index=True)
                            
                            logger.info(f'creating the shift requirements excel files')
                            file_name = datetime.now().strftime(os.path.join(Constants.SHIFT_REQUIREMENTS_EXCEL_FILENAME))
                            # shift_requirements_file = os.path.join(Constants.PROJECT_PATH + Constants.SHIFT_REQUIREMENTS_EXCELS_FOLDER, file_name)    #on local
                            shift_requirements_file = os.path.join( Constants.SHIFT_REQUIREMENTS_EXCELS_FOLDER, file_name)  #on docker
                            df.to_excel(shift_requirements_file, sheet_name=Constants.EXCEL_SHEET_NAME, index=False)

                            logger.info(f'creating the collective requirements excel file to check for the cancellation')
                            collective_28_days_df = pd.read_excel(collective_shift_requirements_file, sheet_name=Constants.EXCEL_SHEET_NAME)
                            collective_28_days_df = collective_28_days_df.append(df, ignore_index=True)
                            collective_28_days_df = collective_28_days_df.fillna('')
                            collective_28_days_df.to_excel(collective_shift_requirements_file, sheet_name=Constants.EXCEL_SHEET_NAME, index=False)
                            
                            # scroll the page up to the top of the list
                            logger.info(f'scrolling the page up to top')
                            Tasks.scroll_up(driver)
                        else:
                            logger.info(f'requirements are not available')
                        
                        if iteration_count + 1 == total_iterations_for_parsing:
                            is_all_wards_parsed = True
                            continue # or break
                        else:
                            is_all_wards_parsed = False
                            iteration_count = iteration_count + 1
                    except ElementClickInterceptedException:
                        # TAKE SCREENSHOT AFTER ERROR
                        # driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.PROJECT_PATH + Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_after_error_occured_%d_%m_%Y_%H_%M_%S.png')))    #on local
                        driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_after_error_occured_%d_%m_%Y_%H_%M_%S.png')))   #on docker

                        exception_type, exception_value, exception_traceback = sys.exc_info()
                        traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
                        err_msg = json.dumps({
                            "errorType": exception_type.__name__,
                            "errorMessage": str(exception_value),
                            "stackTrace": traceback_string
                        })
                        logger.error(f'ElementClickInterceptedException error occured while scraping ward: {err_msg}')
                        
                        driver.close()
                        driver.quit()
                        logger.info(f'closed the browser window')

                        location_scraping_end_time = time.time()
                        location_scraping_total_time = location_scraping_end_time - location_scraping_start_time
                        logger.info(f'Time required for the execution is {location_scraping_total_time}')

                        # update the break flag to retry the entire location scraping
                        logger.info("Raise exception and Retry the entire location scraping")
                        break_flag = True
                        break
                    except Exception:
                        # TAKE SCREENSHOT AFTER ERROR
                        # driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.PROJECT_PATH + Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_after_error_occured_%d_%m_%Y_%H_%M_%S.png')))    #on local
                        driver.get_screenshot_as_file(datetime.now().strftime(os.path.join( Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_after_error_occured_%d_%m_%Y_%H_%M_%S.png')))  #on docker

                        exception_type, exception_value, exception_traceback = sys.exc_info()
                        traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
                        err_msg = json.dumps({
                            "errorType": exception_type.__name__,
                            "errorMessage": str(exception_value),
                            "stackTrace": traceback_string
                        })
                        logger.error(f'Error Occured while scraping ward: {err_msg}')
                        logger.info(f'Retrying with the wards selection')
                        
                        # scroll the page up to the top of the list
                        logger.info(f'scrolling the page up to top')
                        Tasks.scroll_up(driver)
                
                # check the break flag
                if break_flag:
                    raise Exception
                
                # update the loop variables and check if all locations are parsed
                total_parsed_wards = total_parsed_wards + total_wards
                total_parsed_locations = total_parsed_locations + 1
                location_name_list.append(location_name)
                if location_index + 1 == len(location_menu_options_elements):
                    is_all_locations_parsed = True
                    continue # or break
                else:
                    is_all_locations_parsed = False
                    location_index = location_index + 1

            # logout the portal
            logger.info(f'checking and clicking on the logout navigation menu panel')
            navigation_menu_dropdown_element = driver.find_element(By.ID, Constants.LOGOUT_NAVIGATION_DROPDOWN_MENU_ID)
            navigation_menu_dropdown_element.click()
            time.sleep(1)
            
            logger.info(f'clicking on the logout menu button')
            navigation_menu_element = driver.find_element(By.ID, Constants.LOGOUT_NAVIGATION_MENU_ID)
            logout_element = navigation_menu_element.find_element(By.LINK_TEXT, Constants.LOGOUT_OPTION_NAME)
            logout_element.click()
            time.sleep(2)
            
            logger.info(f'logout completed')

            driver.close()
            driver.quit()
            logger.info(f'closed the browser window')

            location_scraping_end_time = time.time()
            location_scraping_total_time = location_scraping_end_time - location_scraping_start_time
            location_names_str = ', '.join(location_name_list)
            logger.info(f'Total time required for the scraping requirements for locations "{location_names_str}" is {location_scraping_total_time}')
            # remove_file_handler_logger()
        except Exception:
            try:
                # TAKE SCREENSHOT AFTER ERROR
                # driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.PROJECT_PATH + Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_after_error_occured_%d_%m_%Y_%H_%M_%S.png')))    #on local
                driver.get_screenshot_as_file(datetime.now().strftime(os.path.join(Constants.EXECUTION_SCREENSHOTS_FOLDER, '28_days_after_error_occured_%d_%m_%Y_%H_%M_%S.png')))   #on docker
                driver.close()
                driver.quit()
            except:
                logger.info(f'Inside the exception of capture error screenshot, drive not initialised')
           
           
            exception_type, exception_value, exception_traceback = sys.exc_info()
            traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
            err_msg = json.dumps({
                "errorType": exception_type.__name__,
                "errorMessage": str(exception_value),
                "stackTrace": traceback_string
            })
            logger.error(f'Error Occured while scraping location: {err_msg}')

            
            logger.info(f'closed the browser window')

            location_scraping_end_time = time.time()
            location_scraping_total_time = location_scraping_end_time - location_scraping_start_time
            logger.info(f'Time required for the execution is {location_scraping_total_time}')
            # remove_file_handler_logger()
            
        return is_all_locations_parsed, location_index

    def download_chrome_driver():
        try:
            response = urllib.request.urlopen(Constants.GET_LATEST_CHROME_DRIVER_VERSION_URL)
            status_code = response.getcode()
            response_json = response.read().decode('UTF-8')
            logger.info(f'api 1 status_code - {status_code}')
            response_json = json.loads(response_json)
            driver_version = response_json['channels']['Stable']['version']
            logger.info(f'driver_version - {driver_version}')

            response = urllib.request.urlopen(Constants.GET_CHROME_DRIVER_DOWNLOAD_PATH_URL)
            status_code = response.getcode()
            response_json = response.read().decode('UTF-8')
            logger.info(f'api 2 status_code - {status_code}')
            response_json = json.loads(response_json)
            drivers_download_list = response_json['channels']['Stable']['downloads']['chromedriver']
            for json_element in drivers_download_list:
                driver_download_platform = drivers_download_list[4]['platform'] #on local for windows
                # driver_download_platform = drivers_download_list[0]['platform'] #on docker for linux
                if driver_download_platform == Constants.CHROME_DRIVER_DOWNLOAD_PLATFORM:
                    driver_download_url = drivers_download_list[4]['url']     #on local for windows
                    # driver_download_url = drivers_download_list[0]['url']       #on docker for linux
                    
            logger.info(f'driver_download_url - {driver_download_url}')
            
            logger.info(f'Downloading Started')
            response = requests.get(driver_download_url)
            file_name = driver_download_url.split('/')[-1]
            file_path = Constants.CHROME_DRIVER_DOWNLOAD_FOLDER + '\\' + file_name  #on local
            file_path = Constants.CHROME_DRIVER_DOWNLOAD_FOLDER + '/' + file_name     #for docker
            file_path = '/tmp/' + file_name                                            #for docker
            folder_name = str(file_name).replace('.zip', '')
            with open(file_path, 'wb') as output_file:
                output_file.write(response.content)
            
            logger.info(f'filename - {file_name}')
            zip_file = zipfile.ZipFile(BytesIO(response.content))
            # zip_file.extractall(Constants.CHROME_DRIVER_DOWNLOAD_FOLDER)
            zip_file.extractall(Constants.CHROME_DRIVER_DOWNLOAD_FOLDER)
            
            driver_path = Constants.CHROME_DRIVER_DOWNLOAD_FOLDER + '//' + folder_name + '//' + Constants.CHROME_DRIVER_FILE_NAME      #on local for window
            # # driver_path = Constants.CHROME_DRIVER_DOWNLOAD_FOLDER + '/' + folder_name + '/' + Constants.CHROME_DRIVER_FILE_NAME      #on docker for linux
            # driver_path = Constants.CHROME_DRIVER_DOWNLOAD_FOLDER + '/' + folder_name + '/' +  Constants.CHROME_DRIVER_FILE_NAME                                                         #on docker for linux
            logger.info(f'Downloading Completed')
        except Exception:
            exception_type, exception_value, exception_traceback = sys.exc_info()
            traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
            err_msg = json.dumps({
                "errorType": exception_type.__name__,
                "errorMessage": str(exception_value),
                "stackTrace": traceback_string
            })
            logger.error(f'Error Occured while downloading the chrome driver: {err_msg}')
            driver_path = Constants.CHROME_DRIVER_DOWNLOAD_FOLDER + '//chromedriver-win64//' + Constants.CHROME_DRIVER_FILE_NAME  #on local for windows driver
            # driver_path = Constants.CHROME_DRIVER_DOWNLOAD_FOLDER + '/chromedriver-win64/' + Constants.CHROME_DRIVER_FILE_NAME
            # driver_path = Constants.CHROME_DRIVER_DOWNLOAD_FOLDER + '/chromedriver-linux64/' + Constants.CHROME_DRIVER_FILE_NAME  #on docker for linux driver

        return driver_path


class ArchiveFiles():
    
    def delete_files_based_on_date():
        ### modify paths, store in list        
        ######modify file list
        for directory in Constants.DELETE_FILES_DIRECTORY_LIST:
            threshold_date = datetime.now() - timedelta(days=Constants.DAYS_THRESHOLD)
            print('directory= ',directory)
            # logger.info(f'#'*50,'Delete files execution started')
            
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
                print('creation_time= ',creation_time, ' threshold_date= ',threshold_date)
                # print('file_path= ',file_path)
                
                if creation_time < threshold_date:
                    try:
                        os.unlink(file_path)
                        # logger.info(f'Deleted file {file_path}')
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")
                        # logger.error(f'error while deleting file {file_path}: {e}')
             
             
# if __name__ == '__main__':
#     NHSPPortalScraping.scraping_requirements()
