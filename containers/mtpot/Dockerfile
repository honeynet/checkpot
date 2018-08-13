FROM python:2.7

RUN git clone https://github.com/cymmetria/mtpot.git

RUN pip install telnetsrv gevent

CMD python mtpot/MTPot.py mtpot/mirai_conf.json
