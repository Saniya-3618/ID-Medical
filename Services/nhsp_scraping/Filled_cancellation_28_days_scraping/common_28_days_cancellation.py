class Constants:
    GET_LATEST_CHROME_DRIVER_VERSION_URL = 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json'
    GET_CHROME_DRIVER_DOWNLOAD_PATH_URL = 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json'
    CHROME_DRIVER_DOWNLOAD_PLATFORM = 'win64'
    CHROME_DRIVER_DOWNLOAD_FOLDER = 'chrome_driver'
    CHROME_DRIVER_FILE_NAME = 'chromedriver.exe'

    PORTAL_LINK = 'https://bank.nhsp.uk/ourbank'
    # PORTAL_CREDENTIALS = {'username': 'EPreneursOH', 'password': 'z5ENa8B5yTN9'}
    PORTAL_CREDENTIALS = {'username': 'EPreneursOH', 'password': 'Welcome24'}

    USERNAME_FIELD_ID = 'login'
    PASSWORD_FIElD_ID = 'password'
    LOGIN_BUTTON_ID = 'log'

    NAVIGATION_PANEL_DIV_ID = 'navbar'
    NEXT_28_DAYS_TAB_NAME = '28 Days'

    FILTER_MENU_XPATH = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div[2]/div[1]'
    FILTER_STATUS_ALL_OPTION_XPATH = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div[2]/div[2]/div/div[2]/div[4]/div/select/option[1]'
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
    # RECORDS_NOT_FOUND_TABLE_CLASS_NAME = 'search_notice_table'    #on chrome driver
    RECORDS_NOT_FOUND_TABLE_CLASS_NAME = 'search_notice_td'         #on firefox driver
    
    EXPORT_BUTTON_XPATH = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div[3]/div/div[1]/div[4]/div/div[1]/button'
    EXPORT_EXCEL_OPTION_XPATH = '/html/body/div[2]/div/div[2]/div/div[5]/div/div/div[3]/div/div[1]/div[4]/div/div[1]/ul/li[1]/a'

    LOGOUT_NAVIGATION_DROPDOWN_MENU_ID = 'desktop-toggle'
    LOGOUT_NAVIGATION_MENU_ID = 'navbar_menu'
    LOGOUT_OPTION_NAME = 'Logout'

    # EXPORT_EXCEL_DOWNLOAD_PATH = 'C:\\Users\\Kapil.Patil\\Downloads\\filled\\28_days\\'
    EXPORT_EXCEL_DOWNLOAD_PATH = 'C:\\Users\\saniya.pathan\\Downloads\\filled\\28_days\\'     #on local
    # EXPORT_EXCEL_DOWNLOAD_PATH = '/app/Downloads/filled/28_days/'                             #on docker
    # PROJECT_PATH = 'C:\\IDMedical\\Python Parser\\CodeBase\\NHSP Filled Requirements Scraping And Cancellation\\'
    # PROJECT_PATH = 'D:\\EPI_Saniya\\ID-Medical\\ID-Medical Data\\NHSP Filled Requirements Scraping And Cancellation\\'
    PROJECT_PATH = 'D:\\EPI_Saniya\\Id-Medical_old\\Services\\nhsp_scraping\\Filled_cancellation_28_days_scraping\\'
    
    EXECUTION_LOGS_FOLDER = 'execution_logs'
    EXECUTION_SCREENSHOTS_FOLDER = 'screenshots'
    EXPORTED_EXCELS_FOLDER = 'exported_excels'
    FILLED_REQUIREMENTS_EXCELS_FOLDER = '28_days_requirements_excels\\filled'           #on local
    UNFILLED_REQUIREMENTS_EXCELS_FOLDER = '28_days_requirements_excels\\unfilled'       #on local
    # FILLED_REQUIREMENTS_EXCELS_FOLDER = '28_days_requirements_excels/filled'            #on docker
    # UNFILLED_REQUIREMENTS_EXCELS_FOLDER = '28_days_requirements_excels/unfilled'        #on docker
    REQUIREMENTS_CANCELLATION_EXCELS_FOLDER = 'requirements_cancellation_excels'

    EXECUTION_LOGS_FILENAME = '28_Days_cancellation_logfile_%d_%m_%Y_%H_%M_%S.log'
    EXPORTED_EXCEL_FILENAME = '28_Days_Exported_Excel_%d_%m_%Y_%H_%M_%S.xlsx'
    SHIFT_REQUIREMENTS_EXCEL_FILENAME = '28_Days_Shift_Requirements_Excel_%d_%m_%Y_%H_%M_%S.xlsx'
    REQUIREMENTS_CANCELLATION_EXCEL_FILENAME = '28_Days_Requirements_Cancellation_Excel_%d_%m_%Y_%H_%M_%S.xlsx'

    EXCEL_COLUMN_HEADERS_LIST = ['Booking Reference Number', 'Location', 'Ward', 'Shift Date', 'Start Time', 'End Time', 'Assignment Code', 'Status', 'First Name', 'Last Name', 'Agency Name', 'Secondary Assignment Code', 'Notes']
    REQIREMENTES_EXCEL_SHEET_NAME = 'Shifts'
    
    # UNFILLED_SCRAPING_SUMMARY_FILE_NAME = '28_Days_Unfilled_Requirements_Scraping_Execution_Summary.xlsx'
    UNFILLED_SCRAPING_SUMMARY_FILE_NAME = 'D:\\EPI_Saniya\\Id-Medical_old\\summary_files\\28_Days_Unfilled_Requirements_Scraping_Execution_Summary.xlsx'
    # FILLED_SCRAPING_SUMMARY_FILE_NAME = '28_Days_Filled_Requirements_Scraping_Execution_Summary.xlsx'
    FILLED_SCRAPING_SUMMARY_FILE_NAME = 'D:\\EPI_Saniya\\Id-Medical_old\\summary_files\\28_Days_Filled_Requirements_Scraping_Execution_Summary.xlsx'
    
    SCRAPING_SUMMARY_COLUMN_HEADERS_LIST = ['Execution Date', 'Execution Time', 'Requirements Filename', 'Is Comparision Completed', 'Requirements Cancellation Filename']
    SCRAPING_SUMMARY_EXCEL_SHEET_NAME = 'Scraping Summary'

    CANCELLATION_EXCEL_SHEET_NAME = 'Requirements Cancellation'

    TOTAL_WARDS_FOR_PARSING = 5

    # this limit is only for the locations whose wards count is very less
    TOTAL_WARDS_FOR_SCRAPING_IN_ONE_LOGIN = 20
