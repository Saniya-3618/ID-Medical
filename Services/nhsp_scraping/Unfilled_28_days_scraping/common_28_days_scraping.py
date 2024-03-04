import time


class Constants:
    GET_LATEST_CHROME_DRIVER_VERSION_URL = 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json'
    GET_CHROME_DRIVER_DOWNLOAD_PATH_URL = 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json'
    CHROME_DRIVER_DOWNLOAD_PLATFORM = 'win64'   #on local
    # CHROME_DRIVER_DOWNLOAD_PLATFORM = 'linux64'   #on docker
    CHROME_DRIVER_DOWNLOAD_FOLDER = 'chrome_driver'   #on local
    # CHROME_DRIVER_DOWNLOAD_FOLDER = '/app/chrome_driver'  #on docker
    # CHROME_DRIVER_DOWNLOAD_FOLDER = '/usr/local/bin'   #on docker
    CHROME_DRIVER_FILE_NAME = 'chromedriver.exe'
    # CHROME_DRIVER_FILE_NAME = 'chromedriver'

    PORTAL_LINK = 'https://bank.nhsp.uk/ourbank'
    # PORTAL_CREDENTIALS = {'username': 'EPreneursOH', 'password': 'z5ENa8B5yTN9'}
    PORTAL_CREDENTIALS = {'username': 'EPreneursOH', 'password': 'Welcome24'}

    USERNAME_FIELD_ID = 'login'
    PASSWORD_FIElD_ID = 'password'
    LOGIN_BUTTON_ID = 'log'

    NAVIGATION_PANEL_DIV_ID = 'navbar'
    NEXT_3_DAYS_TAB_NAME = 'Next 3 days'
    NEXT_28_DAYS_TAB_NAME = '28 Days'

    FILTER_MENU_XPATH = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div[2]/div[1]'
    FILTER_STATUS_UNFILLED_OPTION_XPATH = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div[2]/div[2]/div/div[2]/div[4]/div/select/option[5]'
    FILTER_AUTHORISATION_ALL_OPTION_XPATH = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div[2]/div[2]/div/div[2]/div[3]/div/select/option[1]'

    LOCATION_DROPDOWN_XPATH = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div[3]/div/div[1]/div[1]/div/div/select'
    
    WARD_DROPDOWN_XPATH = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div'
    WARD_DROPDOWN_OPTIONS_CLASS_NAME = 'ng-scope'
    
    DATE_RANGE_DROPDOWN_XPATH = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div[3]/div/div[1]/div[3]/div/div/input'
    DATE_RANGE_DROPDOWN_OPTIONS_CLASS_NAME = 'daterangepicker'
    DATE_RANGE_OPTIONS = ['Next 28 days', 'Next 7 days', 'Next 72 hours', 'Next 24 hours', 'Tomorrow']

    SEARCH_BUTTON_XPATH = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div[3]/div/div[1]/div[4]/div/button'
    
    DATA_LOADER_XPATH = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div[1]/div/span/div'
    
    SHIFT_REQUIREMENTS_DIV_ID = 'reactcontentb1d9c768-cdd2-44d6-8172-9754ea39a9e7'
    
    RECORDS_NOT_FOUND_TABLE_CLASS_NAME = 'search_notice_table'    #on chrome
    # RECORDS_NOT_FOUND_TABLE_CLASS_NAME = 'search_notice_td'  #on firefox
    
    # RECORDS_NOT_FOUND_TABLE_CLASS_NAME = 'col-xs-12 col-sm-12 col-md-12 col-lg-12 search_notice_td'
    
    EXPORT_BUTTON_XPATH = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div[3]/div/div[1]/div[4]/div/div[1]/button'
    EXPORT_EXCEL_OPTION_XPATH = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div[3]/div/div[1]/div[4]/div/div[1]/ul/li[1]/a'

    CARD_HEADER_CLASS_NAME = 'isotonHeader' #on chrome
    # CARD_HEADER_CLASS_NAME = 'min-w220' #on firefox
    CARD_ICOX_XPATH = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div[4]/div/div/div/div[2]/div/div[2]/div/div/table/tbody/tr/td[5]/div/i'
    
    LOGOUT_NAVIGATION_DROPDOWN_MENU_ID = 'desktop-toggle'
    LOGOUT_NAVIGATION_MENU_ID = 'navbar_menu'
    LOGOUT_OPTION_NAME = 'Logout'

    # EXPORT_EXCEL_DOWNLOAD_PATH = 'C:\\Users\\Kapil.Patil\\Downloads\\unfilled\\28_days\\'
    EXPORT_EXCEL_DOWNLOAD_PATH = 'C:\\Users\\saniya.pathan\\Downloads\\unfilled\\28_days\\'
    # EXPORT_EXCEL_DOWNLOAD_PATH = '/home/seluser/Downloads/'
    # EXPORT_EXCEL_DOWNLOAD_PATH = '/app/Downloads/unfilled/28_days/' 
    # PROJECT_PATH = 'C:\\IDMedical\\Python Parser\\CodeBase\\NHSP Unfilled Requirements Scraping\\'
    # PROJECT_PATH = 'D:\\EPI_Saniya\\ID-Medical\\ID-Medical Data\\NHSP Unfilled Requirements Scraping\\'
    PROJECT_PATH = 'D:\\EPI_Saniya\\Id-Medical_old\\Services\\nhsp_scraping\\Unfilled_28_days_scraping\\'
    
    EXPORTED_EXCELS_FOLDER = 'exported_excels'
    SHIFT_REQUIREMENTS_EXCELS_FOLDER = 'shift_requirements_excels'
    EXECUTION_LOGS_FOLDER = 'execution_logs'
    EXECUTION_SCREENSHOTS_FOLDER = 'screenshots'

    EXPORTED_EXCEL_FILENAME = '28_Days_Exported_Excel_%d_%m_%Y_%H_%M_%S.xlsx'
    SHIFT_REQUIREMENTS_EXCEL_FILENAME = '28_Days_Shift_Requirements_Excel_%d_%m_%Y_%H_%M_%S.xlsx'
    EXECUTION_LOGS_FILENAME = '28_Days_logfile_%d_%m_%Y_%H_%M_%S.log'

    EXCEL_COLUMN_HEADERS_LIST = ['Booking Reference Number', 'Location', 'Ward', 'Shift Date', 'Start Time', 'End Time', 'Assignment Code', 'Status', 'Secondary Assignment Code', 'Notes', 'Gender', 'Booking Reason']
    EXCEL_EXTRA_COLUMN_HEADER = 'Worker'
    EXCEL_SHEET_NAME = 'Shifts'

    # REQUIREMENTS_FOR_COMPARE_EXCEL_PATH = 'C:\\IDMedical\\Python Parser\\CodeBase\\NHSP Filled Requirements Scraping And Cancellation\\28_days_requirements_excels\\unfilled\\'
    # REQUIREMENTS_FOR_COMPARE_EXCEL_PATH = 'D:\\EPI_Saniya\\ID-Medical\\ID-Medical Data\\NHSP Filled Requirements Scraping And Cancellation\\28_days_requirements_excels\\unfilled\\'
    REQUIREMENTS_FOR_COMPARE_EXCEL_PATH = 'D:\\EPI_Saniya\\Id-Medical_old\\Services\\nhsp_scraping\\Filled_cancellation_28_days_scraping\\28_days_requirements_excels\\unfilled\\'
    # REQUIREMENTS_FOR_COMPARE_EXCEL_PATH = '/app/28_days_requirements_excels/unfilled/'    #for docker
    # REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_FILE_PATH = 'C:\\IDMedical\\Python Parser\\CodeBase\\NHSP Filled Requirements Scraping And Cancellation\\28_Days_Unfilled_Requirements_Scraping_Execution_Summary.xlsx'
    # REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_FILE_PATH = 'D:\\EPI_Saniya\\ID-Medical\\ID-Medical Data\\NHSP Filled Requirements Scraping And Cancellation\\28_Days_Unfilled_Requirements_Scraping_Execution_Summary.xlsx'
    REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_FILE_PATH = 'D:\\EPI_Saniya\\Id-Medical_old\\summary_files\\28_Days_Unfilled_Requirements_Scraping_Execution_Summary.xlsx'
    # REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_FILE_PATH = '28_Days_Unfilled_Requirements_Scraping_Execution_Summary.xlsx'
    REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_EXCEL_SHEET_NAME = 'Scraping Summary'
    SCRAPING_SUMMARY_COLUMN_HEADERS_LIST = ['Execution Date', 'Execution Time', 'Requirements Filename', 'Is Comparision Completed', 'Requirements Cancellation Filename']

    SCROLL_PAUSE_TIME = 6

    TOTAL_WARDS_FOR_PARSING = 5

    # this limit is only for the locations whose wards count is very less
    TOTAL_WARDS_FOR_SCRAPING_IN_ONE_LOGIN = 15

    DELETE_FILES_DIRECTORY_LIST = ['/app/3_days_requirements_excels/filled/', '/app/execution_logs/', '/app/screenshots/']
    DAYS_THRESHOLD = 7
    ARCHIVE_TASK_LOG_FILE = 'Delete_Files_logfile_%d_%m_%Y_%H_%M_%S.log'
    
    
class Tasks:
    def infinite_scroll_down(driver):
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait to load page
            time.sleep(Constants.SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # If heights are the same it will exit the function
                break
            last_height = new_height
        return
    
    def scroll_up(driver):
        # Scroll up to top
        driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
        time.sleep(2)
        return
