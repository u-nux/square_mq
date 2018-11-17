FROM ubuntu
MAINTAINER Yunus Ozden

RUN apt-get update

RUN apt-get install -y gcc python python-dev python-distribute python-pip
RUN apt-get install -y libev4 libev-dev

RUN apt-get install -y python-snappy

ADD . /square_mq

RUN pip install --upgrade pip
RUN pip install -r /square_mq/requirements.txt

EXPOSE 5000

WORKDIR /square_mq

CMD ./run_environments.sh

