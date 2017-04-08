FROM python:latest
MAINTAINER squarenomad

ADD ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
ADD . /app
EXPOSE 5000

CMD ["python","manage.py","runserver","-h","0.0.0.0"]