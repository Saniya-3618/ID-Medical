# from exchangelib import Credentials, Account, Configuration, DELEGATE, Message, HTMLBody
# import requests
# from bs4 import BeautifulSoup
# import os
# from datetime import datetime
# # String username = "groupid\\ExtrapreneursOH";
# # String password =  "mtf!puq5MYA9cky!maw";
# # String targetMailbox = "OHBookings@ID-medical.com";
# # // String exchangeUrl = "https://172.16.101.79/owa";
# # // String exchangeUrl="autodiscover.id-medical.com";
# # String exchangeUrl="https://mail2016.id-medical.com/owa";

# # resp = requests.get('https://mail2016.id-medical.com/owa')
# # print('resp= ',resp)
# start_time = datetime.now()
# print('start_time = ',start_time)
# # Credentials for authentication
# credentials = Credentials('groupid\\ExtrapreneursOH', 'mtf!puq5MYA9cky!maw')

# # EWS URL for your Exchange server
# # ews_url = 'https://172.16.101.79/owa'  # Replace with your EWS URL
# ews_url = 'mail2016.id-medical.com'
# # Create a configuration object
# config = Configuration(server=ews_url, credentials=credentials)

# # Create an Account object
# account = Account(primary_smtp_address='OHBookings@ID-medical.com', config=config, autodiscover=False, access_type=DELEGATE)
# print('account = ',account)
# end_time = datetime.now()
# print('end_time = ',end_time)

# ## TO READ UNREAD EMAILS FROM INBOX
# inbox = account.inbox
# # Find unread emails and mark them as read
# unread_emails = inbox.filter(is_read=False) ############check if read by sub
# # print('total unred messages= ', len(unread_emails))
# count = 1
# for item in unread_emails.order_by('-datetime_received')[:10]:
#     # email.is_read = True
#     # email.save()
#     if isinstance(item, Message):
#         subject = 'Booking requested'
#         if item.subject.lower() == subject.lower() :
#             if item.body:
#                 # print(item.body)
#                 with open('content.html', "w", encoding="utf-8") as file:
#                     # file = open('content.txt', 'w')
#                     file.write(item.body)
#                     file.close()
                    
#                 if isinstance(item.body, HTMLBody):   
#                     soup = BeautifulSoup(item.body, 'html.parser')
#                     text_content = soup.get_text()
#                 else:
#                     text_content = item.body
#                 # print("Subject:", item.subject)
#                 # print("Sender:", item.sender)
#                 # print("Received Time:", item.datetime_received)
#                 without_empty_lines = os.linesep.join(
#                     [
#                         line for line in text_content.splitlines()
#                         if line
#                     ]
#                 )
#                 # print("Text Content without XML Tags:", text_content)
#                 # print("=" * 50, count)
#                 count+=1
#             # item.is_read = True
#             # item.save()
   
# end_time2 = datetime.now()
# print('end_time2 = ',end_time2)   
   
# ************************************************************************************************************************************************

from extract_msg  import Message
import os
import re
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Path to the .msg file
FHFT_open_path = "D:/EPI_Saniya/Id-Medical_old/EWS_Outlook/sample mails/Shifts for fulfilment.msg"
FHFT_close_path = "D:/EPI_Saniya/Id-Medical_old/EWS_Outlook/sample mails/Shift Cancellation.msg"
GHC_open_path = "D:/EPI_Saniya/Id-Medical_old/EWS_Outlook/sample mails/1-Unfilled Shifts Transferred To Your Agency.msg"
GHC_close_path = "D:/EPI_Saniya/Id-Medical_old/EWS_Outlook/sample mails/Agency request deleted.msg"
IOW_open_path = "D:/EPI_Saniya/Id-Medical_old/EWS_Outlook/sample mails/Unfilled shift transferred to Agency.msg"
IOW_close_path = "D:/EPI_Saniya/Id-Medical_old/EWS_Outlook/sample mails/Agency shift requested deleted.msg"

