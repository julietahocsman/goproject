
# write some code to build your image

FROM python3.9-nodejs15

COPY gopa_data /gopa_data
COPY goproject /goproject
COPY requirements.txt /requirements.txt
COPY run.sh /run.sh
COPY scripts /scripts
COPY raw_data / raw_data

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN npm install -g node-firestore-import-export

CMD python goproject/main.py download

ENV PYTHONPATH .
