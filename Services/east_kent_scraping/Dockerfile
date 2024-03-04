FROM python:3.9

WORKDIR /app

COPY . /app

# # Create a directory for scraped files
# RUN mkdir -p /app/Downloads/filled/28_days

# Install Firefox
RUN apt-get update && apt-get install -y firefox-esr

RUN pip install -r requirements.txt 


EXPOSE 8005
# CMD ["python","main_3_days_scraping.py"]
CMD ["python","main.py"]

