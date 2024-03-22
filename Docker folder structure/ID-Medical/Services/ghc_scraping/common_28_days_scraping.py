class Constants:
    
    PORTAL_LINK = 'https://tgthrbank.allocate-cloud.com/BankStaff/(S(4e21wzfplrhszf3ppgmv5lb5))/UserLogin.aspx'
    PORTAL_CREDENTIALS = {'username': 'IDmedical Bookings', 'password': 'Orange12345'}
    
    LOGIN_PAGE_FRAME_ID = 'aspnetForm'
    USERNAME_ELEMENT_ID = 'ctl00_content_login_UserName'
    PASSWORD_ELEMENT_ID = 'ctl00_content_login_Password'
    LOGIN_BUTTON_ELEMENT_ID = 'ctl00_content_login_LoginButton'
    
    FILTER_FIELD_ELEMENT_ID = 'ctl00_content_BookingStatus1_collapsibleImage'
    NEXT_28_DAYS_OPTION_ELEMENT_ID = 'ctl00_content_BookingStatus1_mListDateOptions'
    SUBMIT_FILTER_BUTTON_ID = 'ctl00_content_BookingStatus1_cmdSubmitPrint'
    EXPORT_EXCEL_ELEMENT_ID = 'ctl00_content_BookingStatus1_cmdXLS'
    
    FILLED_BOOKING_OPTION_XPATH = '/html/body/form/table/tbody/tr/td[1]/div/a[3]/table/tbody/tr/td[2]'
    
    LOGOUT_BUTTON_XPATH = '/html/body/form/div[3]/table/tbody/tr/td[3]/div/table/tbody/tr[2]/td[4]/a'
    DATA_LOADER_XPATH = '/html/body/form/table/tbody/tr/td[2]/div[2]/div/span/span'
                        # '/html/body/form/table/tbody/tr/td[2]/div[2]/div/span/span'
    #REQUIREMENT_EXCEL_FOLDER = 'D:\\EPI_Saniya\\Id-Medical_old\\GHC\\unfilled_requirements_excels\\'
    #EXPORT_FILLED_REQUIREMENT_EXCEL_DOWNLOAD_PATH = 'D:\\EPI_Saniya\\Id-Medical_old\\GHC\\filled_requirements_excels\\'
    #EXECUTION_SCREENSHOTS_FOLDER = 'D:\\EPI_Saniya\\Id-Medical_old\\GHC\\screenshots\\'
    #EXPORT_REQUIREMENT_EXCEL_DOWNLOAD_PATH = 'D:\\EPI_Saniya\\Id-Medical_old\\GHC\\download\\'
    #EXECUTION_LOGS_FOLDER = 'D:\\EPI_Saniya\\Id-Medical_old\\GHC\\execution_logs\\'
    
    REQUIREMENT_EXCEL_FOLDER = '/app/unfilled_requirements_excels/'
    EXPORT_FILLED_REQUIREMENT_EXCEL_DOWNLOAD_PATH = '/app/filled_requirements_excels/'
    EXECUTION_SCREENSHOTS_FOLDER = '/app/screenshots/'
    EXPORT_REQUIREMENT_EXCEL_DOWNLOAD_PATH = '/app/download/'
    EXECUTION_LOGS_FOLDER = '/app/execution_logs/'
    
    
    EXECUTION_LOGS_FILENAME = '28_Days_logfile_%d_%m_%Y_%H_%M_%S.log'
    EXPORTED_REQUIREMENT_EXCEL_FILENAME = '28_Days_Unfilled_Requireents_Excel_%d_%m_%Y_%H_%M_%S.xlsx'
    EXPORTED_FILLED_EXCEL_FILENAME = '28_Days_Filled_Requireents_Excel_%d_%m_%Y_%H_%M_%S.xlsx'
    
    DELETE_FILES_DIRECTORY_LIST = ['/app/download/', '/app/execution_logs/', '/app/screenshots/']
    DAYS_THRESHOLD = 7
    ARCHIVE_TASK_LOG_FILE = 'Delete_Files_logfile_%d_%m_%Y_%H_%M_%S.log'