def ghc_open_shift_scraping(GHC_open_path):
    # Parse the .msg file
    email = Message(GHC_open_path)
    html_body = email.htmlBody

    # with open('ghc_open.html', "w", encoding="utf-8") as file:
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
        print('body_ = ',body_)
        body_list.append(body_)
        
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
        cost_centre_desc = None                  # field not found
        cost_centre = None                                       # field not found
        grade_type = None                       # field not found
        
        for r in tr:
            # print("Request Id Row:", r)
            # Find all <td> tags in the row
            cells = r.find_all('td')
            
            # # Extract text from each <td> tag and store it in the row_data dictionary
            # for index, cell in enumerate(cells):
            #     row_data[f"column_{index+1}"] = cell.get_text().strip()
            
            # Extract text from the first and second <td> tags
            if len(cells) == 2:
                key = cells[0].get_text().strip()
                value = cells[1].get_text().strip()
                if 'Request Id' == key.lower().replace(':',''):
                    req_id = value
                elif 'Date' == key.lower().replace(':',''):
                    shift_date = value
                elif 'Trust Code' == key.lower().replace(':',''):
                    trust_code = value
                elif 'Ward' == key.lower().replace(':',''):
                    ward = value
                elif 'Start' == key.lower().replace(':',''):
                    start_time = value
                elif 'End' == key.lower().replace(':',''):
                    end_time = value
                elif 'Grade' == key.lower().replace(':',''):
                    grade = value
                elif 'Skills' == key.lower().replace(':',''):
                    skills = value
                elif 'Gender' == key.lower().replace(':',''):
                    gender = value
                elif 'Status' == key.lower().replace(':',''):
                    status = value
                elif 'Agency Staff' == key.lower().replace(':',''):
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
            "Cost Centre Desc":cost_centre_desc,                   # field not found
            "Cost Centre":cost_centre,                                       # field not found
            "Grade Type":grade_type	                                              # field not found
        }   
    
        # Append the row_data dictionary to the table_data list
        table_data.append(row_data)

    # Convert table_data list to JSON format
    json_data = json.dumps(table_data, indent=4)
    with open('ghc_open.json', "w") as file:
        # file = open('content.txt', 'w')
        # file.write(html_body)
        file.write(json_data)
        file.close()
    # print(json_data)    
    
    # return json_data
    return table_data

   
def ghc_close_shift_scraping(GHC_close_path):
    email = Message(GHC_close_path)
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
        print(count)
        body_ = count.find_all('body')#[0].find_all('html')[count].find_all('body')
        print('body_ = ',body_)
        # body_list.append(body_)
        
    # for row in body_list:
        # print('row ====      ',row)
        if body_[0].find('table'):
            print('table found------------------')
    #     # tr = row[0].find_all('tr')
            tr = body_[0].find('table').find_all('tr')
            print('tr=',len(tr), tr)
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
            cost_centre_desc = None                  # field not found
            cost_centre = None                                       # field not found
            grade_type = None                       # field not found
            
            for r in tr:
                # print("Request Id Row:", r)
                # Find all <td> tags in the row
                cells = r.find_all('td')
                
                # Extract text from the first and second <td> tags              ###check if index can be dynamic
                if len(cells) >= 2:
                    key = cells[0].get_text().strip()
                    value = cells[1].get_text().strip()
                    
                    if 'Request Id'.lower() == key.lower().replace(':',''):
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
                "Cost Centre Desc":cost_centre_desc,                   # field not found
                "Cost Centre":cost_centre,                                       # field not found
                "Grade Type":grade_type                                          # field not found
            }   
        
            # Append the row_data dictionary to the table_data list
            table_data.append(row_data)

    # Convert table_data list to JSON format
    json_data = json.dumps(table_data, indent=4)
    with open('ghc_closed_data.json', "w") as file:
        # file = open('content.txt', 'w')
        # file.write(html_body)
        file.write(json_data)
        file.close()
    # print(json_data)    
   
    return table_data
   
# ghc_open_res = ghc_open_shift_scraping(GHC_open_path)
# ghc_closed_res = ghc_close_shift_scraping(GHC_close_path)

# final_json = {'Open Shifts': ghc_open_res,
#               'Closed Shifts': ghc_closed_res}

# final_json1 = json.dumps(final_json, indent=4)

# fileName = 'GHC_Shift_Details_JSON_%d_%m_%Y_%H_%M_%S.json'
# fileName = datetime.now().strftime(fileName)

# with open(fileName, "w") as file:
#         # file = open('content.txt', 'w')
#         # file.write(html_body)
#         # json.dump(final_json, file, indent=None)
#         file.write(final_json1)
#         file.close()
        

