# expose the port 5000
FROM python:3.9
COPY . /app 
WORKDIR /app 
RUN ["pip3", "install", "-r", "requirements.txt"]
EXPOSE 5000
CMD ["python3", "server.py"]
