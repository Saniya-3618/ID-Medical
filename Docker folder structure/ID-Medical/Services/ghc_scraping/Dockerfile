FROM python:3.9

COPY . /app

WORKDIR /app

# Install Firefox
RUN apt-get update && apt-get install -y firefox-esr
    
RUN pip install -r requirements.txt 


EXPOSE 8006
# CMD ["python","main_3_days_scraping.py"]
CMD ["python","main.py"]