FROM python:3.7

ADD ./flask/map.py /


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "./flask/map.py"]