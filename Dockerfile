FROM python:3.8-slim-buster

COPY . .

# Change this to correspond with last CMD parameter
EXPOSE 8080

# Change last option for setting default port
CMD [ "python3", "main.py", "-p" , "8080"] 