FROM python:3

RUN pip install selenium
RUN pip install mysql-connector-python

ADD build /home