def iow_open_shift_scraping():
    email = Message(IOW_open_path)
    html_body = email.htmlBody
    # with open('iow_open.html', "w", encoding="utf-8") as file:
    #     # file = open('content.txt', 'w')
    #     # file.write(html_body)
    #     file.write(html_body.decode("utf-8"))
    #     file.close()
    print("Subject:", email.subject)
    subject = email.subject
    sender = email.sender
    print("sender:", sender)
    sender_email = sender.split('<')[1]
    from_name = sender.split('\t')[0]
    print("sender_email:", sender_email)
    print("from_name:",from_name)
    print("Recipients:", email.to)
    to = email.to

    print("CC:", email.cc)
    print("Date:", email.date)
    EmailReceivedDate = email.date
    
    soup = BeautifulSoup(html_body, 'html.parser')
    html = soup.find_all('html')[0].find_all('body')[0].find_all('table')
    # body = html.find_all('body')[0].find_all('html')
    # print('body = ',len(body))
    body_list = []
    table_data = []
    print('html=    ',html)
    
    for table in html:
            print('body=    ',table)
        # body_ = body.find_all('table')#[0].find_all('html')[count].find_all('body')
        # # print('body_ = ',body_)
        # body_list.append(body_)
    
            tr = table.find_all('tr')
            print('tr=',len(tr), tr)
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
            secondary_grade = None
            speciality = None
            priority = None
            cost_centre_desc = None
            fallbackSpeciality = None
            cost_centre = None
            secondary_grade_type = None
            grade_type = None
            
            for r in tr:
                # print("Request Id Row:", r)
                # Find all <td> tags in the row
                cells = r.find_all('td')
                
                # Extract text from the first and second <td> tags              ###check if index can be dynamic
                if len(cells) >= 2:
                    key = cells[0].get_text().strip()
                    value = cells[1].get_text().strip()
                    
                    if 'Request Id'.lower() == key.lower().replace(':',''):
                        req_id = value
                    elif 'Date'.lower() == key.lower().replace(':',''):
                        shift_date = value
                    elif 'Trust Code'.lower() == key.lower().replace(':',''):
                        trust_code = value
                    elif 'Ward'.lower() == key.lower().replace(':',''):
                        ward = value                          
                    elif 'Cost Centre'.lower() == key.lower().replace(':',''):
                        cost_centre = value   
                    elif 'Cost Centre Desc'.lower() == key.lower().replace(':',''):
                        cost_centre_desc = value
                    elif 'Start'.lower() == key.lower().replace(':',''):
                        start_time = value
                    elif 'End'.lower() == key.lower().replace(':',''):
                        end_time = value                       
                    elif 'Grade Type'.lower() == key.lower().replace(':',''):
                        grade_type = value                        
                    elif 'Grade'.lower() == key.lower().replace(':',''):
                        grade = value                        
                    elif 'Secondary Grade Type'.lower() == key.lower().replace(':',''):
                        secondary_grade_type = value                         
                    elif 'Secondary Grade'.lower() == key.lower().replace(':',''):
                        secondary_grade = value                        
                    elif 'Skills'.lower() == key.lower().replace(':',''):
                        skills = value
                    elif 'Gender'.lower() == key.lower().replace(':',''):
                        gender = value                        
                    elif 'Priority'.lower() == key.lower().replace(':',''):
                        priority = value                          
                    elif 'Status'.lower() == key.lower().replace(':',''):
                        status = value
                    elif 'Agency Staff'.lower() == key.lower().replace(':',''):
                        agency_staff = value                        
                    elif 'Speciality'.lower() == key.lower().replace(':',''):
                        speciality = value                         
                    elif 'FallbackSpeciality'.lower() == key.lower().replace(':',''):
                        fallbackSpeciality = value                         
                    elif 'Notes'.lower() == key.lower().replace(':',''):
                        notes = value
                        
            row_data = {
                "Status": status,
                "Secondary Grade":secondary_grade,
                "EmailId":sender_email,
                "Speciality":speciality,
                "Start":start_time,
                "Priority":priority,
                "Trust Code":trust_code,
                "EmailReceivedDate":str(EmailReceivedDate),
                "Grade": grade,
                "Request Id": req_id,
                "Gender":gender,
                "From":from_name,
                "Agency Staff": agency_staff,
                "Date": shift_date,
                "Cost Centre Desc": cost_centre_desc,												
                "Subject": subject,
                "FallbackSpeciality": fallbackSpeciality,												
                "Ward": ward,
                "Skills": skills,
                "Cost Centre": cost_centre,
                "End": end_time,
                "Secondary Grade Type": secondary_grade_type,
                "Grade Type": grade_type                      
            }   
        
      
            # Append the row_data dictionary to the table_data list
            table_data.append(row_data)
    
    # Convert table_data list to JSON format
    json_data = json.dumps(table_data, indent=4)
    with open('iow_open_data.json', "w") as file:
        # file = open('content.txt', 'w')
        # file.write(html_body)
        file.write(json_data)
        file.close()
    # print(json_data)    
   
    return table_data

