from extract_msg  import Message
import os
import re
from bs4 import BeautifulSoup
import json
from app.config.app_config import * 
from datetime import datetime


def ghc_open_shift_scraping():
    # Parse the .msg file
    email = Message(GHC_OPEN_REQUIREMENTS_PATH)
    html_body = email.htmlBody

    # with open('content1.html', "w", encoding="utf-8") as file:
    #     # file = open('content.txt', 'w')
    #     # file.write(html_body)
    #     file.write(html_body.decode("utf-8"))
    #     file.close()
    # Extract various attributes from the .msg file
    print("Subject:", email.subject)
    subject = email.subject
    print("Sender:", email.sender)
    sender = email.sender
    sender_email = sender.split('\t')[1]
    from_name = sender.split('\t')[0]
    print("Recipients:", email.to)
    to = email.to

    print("CC:", email.cc)
    print("Date:", email.date)
    EmailReceivedDate = email.date
    # print("Body:", email.body)

    email_body = os.linesep.join(
                        [
                            line for line in email.body.splitlines()
                            if line
                        ]
                    )
    print("Text Content without XML Tags:\n", email_body)

    # Regular expressions to extract information
    request_id_pattern = r"Request Id:\s+(\d+)"
    date_pattern = r"Date:\s+(\d{2}-[a-zA-Z]{3}-\d{2})"
    trust_code_pattern = r"Trust Code:\s+([\d\w\s]+)"
    ward_pattern = r"Ward:\s+([\d\w\s]+)"
    start_pattern = r"Start:\s+(\d{2}:\d{2})"
    end_pattern = r"End:\s+(\d{2}:\d{2})"
    grade_pattern = r"Grade:\s+([\w\s]+)"

    # Extract information using regular expressions
    request_id = re.search(request_id_pattern, email_body).group(1)
    date = re.search(date_pattern, email_body).group(1)
    trust_code = re.search(trust_code_pattern, email_body).group(1)
    ward = re.search(ward_pattern, email_body).group(1)
    start_time = re.search(start_pattern, email_body).group(1)
    end_time = re.search(end_pattern, email_body).group(1)
    grade = re.search(grade_pattern, email_body).group(1)

    print('@'*60)
    separator_pattern = r"_+"
    # Find occurrences of '________________________________' using regular expression
    separators = re.findall(separator_pattern, email_body)

    # Print the found separators
    print("Occurrences of '____':", len(separators))
    # for count in range(len(separators)):
    #     # Print extracted information
    #     print("Request Id:", request_id)
    #     print("Date:", date)
    #     print("Trust Code:", trust_code)
    #     print("Ward:", ward)
    #     print("Start Time:", start_time)
    #     print("End Time:", end_time)
    #     print("Grade:", grade)
    #     print('*'*60)
        
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_body, 'html.parser')

    # Find all <tr> tags in the HTML content
    html = soup.find_all('html')[0]
    body = html.find_all('body')[0].find_all('html')
    # print('body = ',len(body))
    body_list = []
    table_data = []
    
    for count in range(len(body)):
        # print(html)
        body_ = html.find_all('body')[0].find_all('html')[count].find_all('body')
        # print('body_ = ',body_)
        body_list.append(body_)
        
    # for row in body_list:
        # print('row ====      ',row)
        # tr = row[0].find_all('tr')
        tr = body_[0].find('table').find('tr').find_all('tr')
        # print('tr=',len(tr), tr)
        req_id = None
        shift_date = None
        trust_code= None
        ward= None
        start_time= None
        end_time= None
        grade= None
        skills= None
        gender= None
        status= None
        agency_staff= None
        
        for r in tr:
            # print("Request Id Row:", r)
            # Find all <td> tags in the row
            cells = r.find_all('td')
            
            # Extract text from the first and second <td> tags
            if len(cells) == 2:
                key = cells[0].get_text().strip()
                value = cells[1].get_text().strip()
                if 'Request Id' in key:
                    req_id = value
                elif 'Date' in key:
                    shift_date = value
                elif 'Trust Code' in key:
                    trust_code = value
                elif 'Ward' in key:
                    ward = value
                elif 'Start' in key:
                    start_time = value
                elif 'End' in key:
                    end_time = value
                elif 'Grade' in key:
                    grade = value
                elif 'Skills' in key:
                    skills = value
                elif 'Gender' in key:
                    gender = value
                elif 'Status' in key:
                    status = value
                elif 'Agency Staff' in key:
                    agency_staff = value
                    
        row_data = {
            'Request Id':req_id,
            'Date':shift_date,
            'Trust Code':trust_code,
            'Ward':ward,
            'Start':start_time,
            'End':end_time,
            'Grade':grade,
            'Skills':skills,
            'Gender':gender,
            'Status':status,
            'Agency Staff':agency_staff,
            'EmailId': sender_email,
            'EmailReceivedDate':str(EmailReceivedDate),
            'From':from_name,
            'Subject': subject,
            'To': to,
            "Cost Centre Desc":"",                   # field not found
            "Cost Centre":"",                                       # field not found
            "Grade Type":""	                                              # field not found
        }   
    
        # Append the row_data dictionary to the table_data list
        table_data.append(row_data)

    # # Convert table_data list to JSON format
    # json_data = json.dumps(table_data, indent=4)
    # with open('data.json', "w") as file:
    #     # file = open('content.txt', 'w')
    #     # file.write(html_body)
    #     file.write(json_data)
    #     file.close()
    # # print(json_data)    
    
    # return json_data
    return table_data

   
