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
import pandas as pd
from datetime import datetime, timedelta
import glob
from common_28_days_scraping import Constants
import os

"""
def scrape_test():
# for firefox browser
    # try:
            options = FirefoxOptions()
            # options.set_preference("browser.download.folderList", 2)
            # options.set_preference("browser.download.dir", Constants.EXPORT_EXCEL_DOWNLOAD_PATH)
            # options.set_preference("browser.download.manager.showWhenStarting", False)
            # options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
            # options.add_argument('-headless')
            # driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            # # driver = webdriver.Firefox()
            
            # # minimize the window size to view the requirements in the cards format
            # window_size = driver.get_window_size()
            # window_width = window_size['width'] - ((window_size['width']/100) * 20)
            # window_height = window_size['height'] - ((window_size['height']/100) * 7)
            # driver.set_window_size(window_width, window_height)
            
            options = ChromeOptions()
            # prefs = {'download.default_directory': Constants.EXPORT_EXCEL_DOWNLOAD_PATH}
            # options.add_experimental_option('prefs', prefs)
            # options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
    
            driver = webdriver.Chrome(service=ChromeService(executable_path='D:\EPI_Saniya\ID-Medical\east_kent\chromedriver-win64\chromedriver.exe'), options=options)
            
            print('start')
            
            # https://bookings.nhsprofessionals.nhs.uk/NewLoginFrame.asp
            # Anthony.grubb
            # Arsenal25071985
            
            driver.get('https://bookings.nhsprofessionals.nhs.uk/NewLoginFrame.asp')
            
            print(f'login page opened')
            # driver.implicitly_wait(10)
            
            source= driver.page_source
            print(source)
            driver.switch_to.frame('body')
            # time.sleep(5)
                       
            username = driver.find_element(By.XPATH, '/html/body/form/center/table/tbody/tr[1]/td/table[1]/tbody/tr[2]/td/table/tbody/tr/td[2]/input')
            # username = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/center/table/tbody/tr[1]/td/table[1]/tbody/tr[2]/td/table/tbody/tr/td[2]/input')))
            
            username.clear()
            username.send_keys('Anthony.grubb')
            time.sleep(1)
            password = driver.find_element(By.NAME, 'PIN')
            password.clear()
            password.send_keys('Arsenal25071985')
            time.sleep(1)
            
            login = driver.find_element(By.XPATH, '/html/body/form/center/table/tbody/tr[1]/td/table[2]/tbody/tr/td/input')
            login.click()

            print(f'clicked Login')
            time.sleep(2)
            source= driver.page_source
            # # print('after login=\n',source)
            # file = open('contents.txt', 'w')
            # file.write(source)
            # file.close()
            
            driver.switch_to.frame('toc')
            # source1= driver.page_source
            # file = open('content1.txt', 'w')
            # file.write(source1)
            # file.close()
            # print('after login 1=\n',source)
            
            # source2= driver.page_source
            # file = open('content2.txt', 'w')
            # file.write(source2)
            # file.close()
            # time.sleep(3)
            
            view_request=driver.find_element(By.ID, 'linkViewRequests')
            view_request.click()
            time.sleep(3)
            print('clicked view request')
            
            driver.switch_to.default_content()
            # frame = driver.find_element(By.NAME, 'content')
            driver.switch_to.frame('content')
            driver.switch_to.frame('MenuDetailsWindow')
            
            # agency_req_filter_trust = driver.find_element(By.ID, 'DropDownList_Trust')
            # agency_req_filter_trust.click()
            # time.sleep(1)
            
            #select name 
            select_name = driver.find_element(By.XPATH, '//*[@id="DropDownList_Trust"]/option[10]')
            time.sleep(2)
            select_name.click()
            
            print('selected trust name')
        
            time.sleep(2)
            
            
            submit_btn = driver.find_element(By.NAME, 'btnSumbit')
            submit_btn.click()
            time.sleep(20)
            print('clicked submit button for default filter')
            
            # empty dataframe to store data of all tables
            combined_data = pd.DataFrame()
        
            record_not_found = False
            try:
                no_record_msg = driver.find_element(By.ID, 'lblNoRecord_msg')
                print('no_record_msg= ',no_record_msg.text)
                record_not_found = True
            except:
                print('inside exception of recor_not_found')
                record_not_found = False
                       
            if not record_not_found:
                table_element = driver.find_element(By.ID, 'AgencyRequestsBookings_dynamicPanel')
            
                table_html = table_element.get_attribute("outerHTML")
                # table_data = []
                
                # Convert the scraped table to Pandas DataFrame
                # table_data.append(pd.read_html(table_html)[0])
                table_data = pd.read_html(table_html)[0]
                print('append to empty frame')
                combined_data = table_data
            # print('showing data\n', table_data)
            
            #back button click
            back_to_submit = driver.find_element(By.ID, 'Button_BackToSubmit')
            time.sleep(5)
            back_to_submit.click()
            time.sleep(3)
            print('back button clicked')
            
    ##### Checking for next filters ####################
            
            # Start: 2024-01-14 16:37:09.274510, End: 2024-01-22 16:37:09.274510
            # Start: 2024-01-22 16:37:09.274510, End: 2024-01-30 16:37:09.274510
            # Start: 2024-01-30 16:37:09.274510, End: 2024-02-07 16:37:09.274510
            # Start: 2024-02-07 16:37:09.274510, End: 2024-02-15 16:37:09.274510
            interval_start_date = datetime.now() + timedelta(days=8)
            
            # Generate time intervals for the next 28 days, every 7 days
            for i in range(3):
                select_name = driver.find_element(By.XPATH, '//*[@id="DropDownList_Trust"]/option[10]')
                select_name.click()
                time.sleep(2)
            
                interval_start = (interval_start_date + timedelta(days=i * 7)).strftime('%d/%m/%Y')
                print('interval_start= ',interval_start)
                interval_end = (datetime.strptime(interval_start, '%d/%m/%Y') + timedelta(days=6)).strftime('%d/%m/%Y')
                # time_intervals.append((interval_start, interval_end))
                print(f"Start: {interval_start}, End: {interval_end}")
                start_date = driver.find_element(By.NAME, 'panel_StartDate')
                start_date.clear()
                start_date.send_keys(str(interval_start))
                time.sleep(1)
               
                end_date = driver.find_element(By.NAME, 'panel_EndDate')
                end_date.clear()
                end_date.send_keys(str(interval_end))
                
                print('clicked submit button')
                #submit after filter selection
                submit_btn = driver.find_element(By.NAME, 'btnSumbit')
                submit_btn.click()
                time.sleep(30)
                recor_not_found = False
                try:
                    no_record_msg = driver.find_element(By.ID, 'lblNoRecord_msg')
                    print('no_record_msg= ',no_record_msg.text)
                    recor_not_found = True
                except:
                    print('inside exception of recor_not_found')
                    recor_not_found = False
                    
               

                if not recor_not_found:
                    # Replace the commented lines with your actual scraping logic
                    # For demonstration purposes, let's assume the table has the ID "example_table"
                    table_element = driver.find_element(By.ID, 'AgencyRequestsBookings_dynamicPanel')
                    
                    table_html = table_element.get_attribute("outerHTML")
                    table_data = pd.read_html(table_html)[0]
                    # Convert the scraped table to Pandas DataFrame
                    # table_data.append(pd.read_html(table_html)[0])
                    if combined_data.empty:
                        print('append to empty frame')
                        combined_data = table_data
                    else:
                        print('append data')
                        # Append data to the combined DataFrame without repeating column names
                        combined_data = combined_data.append(table_data, ignore_index=True)
                        
                    # rows_to_skip = [0]
                    # # Iterate through the rows of the table
                    # for row_index, row in enumerate(table_element.find_elements(By.TAG_NAME, "tr")):
                    #     print('inside skip row loop')
                    #     if row_index not in rows_to_skip:
                    #         print('row_index=',row_index,'row= ',row)
                    #         # Extract data from each column in the row (replace this with your actual logic)
                    #         columns = row.find_elements(By.TAG_NAME, "td")
                    #         row_data = [column.text for column in columns]
                    #         table_data.append(row_data)
                            
                    # print('showing data\n', table_data)
                    #back button click
                    back_to_submit = driver.find_element(By.ID, 'Button_BackToSubmit')
                    time.sleep(5)
                    back_to_submit.click()
                    time.sleep(3)
                    print('back button clicked')
            
            
            # Convert the scraped table to Excel
            # df = pd.DataFrame(table_data)
            
            
            excel_filename = "scraped_table2.xlsx"
            # table_data.to_excel(excel_filename, index=False)
            combined_data.to_excel(excel_filename, index=False)
            
            driver.switch_to.default_content()
            # frame = driver.find_element(By.NAME, 'content')
            driver.switch_to.frame('content')
            driver.switch_to.frame('MainMenuWindow')
            logout = driver.find_element(By.ID, 'LogoutImage')
            time.sleep(3)
            logout.click()
            time.sleep(5)
            print('logged out')
            driver.close()
            
# ##########################################################################

#             agency_req_filter_trust = driver.find_element(By.ID, 'DropDownList_Trust')
#             agency_req_filter_trust.click()
#             time.sleep(1)
#             select_name = driver.find_element(By.XPATH, '//*[@id="DropDownList_Trust"]/option[10]')
#             select_name.click()
#             time.sleep(5)
            
#             start_date = driver.find_element(By.NAME, 'panel_StartDate')        
#             start_date.click()
            
#             next_month = driver.find_element(By.ID, 'ctl06_nextArrow')
#             next_month.click()
#             time.sleep(3)
            
#             start_date = driver.find_element(By.ID, 'ctl06_day_2_6')
#             start_date.click()
#             time.sleep(2)
            
#             # end_date = driver.find_element(By.XPATH,'//*[@id="ctl08_daysBody"]/tr[4]/td[7]')
#             end_date = driver.find_element(By.NAME, 'panel_EndDate')
#             end_date.click()
#             end_date = driver.find_element(By.ID,'ctl08_day_3_6')
#             end_date.click()
#             time.sleep(2)
            
#             submit_btn = driver.find_element(By.NAME, 'btnSumbit')
#             submit_btn.click()
            
#             time.sleep(30)
            
            
            
    # except:
    #     print('inside exception')
    #     driver.close()
    
"""