def iow_close_shift_scraping():
    email = Message(IOW_close_path)
    html_body = email.htmlBody
    # with open('iow_closed.html', "w", encoding="utf-8") as file:
    #     # file = open('content.txt', 'w')
    #     # file.write(html_body)
    #     file.write(html_body.decode("utf-8"))
    #     file.close()
    print("Subject:", email.subject)
    subject = email.subject
    sender = email.sender
    print("sender:", sender)
    sender_email = sender.split('<')[1].replace('>','')
    from_name = sender.split('<')[0]
    print("sender_email:", sender_email)
    print("from_name:",from_name)
    print("Recipients:", email.to)
    to = email.to

    print("CC:", email.cc)
    print("Date:", email.date)
    EmailReceivedDate = email.date
    email_body = os.linesep.join(
                        [
                            line for line in email.body.splitlines()
                            if line
                        ]
                    )
    print("Text Content without XML Tags:\n", email_body)
    
    soup = BeautifulSoup(html_body, 'html.parser')
    html = soup.find_all('html')
    # body = html.find_all('body')[0].find_all('html')
    # print('body = ',len(body))
    body_list = []
    table_data = []
    # print('html=    ',html)
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
    secondary_grade = None
    speciality = None
    priority = None
    cost_centre_desc = None
    fallbackSpeciality = None
    cost_centre = None
    secondary_grade_type = None
    grade_type = None
    for body in html:
        # print('body=    ',body)
        body_ = body.find_all('body')#[0].find_all('html')[count].find_all('body')
        # # print('body_ = ',body_)
        # body_list.append(body_)
        
        
        if body_[0].find_all('table'):
            tr = body.find_all('tr')
            print('tr=',len(tr), tr)
            for r in tr:
                # print("Request Id Row:", r)
                # Find all <td> tags in the row
                cells = r.find_all('td')
                
                # Extract text from the first and second <td> tags              ###check if index can be dynamic
                if len(cells) >= 2:
                    key = cells[0].get_text().strip()
                    value = cells[1].get_text().strip()
                    print('key = ',key)
                    if 'Request Id'.lower() == key.lower().replace(':',''):
                        req_id = value
                        print('req_id= ',req_id)
                        
                    elif 'Date'.lower() == key.lower().replace(':',''):
                        shift_date = value
                        print('shift_date= ',shift_date)
                        
                    elif 'Trust Code'.lower() == key.lower().replace(':',''):
                        trust_code = value
                        print('trust_code= ',trust_code)
                        
                    elif 'Ward'.lower() == key.lower().replace(':',''):
                        ward = value    
                        print('ward= ',ward)
                                              
                    elif 'Cost Centre'.lower() == key.lower().replace(':',''):
                        cost_centre = value 
                        print('cost_centre= ',cost_centre)
                          
                    elif 'Cost Centre Desc'.lower() == key.lower().replace(':',''):
                        cost_centre_desc = value
                        print('cost_centre_desc= ',cost_centre_desc)
                        
                    elif 'Start'.lower() == key.lower().replace(':',''):
                        start_time = value
                        print('start_time= ',start_time)
                        
                    elif 'End'.lower() == key.lower().replace(':',''):
                        end_time = value     
                        print('end_time= ',end_time)
                                          
                    elif 'Grade Type'.lower() == key.lower().replace(':',''):                        
                        grade_type = value                        
                        print('grade_type= ',grade_type)
                    elif 'Grade'.lower() == key.lower().replace(':',''):
                        grade = value  
                        print('grade= ',grade)
                                              
                    elif 'Secondary Grade Type'.lower() == key.lower().replace(':',''):
                        print('111= ',key.lower().replace(':',''))
                        secondary_grade_type = value 
                        print('secondary_grade_type= ',secondary_grade_type)
                           
                                             
                    elif 'Secondary Grade'.lower() == key.lower().replace(':',''):
                        secondary_grade = value     
                        print('secondary_grade= ',secondary_grade)
                                           
                    elif 'Skills'.lower() == key.lower().replace(':',''):
                        skills = value
                        print('skills= ',skills)
                        
                    elif 'Gender'.lower() == key.lower().replace(':',''):
                        gender = value
                        print('gender= ',gender)                        
                    elif 'Priority'.lower() == key.lower().replace(':',''):
                        priority = value 
                        print('priority= ',priority)
                                                 
                    elif 'Status'.lower() == key.lower().replace(':',''):
                        status = value
                        print('status= ',status)
                        
                    elif 'Agency Staff'.lower() == key.lower().replace(':',''):
                        agency_staff = value 
                        print('agency_staff= ',agency_staff)
                                              
                    elif 'Speciality'.lower() == key.lower().replace(':',''):
                        speciality = value   
                        print('speciality= ',speciality)
                                              
                    elif 'FallbackSpeciality'.lower() == key.lower().replace(':',''):
                        fallbackSpeciality = value     
                        print('fallbackSpeciality= ',fallbackSpeciality)
                                            
                    elif 'Notes'.lower() == key.lower().replace(':',''):
                        notes = value
                        print('notes= ',notes)
                        
                        
            row_data = {
                "Status": status,
                "Secondary Grade":secondary_grade,
                "EmailId":sender_email,
                "Speciality":speciality,
                "Start":start_time,
                "Priority":priority,
                "Trust Code":trust_code,
                "EmailReceivedDate":str(EmailReceivedDate),
                "Grade": grade,
                "Request Id": req_id,
                "Gender":gender,
                "From":from_name,
                "Agency Staff": agency_staff,
                "Date": shift_date,
                "Cost Centre Desc": cost_centre_desc,												
                "Subject": subject,
                "FallbackSpeciality": fallbackSpeciality,												
                "Ward": ward,
                "Skills": skills,
                "Cost Centre": cost_centre,
                "End": end_time,
                "Secondary Grade Type": secondary_grade_type,
                "Grade Type": grade_type                      
            }   
        
      
            # Append the row_data dictionary to the table_data list
            table_data.append(row_data)
    
    # Convert table_data list to JSON format
    json_data = json.dumps(table_data, indent=4)
    with open('iow_close_data.json', "w") as file:
        # file = open('content.txt', 'w')
        # file.write(html_body)
        file.write(json_data)
        file.close()
    # print(json_data)    
   
    return table_data

# iow_open_res = iow_open_shift_scraping()
# iow_closed_res = iow_close_shift_scraping()
# iow_json = {'Open Shifts': iow_open_res,
#               'Closed Shifts': iow_closed_res}

