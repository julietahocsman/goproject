
# write some code to build your image

FROM python:3.8.8-buster

COPY gopa_data /gopa_data
COPY goproject /goproject
COPY requirements.txt /requirements.txt
COPY run.sh /run.sh
COPY scripts /scripts

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ./run.sh download