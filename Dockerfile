FROM python:3.7-alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY record_location ./record_location/
COPY setup.py ./
RUN pip install -e .

CMD [ "record-location" ]