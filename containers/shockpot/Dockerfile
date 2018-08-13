FROM python:2.7

RUN git clone https://github.com/threatstream/shockpot.git

RUN pip install -r shockpot/requirements.txt

# disable logging and ip search as we don't need them
RUN sed -i '/enabled = True/c\enabled = False' shockpot/shockpot.conf

CMD python shockpot/shockpot.py
