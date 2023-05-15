FROM python:3.10
WORKDIR /app
COPY requirements.txt /app
COPY etl.py /app
RUN pip install -r requirements.txt
CMD ["python", "etl.py"]