FROM python:3.9

COPY . /app

# Create a directory for scraped files
RUN mkdir -p /app/Downloads/unfilled/3_days
# RUN mkdir -p /app/Downloads/unfilled/28_days

# Create a directory for scraping execution summury files
RUN mkdir -p /app/3_days_requirements_excels/unfilled
# RUN mkdir -p /NHSP_Filled_Requirements_Scraping_And_Cancellation/28_days_requirements_excels/unfilled
                # /NHSP_Filled_Requirements_Scraping_And_Cancellation/28_days_requirements_excels/unfilled/
WORKDIR /app

# Install Firefox
RUN apt-get update && apt-get install -y firefox-esr

# #Install libraries required for chromedriver
# RUN apt-get update && apt-get install -y libglib2.0-0 \ 
#     libnss3 \
#     libgconf-2-4 \
#     libfontconfig1

# # Install dependencies
# RUN apt-get update && apt-get install -y \
#     wget \
#     gnupg \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# # Install Google Chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
#     && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
#     && apt-get update \
#     && apt-get install -y google-chrome-stable \
#     && rm -rf /var/lib/apt/lists/*
    
RUN pip install -r requirements.txt 

# Set up a volume for storing downloaded files
# VOLUME /app/downloads

EXPOSE 8001
# CMD ["python","main_3_days_scraping.py"]
CMD ["python","main.py"]