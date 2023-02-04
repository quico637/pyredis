FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# Change this to correspond with last CMD parameter
EXPOSE 8080

# Change last option for setting default port
CMD [ "python3", "main.py", "-p" , "8080"] 