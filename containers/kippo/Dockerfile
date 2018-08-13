FROM ubuntu:trusty

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y git openssl python-dev python-openssl python-pyasn1 python-twisted python-pip

RUN pip2 install twisted==15.1.0

#custom folder because homedir of user kippo causes a conflict
RUN git clone https://github.com/desaster/kippo.git /kipposource

RUN mv /kipposource/kippo.cfg.dist /kipposource/kippo.cfg

RUN useradd -d /kippo -s /bin/bash -m kippo -g sudo
RUN chown kippo /kipposource/ -R

EXPOSE 2222

USER kippo
WORKDIR /kipposource

CMD ["twistd", "--nodaemon", "-y", "/kipposource/kippo.tac", "--pidfile=/kipposource/kippo.pid"]