# iow_final_json = json.dumps(iow_json, indent=4)

# IOWfileName = 'IOW_Shift_Details_JSON_%d_%m_%Y_%H_%M_%S.json'
# IOWfileName = datetime.now().strftime(IOWfileName)
# with open(IOWfileName, "w") as file:
       
#         # json.dump(iow_final_json, file, indent=None)
#         file.write(iow_final_json)
#         file.close()

def fhft_open_shift_scraping():
    email = Message(FHFT_open_path)
    html_body = email.htmlBody
    # with open('fhft_open.html', "w", encoding="utf-8") as file:
    #     # file = open('content.txt', 'w')
    #     # file.write(html_body)
    #     file.write(html_body.decode("utf-8"))
    #     file.close()
    print("Subject:", email.subject)
    subject = email.subject
    sender = email.sender
    print("sender:", sender)
    sender_email = sender.split('<')[1].replace('>','')
    from_name = sender.split('<')[0]
    print("sender_email:", sender_email)
    print("from_name:",from_name)
    print("Recipients:", email.to)
    to = email.to

    print("CC:", email.cc)
    print("Date:", email.date)
    EmailReceivedDate = email.date
    
    soup = BeautifulSoup(html_body, 'html.parser')
    html = soup.find_all('html')[0].find_all('body')[0].find_all('table')
    # body = html.find_all('body')[0].find_all('html')
    # print('body = ',len(body))
    body_list = []
    table_data = []
    # print('html=    ',html)
    
    for table in html:
            # print('table=    ',table)
        # body_ = body.find_all('table')#[0].find_all('html')[count].find_all('body')
        # # print('body_ = ',body_)
        # body_list.append(body_)
    
            tr = table.find_all('tr')[0].find_all('tr')
            # print('tr=',len(tr), tr)
            req_id = None
            shift_date = None
            # trust_code= None
            ward= None
            start_time= None
            end_time= None
            grade= None
            # skills= None
            gender= None
            status= None
            agency_staff= None
            # secondary_grade = None
            speciality = None
            priority = None
            cost_centre_desc = None
            fallbackSpeciality = None
            cost_centre = None
            secondary_grade_type = None
            grade_type = None
            
            for r in tr:
                # print("Request Id Row:", r)
                # Find all <td> tags in the row
                cells = r.find_all('td')
                
                # Extract text from the first and second <td> tags              ###check if index can be dynamic
                if len(cells) >= 2:
                    key = cells[0].get_text().strip()
                    value = cells[1].get_text().strip()
                    print('key = ',key)
                    
                    if 'Request Id'.lower() == key.lower().replace(':',''):
                        req_id = value
                        print('req_id= ',req_id)
                        
                    elif 'Date'.lower() == key.lower().replace(':',''):
                        shift_date = value
                        print('shift_date= ',shift_date)
                        
                    elif 'Trust Code'.lower() == key.lower().replace(':',''):
                        trust_code = value
                        print('trust_code= ',trust_code)
                        
                    elif 'Ward'.lower() == key.lower().replace(':',''):
                        ward = value    
                        print('ward= ',ward)
                                              
                    elif 'Cost Centre'.lower() == key.lower().replace(':',''):
                        cost_centre = value 
                        print('cost_centre= ',cost_centre)
                          
                    elif 'Cost Centre Desc'.lower() == key.lower().replace(':',''):
                        cost_centre_desc = value
                        print('cost_centre_desc= ',cost_centre_desc)
                        
                    elif 'Start'.lower() == key.lower().replace(':',''):
                        start_time = value
                        print('start_time= ',start_time)
                        
                    elif 'End'.lower() == key.lower().replace(':',''):
                        end_time = value     
                        print('end_time= ',end_time)
                                          
                    elif 'Grade Type'.lower() == key.lower().replace(':',''):                        
                        grade_type = value                        
                        print('grade_type= ',grade_type)
                    elif 'Grade'.lower() == key.lower().replace(':',''):
                        grade = value  
                        print('grade= ',grade)
                                              
                    elif 'Secondary Grade Type'.lower() == key.lower().replace(':',''):
                        print('111= ',key.lower().replace(':',''))
                        secondary_grade_type = value 
                        print('secondary_grade_type= ',secondary_grade_type)
                           
                                             
                    elif 'Secondary Grade'.lower() == key.lower().replace(':',''):
                        secondary_grade = value     
                        print('secondary_grade= ',secondary_grade)
                                           
                    elif 'Skills'.lower() == key.lower().replace(':',''):
                        skills = value
                        print('skills= ',skills)
                        
                    elif 'Gender'.lower() == key.lower().replace(':',''):
                        gender = value
                        print('gender= ',gender)                        
                    elif 'Priority'.lower() == key.lower().replace(':',''):
                        priority = value 
                        print('priority= ',priority)
                                                 
                    elif 'Status'.lower() == key.lower().replace(':',''):
                        status = value
                        print('status= ',status)
                        
                    elif 'Agency Staff'.lower() == key.lower().replace(':',''):
                        agency_staff = value 
                        print('agency_staff= ',agency_staff)
                                              
                    elif 'Speciality'.lower() == key.lower().replace(':',''):
                        speciality = value   
                        print('speciality= ',speciality)
                                              
                    elif 'FallbackSpeciality'.lower() == key.lower().replace(':',''):
                        fallbackSpeciality = value     
                        print('fallbackSpeciality= ',fallbackSpeciality)
                                            
                    elif 'Notes'.lower() == key.lower().replace(':',''):
                        notes = value
                        print('notes= ',notes)
                        
            row_data = {
                    "Status": status,
                # "Secondary Grade":secondary_grade,
                    "EmailId":sender_email,
                    "Speciality":speciality,
                    "Start":start_time,
                    "Priority":priority,
                # "Trust Code":trust_code,
                    "EmailReceivedDate":str(EmailReceivedDate),
                    "Grade": grade,
                    "Request Id": req_id,
                    "Gender":gender,
                    "From":from_name,
                    "Agency Staff": agency_staff,
                    "Date": shift_date,
                    "Cost Centre Desc": cost_centre_desc,												
                    "Subject": subject,
                    "FallbackSpeciality": fallbackSpeciality,												
                    "Ward": ward,
                    "Cost Centre": cost_centre,
                    "End": end_time,
                    "Secondary Grade Type": secondary_grade_type,
                    "Grade Type": grade_type                      
            }   
            
      
            # Append the row_data dictionary to the table_data list
            table_data.append(row_data)
    
    # Convert table_data list to JSON format
    json_data = json.dumps(table_data, indent=4)
    with open('fhft_open_data.json', "w") as file:
        # file = open('content.txt', 'w')
        # file.write(html_body)
        file.write(json_data)
        file.close()
    # print(json_data)    
   
    return table_data


