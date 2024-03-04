FROM python:3.9

WORKDIR /app

COPY . /app

# Create a directory for scraped files
RUN mkdir -p /app/Downloads/unfilled/28_days

# Create a directory for scraping execution summury files
RUN mkdir -p /app/28_days_requirements_excels/unfilled

# Install Firefox
RUN apt-get update && apt-get install -y firefox-esr

# # Install Chrome WebDriver
# RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
#     mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
#     curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
#     unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
#     rm /tmp/chromedriver_linux64.zip && \
#     chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
#     ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

# # Install Google Chrome
# RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#     echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
#     apt-get -yqq update && \
#     apt-get -yqq install google-chrome-stable && \
#     rm -rf /var/lib/apt/lists/*


RUN pip install -r requirements.txt 


EXPOSE 8002
# CMD ["python","main_3_days_scraping.py"]
CMD ["python","main.py"]


# # install google chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# RUN apt-get -y update
# RUN apt-get install -y google-chrome-stable

# # install chromedriver
# RUN apt-get install -yqq unzip
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# RUN mkdir -p /chromedriver

# RUN apt-get update && \
#     apt-get install -y gnupg wget curl unzip --no-install-recommends && \
#     wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#     echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list 

# RUN apt-get update -y && apt-get install -y google-chrome-stable 

# RUN CHROME_VERSION=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
#     CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION") && \
#     wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" 

# RUN unzip /chromedriver/chromedriver* -d /usr/local/bin/

# # Set up Chromedriver Environment variables
# ENV CHROMEDRIVER_VERSION 120.0.6099.109
# ENV CHROMEDRIVER_DIR /chromedriver
# RUN mkdir $CHROMEDRIVER_DIR
# # Download and install Chromedriver
# RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
# RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR
# # Put Chromedriver into the PATH
# ENV PATH $CHROMEDRIVER_DIR:$PATH


# RUN DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
#     wget https://chromedriver.storage.googleapis.com/$DRIVER_VERSION/chromedriver_linux64.zip && \
#     unzip chromedriver_linux64.zip -d /usr/bin/ && rm chromedriver_linux64.zip && chmod +x /usr/bin/chromedriver

# RUN apt-get update && apt-get install wget unzip && \ 
#     wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \ 
#     apt install -y ./google-chrome-stable_current_amd64.deb && \ 
#     rm google-chrome-stable_current_amd64.deb && \ 
#     apt-get clean
# # Install Google Chrome
# RUN apt-get update && apt-get install -y google-chrome-stable 
# Adding trusting keys to apt for repositories
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# # Adding Google Chrome to the repositories
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# # Updating apt to see and install Google Chrome
# RUN apt-get -y update
# # Magic happens
# RUN apt-get install -y google-chrome-stable
# # Installing Unzip
# RUN apt-get install -yqq unzip
# # Download the Chrome Driver
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# # Unzip the Chrome Driver into /usr/local/bin directory
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# # # Set display port as an environment variable
# # ENV DISPLAY=:99







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



    
