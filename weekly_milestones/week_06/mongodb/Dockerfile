FROM python:3.10
WORKDIR /app
COPY requirements.txt /app
COPY mongo_app.py /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "mongo_app.py"]