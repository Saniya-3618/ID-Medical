FROM python:3.9

WORKDIR /app

COPY . /app

# Create a directory for scraped files
RUN mkdir -p /app/Downloads/filled/28_days

# Install Firefox
RUN apt-get update && apt-get install -y firefox-esr

RUN pip install -r requirements.txt 


EXPOSE 8004
# CMD ["python","main_3_days_scraping.py"]
CMD ["python","main.py"]

# Create a directory for scraping execution summury files
# RUN mkdir -p /app/28_days_requirements_excels/unfilled
# RUN mkdir -p /app/28_days_requirements_excels/filled            


# # Install Firefox
# RUN apt-get update && apt-get install -y firefox-esr

# #Install libraries required for chromedriver
# RUN apt-get update && apt-get install -y libglib2.0-0 \ 
#     libnss3 \
#     libgconf-2-4 \
#     libfontconfig1

# RUN apt-get update && \
#     apt-get install -y \
#     wget \
#     gnupg \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
#     && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
#     && apt-get update \
#     && apt-get install -y google-chrome-stable \
#     && rm -rf /var/lib/apt/lists/*

# RUN apt-get update && apt-get install wget unzip && \ 
#     wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \ 
#     apt install -y ./google-chrome-stable_current_amd64.deb && \ 
#     rm google-chrome-stable_current_amd64.deb && \ 
#     apt-get clean

# # Install Google Chrome
# RUN apt-get update && apt-get install -y google-chrome-stable 

    