def fhft_close_shift_scraping():
    email = Message(FHFT_close_path)
    html_body = email.htmlBody
    # with open('fhft_close.html', "w", encoding="utf-8") as file:
    #     # file = open('content.txt', 'w')
    #     # file.write(html_body)
    #     file.write(html_body.decode("utf-8"))
    #     file.close()
    print("Subject:", email.subject)
    subject = email.subject
    sender = email.sender
    print("sender:", sender)
    sender_email = sender.split('<')[1].replace('>','')
    from_name = sender.split('<')[0]
    print("sender_email:", sender_email)
    print("from_name:",from_name)
    print("Recipients:", email.to)
    to = email.to

    print("CC:", email.cc)
    print("Date:", email.date)
    EmailReceivedDate = email.date
    
    soup = BeautifulSoup(html_body, 'html.parser')
    html = soup.find_all('html')#[0].find_all('body')[0].find_all('table')
    # body = html.find_all('body')[0].find_all('html')
    # print('body = ',len(body))
    body_list = []
    table_data = []
    # print('html=    ',html)
                            
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
    secondary_grade = None
    speciality = None
    priority = None
    cost_centre_desc = None
    fallbackSpeciality = None
    cost_centre = None
    secondary_grade_type = None
    grade_type = None
    
    for body in html:
        # print('body=    ',body)
        body_ = body.find_all('body')#[0].find_all('html')[count].find_all('body')
        print('body_ = ',body_)
        # body_list.append(body_)
     
        if body_[0].find_all('table'):
            tr = body.find_all('tr')
            print('tr=',len(tr), tr)
            for r in tr:
                # print("Request Id Row:", r)
                # Find all <td> tags in the row
                cells = r.find_all('td')
                
                # Extract text from the first and second <td> tags              ###check if index can be dynamic
                if len(cells) >= 2:
                    key = cells[0].get_text().strip()
                    value = cells[1].get_text().strip()
                    print('key = ',key)
                    if 'Request Id'.lower() == key.lower().replace(':',''):
                        req_id = value
                        print('req_id= ',req_id)
                        
                    elif 'Date'.lower() == key.lower().replace(':',''):
                        shift_date = value
                        print('shift_date= ',shift_date)
                        
                    elif 'Trust Code'.lower() == key.lower().replace(':',''):
                        trust_code = value
                        print('trust_code= ',trust_code)
                        
                    elif 'Ward'.lower() == key.lower().replace(':',''):
                        ward = value    
                        print('ward= ',ward)
                                              
                    elif 'Cost Centre'.lower() == key.lower().replace(':',''):
                        cost_centre = value 
                        print('cost_centre= ',cost_centre)
                          
                    elif 'Cost Centre Desc'.lower() == key.lower().replace(':',''):
                        cost_centre_desc = value
                        print('cost_centre_desc= ',cost_centre_desc)
                        
                    elif 'Start'.lower() == key.lower().replace(':',''):
                        start_time = value
                        print('start_time= ',start_time)
                        
                    elif 'End'.lower() == key.lower().replace(':',''):
                        end_time = value     
                        print('end_time= ',end_time)
                                          
                    elif 'Grade Type'.lower() == key.lower().replace(':',''):                        
                        grade_type = value                        
                        print('grade_type= ',grade_type)
                    elif 'Grade'.lower() == key.lower().replace(':',''):
                        grade = value  
                        print('grade= ',grade)
                                              
                    elif 'Secondary Grade Type'.lower() == key.lower().replace(':',''):
                        print('111= ',key.lower().replace(':',''))
                        secondary_grade_type = value 
                        print('secondary_grade_type= ',secondary_grade_type)
                           
                                             
                    elif 'Secondary Grade'.lower() == key.lower().replace(':',''):
                        secondary_grade = value     
                        print('secondary_grade= ',secondary_grade)
                                           
                    elif 'Skills'.lower() == key.lower().replace(':',''):
                        skills = value
                        print('skills= ',skills)
                        
                    elif 'Gender'.lower() == key.lower().replace(':',''):
                        gender = value
                        print('gender= ',gender)                        
                    elif 'Priority'.lower() == key.lower().replace(':',''):
                        priority = value 
                        print('priority= ',priority)
                                                 
                    elif 'Status'.lower() == key.lower().replace(':',''):
                        status = value
                        print('status= ',status)
                        
                    elif 'Agency Staff'.lower() == key.lower().replace(':',''):
                        agency_staff = value 
                        print('agency_staff= ',agency_staff)
                                              
                    elif 'Speciality'.lower() == key.lower().replace(':',''):
                        speciality = value   
                        print('speciality= ',speciality)
                                              
                    elif 'FallbackSpeciality'.lower() == key.lower().replace(':',''):
                        fallbackSpeciality = value     
                        print('fallbackSpeciality= ',fallbackSpeciality)
                                            
                    elif 'Notes'.lower() == key.lower().replace(':',''):
                        notes = value
                        print('notes= ',notes)
                        
                        
            row_data = {
                "Status": status,
                "Secondary Grade":secondary_grade,
                "EmailId":sender_email,
                "Speciality":speciality,
                "Start":start_time,
                "Priority":priority,
                "Trust Code":trust_code,
                "EmailReceivedDate":str(EmailReceivedDate),
                "Grade": grade,
                "Request Id": req_id,
                "Gender":gender,
                "From":from_name,
                "Agency Staff": agency_staff,
                "Date": shift_date,
                "Cost Centre Desc": cost_centre_desc,												
                "Subject": subject,
                "FallbackSpeciality": fallbackSpeciality,												
                "Ward": ward,
                "Skills": skills,
                "Cost Centre": cost_centre,
                "End": end_time,
                "Secondary Grade Type": secondary_grade_type,
                "Grade Type": grade_type                      
            }   
        
      
            # Append the row_data dictionary to the table_data list
            table_data.append(row_data)
             
    # Convert table_data list to JSON format
    json_data = json.dumps(table_data, indent=4)
    with open('fhft_close_data.json', "w") as file:
        # file = open('content.txt', 'w')
        # file.write(html_body)
        file.write(json_data)
        file.close()
    # print(json_data)    
   
    return table_data     

       
