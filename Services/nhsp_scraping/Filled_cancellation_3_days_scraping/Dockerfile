FROM python:3.9

WORKDIR /app

COPY . /app

# Create a directory for scraped files
RUN mkdir -p /app/Downloads/filled/3_days

# # Create a directory for scraping execution summury files
# RUN mkdir -p /NHSP_Filled_Requirements_Scraping_And_Cancellation/28_days_requirements_excels/unfilled
             
# Install Firefox
RUN apt-get update && apt-get install -y firefox-esr

RUN pip install -r requirements.txt 

EXPOSE 8003
# CMD ["python","main_3_days_scraping.py"]
CMD ["python","main.py"]


