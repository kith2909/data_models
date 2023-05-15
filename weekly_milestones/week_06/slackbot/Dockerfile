FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "slack.py"]