def data_manupulate():
    # exported_excel_file = glob.glob(Constants.REQUIREMENT_FILES_FOLDERPATH + '*.xlsx')
    # print('exported_excel_file=',exported_excel_file)  
    # exported_excel_df = pd.read_excel(exported_excel_file[0], sheet_name='Sheet1')
            
    # filtered_df = exported_excel_df[:-2]
    # print('filtered_df= ',filtered_df)
    # # filtered_df = filtered_df[filtered_df[Constants.EXCEL_COLUMN_HEADERS_LIST[7]] != 'Unfilled']
    # filtered_df = filtered_df[Constants.EXCEL_COLUMN_HEADERS_LIST]
    # filtered_df = filtered_df.fillna('')
    
    # # file_name = datetime.now().strftime(os.path.join(Constants.FILE_NAME_OF_SCRAPED_DATA))
    # # filled_requirements_file = os.path.join(Constants.FILLED_REQUIREMENTS_EXCELS_FOLDER, file_name)
    # filtered_df.to_excel(exported_excel_file[0], index=False)
    # # print('filtered_df1= ',filtered_df)
    
     # filter the not compared records from the summary dataframe
    unfilled_scraping_summary_excel_df = pd.read_excel(Constants.UNFILLED_SCRAPING_SUMMARY_FILE_NAME, sheet_name=Constants.SCRAPING_SUMMARY_EXCEL_SHEET_NAME)
    filtered_unfilled_scraping_summary_excel_df = unfilled_scraping_summary_excel_df[unfilled_scraping_summary_excel_df[Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]] == 'no']
    # print('filtered_unfilled_scraping_summary_excel_df= ',filtered_unfilled_scraping_summary_excel_df)
    # print('filtered_unfilled_scraping_summary_excel_df= ',filtered_unfilled_scraping_summary_excel_df.index, '| ', len(filtered_unfilled_scraping_summary_excel_df))
    unique_execution_dates = filtered_unfilled_scraping_summary_excel_df['Execution Date'].unique()
    print(unique_execution_dates)
    # Iterate over each execution date
    for date in unique_execution_dates:
        print('date= ',date)
        records_for_date = filtered_unfilled_scraping_summary_excel_df[filtered_unfilled_scraping_summary_excel_df['Execution Date'] == date]

        # Sort records by a unique identifier (assuming 'ID' is the identifier)
        sorted_records = records_for_date.sort_values(by='Execution Date')
        print('sorted_records = ',len(sorted_records))
        
        if len(sorted_records) == 1:
            #update record in summary file {is comared= yes, file name =compared }
            pass
        else:
            # Compare consecutive records for 'isCompared' status
            for i in range(len(sorted_records) - 1):
                prev_record = sorted_records.iloc[i]
                curr_record = sorted_records.iloc[i + 1]
                # print('current_record=',current_record['Is Comparision Completed'])
                if prev_record['Is Comparision Completed'] == 'no': # and next_record['Is Comparision Completed'] == 'no':
                    # Perform actions for not compared records
                    print(f"Not compared prev_record records for execution date {date}:\n{prev_record['Execution Date'], prev_record['Requirements Filename']}")
                    
                if curr_record['Is Comparision Completed'] == 'no':
                    # Perform actions for not compared records
                    print(f"Not compared curr_record records for execution date {date}:\n{curr_record['Execution Date'], curr_record['Requirements Filename']}")
    # # check if the records for comparision are more than 0
    # if len(filtered_unfilled_scraping_summary_excel_df.index) > 1:
    #             files_found = False
    #             # logging.info(f'summary records available for the comparision')
    #             for i in range(len(filtered_unfilled_scraping_summary_excel_df.index)):
    #                 # while not files_found:
    #                     unfilled_execution_date_file1 = filtered_unfilled_scraping_summary_excel_df.loc[filtered_unfilled_scraping_summary_excel_df.index[i], Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[0]]
    #                     unfilled_execution_date_file2 = filtered_unfilled_scraping_summary_excel_df.loc[filtered_unfilled_scraping_summary_excel_df.index[i+1], Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[0]]
    #                     print('iii = ',unfilled_execution_date_file1, unfilled_execution_date_file2)
                        
    #                     if unfilled_execution_date_file1 == unfilled_execution_date_file2:
    #                         files_found = True
    #                         print('break=============================================')
    #                         break
                                
        
    #             print('11 = ',unfilled_scraping_summary_excel_df,'** ', filtered_unfilled_scraping_summary_excel_df,'** ', len(filtered_unfilled_scraping_summary_excel_df.index))
    #         #   # get the row index values
    #         #     unfilled_row_index0 = filtered_unfilled_scraping_summary_excel_df.index[0]
    #         #     unfilled_row_index1 = filtered_unfilled_scraping_summary_excel_df.index[1]
    #         #     print('unfilled_row_index0= ',unfilled_row_index0)
    #         #     unfilled_requirements_file_path1 = os.path.join(Constants.PROJECT_PATH + Constants.REQUIREMENT_EXCEL_FOLDER + '\\' + filtered_unfilled_scraping_summary_excel_df.loc[unfilled_row_index0, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[2]])
    #         #     unfilled_requirements_file_path2 = os.path.join(Constants.PROJECT_PATH + Constants.REQUIREMENT_EXCEL_FOLDER + '\\' + filtered_unfilled_scraping_summary_excel_df.loc[unfilled_row_index1, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[2]])
    #         #     # logging.info(f'unfilled_requirements_file_path - {unfilled_requirements_file_path}')
    #         #     unfilled_requirements_file1_df = pd.read_excel(unfilled_requirements_file_path1, sheet_name=Constants.REQIREMENTES_EXCEL_SHEET_NAME)
    #         #     # unfilled_requirements_file1_bank_req_id_list = unfilled_requirements_file1_df['Bank Req Num'].tolist()
    #         #     unfilled_requirements_file2_df = pd.read_excel(unfilled_requirements_file_path2, sheet_name=Constants.REQIREMENTES_EXCEL_SHEET_NAME)
    #         #     unfilled_requirements_file2_bank_req_id_list = unfilled_requirements_file2_df['Bank Req Num'].tolist()
                
    #         #     # # find the difference and get the requirements which are now filled by bank
    #         #     closed_requirements_df = unfilled_requirements_file1_df[~unfilled_requirements_file1_df['Bank Req Num'].isin(unfilled_requirements_file2_bank_req_id_list)]
    #         #     print('requirements_filled_df= ',closed_requirements_df)
                
    #         #     previous_date = datetime.now() - timedelta(days = 1)
    #         #     previous_date_str = previous_date.strftime('%d-%b-%Y')
    #         #     current_date = datetime.now()
    #         #     current_date_str = current_date.strftime('%d-%b-%Y')
    #         #     # logging.info(f'removing the previous and current date requirements from the cancelled requirements')
    #         #     completely_missing_requirements_df = closed_requirements_df[~closed_requirements_df['Date'].isin([previous_date_str, current_date_str])]
    #         #     print('completely_missing_requirements_df= ',completely_missing_requirements_df)
                
    #         #     # # check if the dataframe has rows greater than 0 then generate the cancellation excel
    #         #     # # else check the next comparision and update the summary dataframe with appropriate values
    #         #     if len(completely_missing_requirements_df.index) > 0:
    #         #         
    #         #         cancellation_df = completely_missing_requirements_df
                    
    #         #             # i/ += 1
    #         #     #     # logging.info(f'creating the requirements cancellation excel file')
    #         #         file_name = datetime.now().strftime(os.path.join(Constants.REQUIREMENTS_CANCELLATION_EXCEL_FILENAME))
    #         #         requirements_cancellation_28_days_file = os.path.join(Constants.PROJECT_PATH + Constants.REQUIREMENTS_CANCELLATION_EXCELS_FOLDER, file_name) #on local
    #         #         cancellation_df.to_excel(requirements_cancellation_28_days_file, sheet_name=Constants.CANCELLATION_EXCEL_SHEET_NAME, index=False)
    #         #         print('*****=\n',unfilled_scraping_summary_excel_df.loc[unfilled_row_index0, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]])
                    
    #         #         # unfilled_scraping_summary_excel_df.loc[unfilled_row_index0,  Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]] = 'yes'
    #         #         unfilled_scraping_summary_excel_df.loc[unfilled_row_index0, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3] ] = 'yes'
    #         #         unfilled_scraping_summary_excel_df.loc[unfilled_row_index0, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[4]] = file_name
    #         #         unfilled_scraping_summary_excel_df.to_excel(Constants.UNFILLED_SCRAPING_SUMMARY_FILE_NAME, sheet_name=Constants.SCRAPING_SUMMARY_EXCEL_SHEET_NAME, index=False)
                    
    #         #         print('*****2=\n',unfilled_scraping_summary_excel_df.loc[unfilled_row_index0, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]])
    #         #         time.sleep(1)
    #         #     else:
    #         #         # logging.info(f'no difference between the unfilled and filled scraped requirements')
    #         #         unfilled_scraping_summary_excel_df.loc[unfilled_row_index0, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[3]] = 'yes'
    #         #         unfilled_scraping_summary_excel_df.loc[unfilled_row_index0, Constants.SCRAPING_SUMMARY_COLUMN_HEADERS_LIST[4]] = 'No Difference'
    #         #         unfilled_scraping_summary_excel_df.to_excel(Constants.UNFILLED_SCRAPING_SUMMARY_FILE_NAME, sheet_name=Constants.SCRAPING_SUMMARY_EXCEL_SHEET_NAME, index=False)
    
                    
    # else:
    #     # logging.info(f'summary records are not available for the comparision')
    #     print('summary records are not available for the comparision')
    # start_date = datetime.now().date()
    # interval_days = 7
    # intervals = []
    # for i in range(4):
    #     interval_start = start_date + timedelta(days=i * interval_days)
    #     interval_end = start_date + timedelta(days=(i + 1) * interval_days - 1)
    #     intervals.append((interval_start, interval_end))
    # print(intervals)
  
if __name__ == '__main__':
    # scrape_test()
    data_manupulate()
          