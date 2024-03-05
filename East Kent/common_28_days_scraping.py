class Constants:
    
    PORTAL_LINK = 'https://bookings.nhsprofessionals.nhs.uk/NewLoginFrame.asp'
    # PORTAL_CREDENTIALS = {'username': 'Anthony.grubb', 'password': 'Arsenal25071985'}
    PORTAL_CREDENTIALS = {'username': 'AUJonathanIDM', 'password': 'Newpassword@1'}
    
    USERNAME_FIELD_ELEMENT_NAME = 'StaffNo'
    PASSWORD_FIELD_ELEMENT_NAME = 'PIN'
    LOGIN_BUTTON_ELEMENT_NAME = 'Submit'
    LOGOUT_BUTTON_ELEMENT_ID = 'LogoutImage'
    
    VIEW_REQUEST_OPTION_ELEMENT_ID = 'linkViewRequests'
    # SELECT_TRUST_NAME_ELEMENT_XPATH = '//*[@id="DropDownList_Trust"]/option[10]'
    SELECT_TRUST_NAME_ELEMENT_NAME = 'DropDownList_Trust'
    SUBMIT_BUTTON_ELEMENT_NAME = 'btnSumbit'
    RECORD_NOT_FOUND_MSG_ELEMENT_ID = 'lblNoRecord_msg'
    
    TRUST_NAME = 'East Kent Hospitals Uni NHS Foundation Trust'
    
    TABLE_ELEMENT_ID = 'AgencyRequestsBookings_dynamicPanel'
    BACK_BUTTON_ELEMENT_ID = 'Button_BackToSubmit'
    
    INTERVAL_ITERATION_RANGE = 4
    START_DATE_ELEMENT_NAME ='panel_StartDate'
    END_DATE_ELEMENT_NAME = 'panel_EndDate'
    
    PROJECT_PATH = 'D:\\EPI_Saniya\\Id-Medical_old\\East Kent\\'
    
    REQUIREMENT_EXCEL_FOLDER = 'requirement_files'
    UNFILLED_REQUIREMENT_EXCEL_FOLDER = '28_days_requirements'
    REQUIREMENTS_CANCELLATION_EXCELS_FOLDER = 'requirements_cancellation_excels'      
    CANCELLATION_EXCEL_SHEET_NAME = 'Requirements Cancellation'
    
    
    FILE_NAME_OF_SCRAPED_DATA = '28_Days_Unfilled_Requirements_Excel_%d_%m_%Y_%H_%M_%S.xlsx'
    EXECUTION_LOGS_FILENAME = '28_Days_Unfilled_logfile_%d_%m_%Y_%H_%M_%S.log'
    EXECUTION_LOGS_FOLDER  = 'execution_logs'
    # EXCEL_COLUMN_HEADERS_LIST = ['Bank Req Num', 'Date', 'Start Time', 'End Time', 'Location', 'Ward','Assignment',  'Training', 'Training.1', 'Sex', 'Notes', 'Secondary Assignment' ]
    EXCEL_COLUMN_HEADERS_LIST = ['Bank Req Num', 'Date', 'Start Time', 'End Time', 'Location', 'Ward', 'Assignment', 'Sex', 'Notes', 'Secondary Assignment']
    SCRAPING_SUMMARY_COLUMN_HEADERS_LIST = ['Execution Date', 'Execution Time', 'Requirements Filename', 'Is Comparision Completed', 'Requirements Cancellation Filename']

    UNFILLED_SCRAPING_SUMMARY_FILE_NAME = '28_Days_Unfilled_Requirements_Scraping_Execution_Summary.xlsx'
    SCRAPING_SUMMARY_EXCEL_SHEET_NAME = 'Scraping Summary'
    REQIREMENTES_EXCEL_SHEET_NAME = 'Sheet1'
    
    REQUIREMENTS_CANCELLATION_EXCEL_FILENAME = '28_Days_Requirements_Cancellation_Excel_%d_%m_%Y_%H_%M_%S.xlsx'
    
    EXECUTION_SCREENSHOTS_FOLDER = 'screenshots'