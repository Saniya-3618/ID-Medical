class Constants:
    PORTAL_LINK = 'https://bank.nhsp.uk/ourbank'
    # PORTAL_CREDENTIALS = {'username': 'EPreneursOH', 'password': 'z5ENa8B5yTN9'}
    PORTAL_CREDENTIALS = {'username': 'EPreneursOH', 'password': 'Welcome24'}

    USERNAME_FIELD_ID = 'login'
    PASSWORD_FIElD_ID = 'password'
    LOGIN_BUTTON_ID = 'log'

    NAVIGATION_PANEL_DIV_ID = 'navbar'
    NEXT_3_DAYS_TAB_NAME = 'Next 3 days'

    FILTER_MENU_XPATH = '/html/body/div[2]/div/div[2]/div/div[3]/div/div/div[2]/div[1]'
    FILTER_STATUS_ALL_OPTION_XPATH = '/html/body/div[2]/div/div[2]/div/div[3]/div/div/div[2]/div[2]/div/div[2]/div[4]/div/select/option[1]'
    FILTER_AUTHORISATION_ALL_OPTION_XPATH = '/html/body/div[2]/div/div[2]/div/div[3]/div/div/div[2]/div[2]/div/div[2]/div[3]/div/select/option[1]'

    EXPORT_BUTTON_XPATH = '/html/body/div[2]/div/div[2]/div/div[3]/div/div/div[3]/div/div[1]/div[4]/div/div[1]/button'
    EXPORT_EXCEL_OPTION_XPATH = '/html/body/div[2]/div/div[2]/div/div[3]/div/div/div[3]/div/div[1]/div[4]/div/div[1]/ul/li[1]/a'
    
    LOGOUT_NAVIGATION_DROPDOWN_MENU_ID = 'desktop-toggle'
    LOGOUT_NAVIGATION_MENU_ID = 'navbar_menu'
    LOGOUT_OPTION_NAME = 'Logout'

    # EXPORT_EXCEL_DOWNLOAD_PATH = 'C:\\Users\\Kapil.Patil\\Downloads\\filled\\3_days\\'
    # EXPORT_EXCEL_DOWNLOAD_PATH = 'C:\\Users\\saniya.pathan\\Downloads\\Downloads\\filled\\3_days\\'
    EXPORT_EXCEL_DOWNLOAD_PATH = '/app/Downloads/filled/3_days/'    #on docker
    # PROJECT_PATH = 'C:\\IDMedical\\Python Parser\\CodeBase\\NHSP Filled Requirements Scraping And Cancellation\\'
    PROJECT_PATH = 'D:\\EPI_Saniya\\Id-Medical_old\\Services\\nhsp_scraping\\Unfilled_3_days_scraping\\'
    
    EXECUTION_LOGS_FOLDER = 'execution_logs'
    EXECUTION_SCREENSHOTS_FOLDER = 'screenshots'
    EXPORTED_EXCELS_FOLDER = 'exported_excels'
    # UNFILLED_REQUIREMENTS_EXCELS_FOLDER = '3_days_requirements_excels\\unfilled'   #on local
    # FILLED_REQUIREMENTS_EXCELS_FOLDER = '3_days_requirements_excels\\filled'          #on local
    UNFILLED_REQUIREMENTS_EXCELS_FOLDER = '3_days_requirements_excels/unfilled'  #on docker
    FILLED_REQUIREMENTS_EXCELS_FOLDER = '3_days_requirements_excels/filled'        #on docker
    REQUIREMENTS_CANCELLATION_EXCELS_FOLDER = 'requirements_cancellation_excels'      
    
    EXECUTION_LOGS_FILENAME = '3_Days_cancellation_logfile_%d_%m_%Y_%H_%M_%S.log'
    EXPORTED_EXCEL_FILENAME = '3_Days_Exported_Excel_%d_%m_%Y_%H_%M_%S.xlsx'
    SHIFT_REQUIREMENTS_EXCEL_FILENAME = '3_Days_Shift_Requirements_Excel_%d_%m_%Y_%H_%M_%S.xlsx'
    REQUIREMENTS_CANCELLATION_EXCEL_FILENAME = '3_Days_Requirements_Cancellation_Excel_%d_%m_%Y_%H_%M_%S.xlsx'

    EXCEL_COLUMN_HEADERS_LIST = ['Booking Reference Number', 'Location', 'Ward', 'Shift Date', 'Start Time', 'End Time', 'Assignment Code', 'Status', 'First Name', 'Last Name', 'Agency Name', 'Secondary Assignment Code', 'Notes','Gender', 'Booking Reason']
    REQIREMENTES_EXCEL_SHEET_NAME = 'Shifts'

    UNFILLED_SCRAPING_SUMMARY_FILE_NAME = '3_Days_Unfilled_Requirements_Scraping_Execution_Summary.xlsx'
    FILLED_SCRAPING_SUMMARY_FILE_NAME = '3_Days_Filled_Requirements_Scraping_Execution_Summary.xlsx'

    SCRAPING_SUMMARY_COLUMN_HEADERS_LIST = ['Execution Date', 'Execution Time', 'Requirements Filename', 'Is Comparision Completed', 'Requirements Cancellation Filename']
    SCRAPING_SUMMARY_EXCEL_SHEET_NAME = 'Scraping Summary'

    CANCELLATION_EXCEL_SHEET_NAME = 'Requirements Cancellation'
    
     #/app/3_days_requirements_excels/filled/
    DELETE_FILES_DIRECTORY_LIST = ['/app/exported_excels/', '/app/execution_logs/', '/app/screenshots/']
    DAYS_THRESHOLD = 30
    ARCHIVE_TASK_LOG_FILE = 'Delete_Files_logfile_%d_%m_%Y_%H_%M_%S.log'
    
    
    
    
    
    
    
    
    