def ghc_close_shift_scraping():
    email = Message(GHC_CLOSED_REQUIREMENTS_PATH)
    html_body = email.htmlBody
    # with open('ghc_closed.html', "w", encoding="utf-8") as file:
    #     # file = open('content.txt', 'w')
    #     # file.write(html_body)
    #     file.write(html_body.decode("utf-8"))
    #     file.close()
    
    print("Subject:", email.subject)
    subject = email.subject
    sender = email.sender
    sender_email = sender.split('\t')[1]
    from_name = sender.split('\t')[0]
    print("sender_email:", sender_email)
    print("from_name:",from_name)
    print("Recipients:", email.to)
    to = email.to

    print("CC:", email.cc)
    print("Date:", email.date)
    EmailReceivedDate = email.date
    # print("Body:", email.body)

    email_body = os.linesep.join(
                        [
                            line for line in email.body.splitlines()
                            if line
                        ]
                    )
    print("Text Content without XML Tags:\n", email_body)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_body, 'html.parser')

    # Find all <tr> tags in the HTML content
    html = soup.find_all('html')
    # body = html.find_all('body')[0].find_all('html')
    # print('body = ',len(body))
    body_list = []
    table_data = []
    
    for count in html:
        # print(count)
        body_ = count.find_all('body')#[0].find_all('html')[count].find_all('body')
        # print('body_ = ',body_)
        body_list.append(body_)
        
    # for row in body_list:
        # print('row ====      ',row)
        if body_[0].find('table'):
            # print('table found------------------')
    #     # tr = row[0].find_all('tr')
            tr = body_[0].find('table').find_all('tr')
            # print('tr=',len(tr), tr)
            req_id = None
            shift_date = None
            trust_code= None
            ward= None
            start_time= None
            end_time= None
            grade= None
            skills= None
            gender= None
            status= None
            agency_staff= None
            
            for r in tr:
                # print("Request Id Row:", r)
                # Find all <td> tags in the row
                cells = r.find_all('td')
                
                # Extract text from the first and second <td> tags              ###check if index can be dynamic
                if len(cells) >= 2:
                    key = cells[0].get_text().strip()
                    value = cells[1].get_text().strip()
                    
                    if 'Request Id'.lower() in key.lower():
                        req_id = value
                    elif 'Date' in key:
                        shift_date = value
                    elif 'Trust Code' in key:
                        trust_code = value
                    elif 'Ward' in key:
                        ward = value
                    elif 'Start' in key:
                        start_time = value
                    elif 'End' in key:
                        end_time = value
                    elif 'Grade' in key:
                        grade = value
                    elif 'Skills' in key:
                        skills = value
                    elif 'Gender' in key:
                        gender = value
                    elif 'Status' in key:
                        status = value
                    elif 'Agency Staff' in key:
                        agency_staff = value
                        
            row_data = {
                'Request Id':req_id,
                'Date':shift_date,
                'Trust Code':trust_code,
                'Ward':ward,
                'Start':start_time,
                'End':end_time,
                'Grade':grade,
                'Skills':skills,
                'Gender':gender,
                'Status':status,
                'Agency Staff':agency_staff,
                'EmailId': sender_email,
                'EmailReceivedDate':str(EmailReceivedDate),
                'From':from_name,
                'Subject': subject,
                'To': to,
                "Cost Centre Desc":"Wotton Lawn - Montpellier",                   # field not found
                "Cost Centre":"327 D11612",                                       # field not found
                "Grade Type":"HCA"	                                              # field not found
            }   
        
            # Append the row_data dictionary to the table_data list
            table_data.append(row_data)

    # # Convert table_data list to JSON format
    # json_data = json.dumps(table_data, indent=4)
    # with open('ghc_closed_data.json', "w") as file:
    #     # file = open('content.txt', 'w')
    #     # file.write(html_body)
    #     file.write(json_data)
    #     file.close()
    # # print(json_data)    
   
    return table_data

def ghc_shifts_json():
    open_res = ghc_open_shift_scraping()
    closed_res = ghc_close_shift_scraping()

    final_json = {'Open Shifts': open_res,
                'Closed Shifts': closed_res}

    final_json1 = json.dumps(final_json, indent=4)
    
    fileName = 'GHC_Shift_Details_JSON_%d_%m_%Y_%H_%M_%S.json'
    fileName = datetime.now().strftime(fileName)
    
    with open(fileName, "w") as file:
        # json.dump(final_json, file, indent=None)
        file.write(final_json1)
        file.close()
    
    return final_json1