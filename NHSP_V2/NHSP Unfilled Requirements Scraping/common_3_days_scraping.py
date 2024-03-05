import time


class Constants:
    PORTAL_LINK = 'https://bank.nhsp.uk/ourbank'
    # PORTAL_CREDENTIALS = {'username': 'EPreneursOH', 'password': 'z5ENa8B5yTN9'}
    PORTAL_CREDENTIALS = {'username': 'EPreneursOH', 'password': 'Welcome24'}

    USERNAME_FIELD_ID = 'login'
    PASSWORD_FIElD_ID = 'password'
    LOGIN_BUTTON_ID = 'log'

    NAVIGATION_PANEL_DIV_ID = 'navbar'
    NEXT_3_DAYS_TAB_NAME = 'Next 3 days'
    NEXT_3_DAYS_TAB_XPATH = '//*[@id="navbar"]/ul/li[3]/a'

    FILTER_MENU_XPATH = '/html/body/div[2]/div/div[2]/div/div[3]/div/div/div[2]/div[1]'
    FILTER_STATUS_UNFILLED_OPTION_XPATH = '/html/body/div[2]/div/div[2]/div/div[3]/div/div/div[2]/div[2]/div/div[2]/div[4]/div/select/option[5]'
    FILTER_AUTHORISATION_ALL_OPTION_XPATH = '/html/body/div[2]/div/div[2]/div/div[3]/div/div/div[2]/div[2]/div/div[2]/div[3]/div/select/option[1]'

    EXPORT_BUTTON_XPATH = '/html/body/div[2]/div/div[2]/div/div[3]/div/div/div[3]/div/div[1]/div[4]/div/div[1]/button'
    EXPORT_EXCEL_OPTION_XPATH = '/html/body/div[2]/div/div[2]/div/div[3]/div/div/div[3]/div/div[1]/div[4]/div/div[1]/ul/li[1]/a'
    
    SHIFT_REQUIREMENTS_DIV_ID = 'reactcontent3'

    LOGOUT_NAVIGATION_DROPDOWN_MENU_ID = 'desktop-toggle'
    LOGOUT_NAVIGATION_MENU_ID = 'navbar_menu'
    LOGOUT_OPTION_NAME = 'Logout'

    # EXPORT_EXCEL_DOWNLOAD_PATH = 'C:\\Users\\Kapil.Patil\\Downloads\\unfilled\\3_days\\'
    # PROJECT_PATH = 'C:\\IDMedical\\Python Parser\\CodeBase\\NHSP Unfilled Requirements Scraping\\'
    EXPORT_EXCEL_DOWNLOAD_PATH = 'C:\\Users\\saniya.pathan\\Downloads\\unfilled\\3_days\\'
    PROJECT_PATH = 'D:\\EPI_Saniya\\Id-Medical_old\\NHSP_V2\\NHSP Unfilled Requirements Scraping\\'
    
    EXPORTED_EXCELS_FOLDER = 'exported_excels'
    SHIFT_REQUIREMENTS_EXCELS_FOLDER = 'shift_requirements_excels'
    EXECUTION_LOGS_FOLDER = 'execution_logs'
    EXECUTION_SCREENSHOTS_FOLDER = 'screenshots'

    EXPORTED_EXCEL_FILENAME = '3_Days_Exported_Excel_%d_%m_%Y_%H_%M_%S.xlsx'
    SHIFT_REQUIREMENTS_EXCEL_FILENAME = '3_Days_Shift_Requirements_Excel_%d_%m_%Y_%H_%M_%S.xlsx'
    EXECUTION_LOGS_FILENAME = '3_Days_logfile_%d_%m_%Y_%H_%M_%S.log'
    
    # EXCEL_COLUMN_HEADERS_LIST = ['Booking Reference Number', 'Location', 'Ward', 'Shift Date', 'Start Time', 'End Time', 'Assignment Code', 'Status', 'Secondary Assignment Code', 'Notes']
    EXCEL_COLUMN_HEADERS_LIST = ['Booking Reference Number', 'Location', 'Ward', 'Shift Date', 'Start Time', 'End Time', 'Assignment Code', 'Status', 'Notes', 'Gender']
    EXCEL_EXTRA_COLUMN_HEADER = 'Worker'
    EXCEL_SHEET_NAME = 'Shifts'

    # REQUIREMENTS_FOR_COMPARE_EXCEL_PATH = 'C:\\IDMedical\\Python Parser\\CodeBase\\NHSP Filled Requirements Scraping And Cancellation\\3_days_requirements_excels\\unfilled\\'
    # REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_FILE_PATH = 'C:\\IDMedical\\Python Parser\\CodeBase\\NHSP Filled Requirements Scraping And Cancellation\\3_Days_Unfilled_Requirements_Scraping_Execution_Summary.xlsx'
    REQUIREMENTS_FOR_COMPARE_EXCEL_PATH = 'D:\\EPI_Saniya\\Id-Medical_old\\NHSP_V2\\NHSP Filled Requirements Scraping And Cancellation\\3_days_requirements_excels\\unfilled\\'
    REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_FILE_PATH = 'D:\\EPI_Saniya\\Id-Medical_old\\NHSP_V2\\NHSP Filled Requirements Scraping And Cancellation\\3_Days_Unfilled_Requirements_Scraping_Execution_Summary.xlsx'
    
    REQUIREMENTS_SCRAPING_EXECUTION_SUMMARY_EXCEL_SHEET_NAME = 'Scraping Summary'
    SCRAPING_SUMMARY_COLUMN_HEADERS_LIST = ['Execution Date', 'Execution Time', 'Requirements Filename', 'Is Comparision Completed', 'Requirements Cancellation Filename']

    SCROLL_PAUSE_TIME = 6


class Tasks:
    def infinite_scroll(driver):
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
