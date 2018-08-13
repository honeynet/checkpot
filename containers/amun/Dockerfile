FROM python:2.7

RUN git clone https://github.com/zeroq/amun.git

# set IP from eth0
RUN sed -i '/ip: 127.0.0.1/c\ip: eth0' amun/conf/amun.conf

CMD python amun/amun_server.py
