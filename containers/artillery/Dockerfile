FROM python:3.6

RUN git clone https://github.com/BinaryDefense/artillery.git
RUN cd artillery && echo "yes" > inputfile && echo "no" >> inputfile && echo "yes" >> inputfile
RUN bash -c "cd artillery && python setup.py < inputfile"

CMD python artillery/artillery.py
