FROM python:2.7

RUN mkdir /sources
COPY . /sources/
WORKDIR /sources

RUN cd /sources/
RUN pip2 install --upgrade pip
RUN pip2 install -r requirements.txt

RUN python2 manage.py makemigrations
RUN python2 manage.py migrate

EXPOSE 8000
CMD ["python2", "manage.py", "runserver", "0.0.0.0:8000"]