# fhft_open_res = fhft_open_shift_scraping()
# fhft_closed_res =fhft_close_shift_scraping()

# fhft_json = {'Open Shifts': fhft_open_res,
#               'Closed Shifts': fhft_closed_res}

# fhft_final_json = json.dumps(fhft_json, indent=4)

# FHFTfileName = 'FHFT_Shift_Details_JSON_%d_%m_%Y_%H_%M_%S.json'
# FHFTfileName = datetime.now().strftime(FHFTfileName)
# with open(FHFTfileName, "w") as file:
       
#         # json.dump(fhft_final_json, file, indent=None)
#         file.write(fhft_final_json)
#         file.close()
        
lms_open_shift_path = 'D:/EPI_Saniya/Id-Medical_old/EWS_Outlook/doctors sample mails/New job notification.msg'
def doctors_open_shift_scraping():
    email = Message(lms_open_shift_path)
    html_body = email.htmlBody
    with open('lms_open.html', "w", encoding="utf-8") as file:
        # file = open('content.txt', 'w')
        # file.write(html_body)
        file.write(html_body.decode("utf-8"))
        file.close()
    print("Subject:", email.subject)
    subject = email.subject
    sender = email.sender
    print("sender:", sender)
    sender_email = sender.split('<')[1].replace('>','')
    from_name = sender.split('<')[0]
    print("sender_email:", sender_email)
    print("from_name:",from_name)
    print("Recipients:", email.to)
    to = email.to

    print("CC:", email.cc)
    print("Date:", email.date)
    EmailReceivedDate = email.date
    
    soup = BeautifulSoup(html_body, 'html.parser')
    html = soup.find_all('html')#[0].find_all('body')[0].find_all('table')
    # body = html.find_all('body')[0].find_all('html')
    # print('body = ',len(body))
    body_list = []
    table_data = []
    # print('html=    ',html)
                            
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
    secondary_grade = None
    speciality = None
    priority = None
    cost_centre_desc = None
    fallbackSpeciality = None
    cost_centre = None
    secondary_grade_type = None
    grade_type = None
    
    for body in html:
        # print('body=    ',body)
        body_ = body.find_all('body')#[0].find_all('html')[count].find_all('body')
        print('body_ = ',body_)
        # body_list.append(body_)
     
        if body_[0].find_all('table'):
            tr = body.find_all('tr')
            print('tr=',len(tr), tr)
            for r in tr:
                # print("Request Id Row:", r)
                # Find all <td> tags in the row
                cells = r.find_all('td')
                
                # Extract text from the first and second <td> tags              ###check if index can be dynamic
                if len(cells) >= 2:
                    key = cells[0].get_text().strip()
                    value = cells[1].get_text().strip()
                    print('key = ',key)
                    if 'Request Id'.lower() == key.lower().replace(':',''):
                        req_id = value
                        print('req_id= ',req_id)
                        
                    elif 'Date'.lower() == key.lower().replace(':',''):
                        shift_date = value
                        print('shift_date= ',shift_date)
                        
                    elif 'Trust Code'.lower() == key.lower().replace(':',''):
                        trust_code = value
                        print('trust_code= ',trust_code)
                        
                    elif 'Ward'.lower() == key.lower().replace(':',''):
                        ward = value    
                        print('ward= ',ward)
                                              
                    elif 'Cost Centre'.lower() == key.lower().replace(':',''):
                        cost_centre = value 
                        print('cost_centre= ',cost_centre)
                          
                    elif 'Cost Centre Desc'.lower() == key.lower().replace(':',''):
                        cost_centre_desc = value
                        print('cost_centre_desc= ',cost_centre_desc)
                        
                    elif 'Start'.lower() == key.lower().replace(':',''):
                        start_time = value
                        print('start_time= ',start_time)
                        
                    elif 'End'.lower() == key.lower().replace(':',''):
                        end_time = value     
                        print('end_time= ',end_time)
                                          
                    elif 'Grade Type'.lower() == key.lower().replace(':',''):                        
                        grade_type = value                        
                        print('grade_type= ',grade_type)
                    elif 'Grade'.lower() == key.lower().replace(':',''):
                        grade = value  
                        print('grade= ',grade)
                                              
                    elif 'Secondary Grade Type'.lower() == key.lower().replace(':',''):
                        print('111= ',key.lower().replace(':',''))
                        secondary_grade_type = value 
                        print('secondary_grade_type= ',secondary_grade_type)
                           
                                             
                    elif 'Secondary Grade'.lower() == key.lower().replace(':',''):
                        secondary_grade = value     
                        print('secondary_grade= ',secondary_grade)
                                           
                    elif 'Skills'.lower() == key.lower().replace(':',''):
                        skills = value
                        print('skills= ',skills)
                        
                    elif 'Gender'.lower() == key.lower().replace(':',''):
                        gender = value
                        print('gender= ',gender)                        
                    elif 'Priority'.lower() == key.lower().replace(':',''):
                        priority = value 
                        print('priority= ',priority)
                                                 
                    elif 'Status'.lower() == key.lower().replace(':',''):
                        status = value
                        print('status= ',status)
                        
                    elif 'Agency Staff'.lower() == key.lower().replace(':',''):
                        agency_staff = value 
                        print('agency_staff= ',agency_staff)
                                              
                    elif 'Speciality'.lower() == key.lower().replace(':',''):
                        speciality = value   
                        print('speciality= ',speciality)
                                              
                    elif 'FallbackSpeciality'.lower() == key.lower().replace(':',''):
                        fallbackSpeciality = value     
                        print('fallbackSpeciality= ',fallbackSpeciality)
                                            
                    elif 'Notes'.lower() == key.lower().replace(':',''):
                        notes = value
                        print('notes= ',notes)
                        
                        
            row_data = {
                "Status": status,
                "Secondary Grade":secondary_grade,
                "EmailId":sender_email,
                "Speciality":speciality,
                "Start":start_time,
                "Priority":priority,
                "Trust Code":trust_code,
                "EmailReceivedDate":str(EmailReceivedDate),
                "Grade": grade,
                "Request Id": req_id,
                "Gender":gender,
                "From":from_name,
                "Agency Staff": agency_staff,
                "Date": shift_date,
                "Cost Centre Desc": cost_centre_desc,												
                "Subject": subject,
                "FallbackSpeciality": fallbackSpeciality,												
                "Ward": ward,
                "Skills": skills,
                "Cost Centre": cost_centre,
                "End": end_time,
                "Secondary Grade Type": secondary_grade_type,
                "Grade Type": grade_type                      
            }   
        
      
            # Append the row_data dictionary to the table_data list
            table_data.append(row_data)
             
    # Convert table_data list to JSON format
    json_data = json.dumps(table_data, indent=4)
    with open('fhft_close_data.json', "w") as file:
        # file = open('content.txt', 'w')
        # file.write(html_body)
        file.write(json_data)
        file.close()
    # print(json_data)    
   
    return table_data     
  
doctors_open_shift_scraping()  
