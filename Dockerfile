FROM ubuntu:latest
MAINTAINER Olsi Birbo "olsi.birbo@ihsmarkit.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential mysql-server python-mysqldb flask-mysqldb flask-mysql
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
