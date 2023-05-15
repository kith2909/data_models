FROM python:3.10
WORKDIR /test
COPY requirements.txt ./
COPY reddit_app.py /test
COPY . /test
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "reddit_app.py"]